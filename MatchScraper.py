from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pandas as pd
import time

# Setup
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Uncomment this if you want no browser window
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

def expand_all_tiers():
    try:
        tier_headers = driver.find_elements(By.CSS_SELECTOR, "div.gib-head[role='button']")
        for btn in tier_headers:
            try:
                driver.execute_script("arguments[0].click();", btn)
            except:
                pass
        time.sleep(2)
    except Exception as e:
        print("⚠️ Failed to expand tiers:", e)

def scrape_dota2():
    print("🔵 Scraping Dota 2 matches...")
    driver.get("https://liquipedia.net/dota2/Liquipedia:Matches")
    expand_all_tiers()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "match")))

    matches = []
    for card in driver.find_elements(By.CLASS_NAME, "match"):
        try:
            team1 = card.find_element(By.CLASS_NAME, "team-left").text.strip()
            team2 = card.find_element(By.CLASS_NAME, "team-right").text.strip()
            tournament = card.find_element(By.CLASS_NAME, "tournament-name").text.strip()
            timestamp = card.find_element(By.CLASS_NAME, "timer-object").get_attribute("data-timestamp")

            if not team1 or not team2:
                continue

            dt_utc = datetime.utcfromtimestamp(int(timestamp))
            dt_pht = dt_utc + timedelta(hours=8)

            matches.append({
                "Tournament": tournament,
                "Team 1": team1,
                "Team 2": team2,
                "Time (PHT)": dt_pht.strftime("%Y-%m-%d %H:%M"),
                "Game": "Dota 2"
            })
        except:
            continue
    return matches

def scrape_cs2():
    print("🟠 Scraping CS2 matches...")
    driver.get("https://liquipedia.net/counterstrike/Liquipedia:Matches")
    expand_all_tiers()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "wikitable")))

    matches = []
    tables = driver.find_elements(By.CLASS_NAME, "wikitable")
    for table in tables:
        try:
            rows = table.find_elements(By.TAG_NAME, "tr")
            if len(rows) < 2:
                continue

            team1 = rows[0].find_element(By.CLASS_NAME, "team-left").text.strip()
            team2 = rows[0].find_element(By.CLASS_NAME, "team-right").text.strip()

            if not team1 or not team2:
                continue

            timestamp = rows[1].find_element(By.CLASS_NAME, "timer-object").get_attribute("data-timestamp")

            try:
                tournament = rows[1].find_element(By.CSS_SELECTOR, "div.text-nowrap a").text.strip()
                if not tournament:
                    tournament = rows[1].find_element(By.CSS_SELECTOR, "div.text-nowrap a").get_attribute("title").strip()
            except:
                tournament = "Unknown"

            dt_utc = datetime.utcfromtimestamp(int(timestamp))
            dt_pht = dt_utc + timedelta(hours=8)

            matches.append({
                "Tournament": tournament,
                "Team 1": team1,
                "Team 2": team2,
                "Time (PHT)": dt_pht.strftime("%Y-%m-%d %H:%M"),
                "Game": "CS2"
            })
        except:
            continue
    return matches

# Run both scrapers
dota_matches = scrape_dota2()
cs2_matches = scrape_cs2()
driver.quit()

# Combine and clean
all_matches = dota_matches + cs2_matches
cleaned = [m for m in all_matches if m["Team 1"].strip() and m["Team 2"].strip()]

# Export
# Write to JavaScript file instead of Excel
with open("match.js", "w", encoding="utf-8") as f:
    f.write("// Tournament match data\n")
    f.write("const tournamentData = [\n")
    for match in all_matches:
        f.write(f'    {{ tournament: "{match["Tournament"]}", team1: "{match["Team 1"]}", team2: "{match["Team 2"]}", time: "{match["Time (PHT)"]}", game: "{match["Game"]}" }},\n')
    f.write("];\n\n// Export the data so it can be used in other files\n")
    f.write("export { tournamentData };\n")
