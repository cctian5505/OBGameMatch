# Game Tournament Calendar

A web-based calendar application that displays and tracks esports tournament schedules, focusing on Dota 2 and CS2 matches. The project includes both a web interface for viewing matches and Python scripts for scraping match data from Liquipedia.

## Features

### Web Calendar Interface
- Interactive calendar view with match details
- Table view for listing all matches
- Filter matches by game and tournament
- Real-time match status updates (Upcoming, Live, Completed)
- Countdown timers for upcoming matches
- Responsive design for mobile and desktop

### Match Data Collection
- Automated scraping from Liquipedia
- Supports both Dota 2 and CS2 tournaments
- Converts UTC timestamps to PHT (Philippine Time)
- Exports match data in JavaScript format

## Setup

### Prerequisites
- Python 3.x
- Chrome WebDriver
- Web browser (Chrome recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/cctian5505/OBGameMatch.git
   ```

2. Install Python dependencies:
   ```bash
   pip install selenium pandas
   ```

3. Make sure Chrome WebDriver is in the `chromedriver-win64` directory

### Usage

#### Updating Match Data
1. Run the Python scraper:
   ```bash
   python TryV3.py
   ```
2. The script will update `match.js` with the latest tournament data

#### Viewing the Calendar
1. Open `index.html` in a web browser
2. Use the tabs to switch between Calendar and Table views
3. Use filters to find specific matches

## Project Structure
- `index.html` - Main web interface
- `match.js` - Tournament match data
- `TryV3.py` - Match data scraper
- `chromedriver-win64/` - Chrome WebDriver files
- `.gitignore` - Git ignore rules

## Contributing
Feel free to fork the repository and submit pull requests for any improvements.

## License
This project is open source and available under the MIT License. 