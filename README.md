# Market Analysis (Trading Assistant)

> **Note: this is an old project.** I made it a long time ago as my Computer Science IA (Internal Assessment) for the May 2025 session, and the code was last modified in April 2025. I'm putting it on GitHub as I submitted it, so it shows where I was then and not how I'd write it today.

A desktop app (Python and PyQt6) that analyses Indian futures and options (F&O) data from the NSE. I built it for a real client, my dad, who trades the Indian stock market as a hobby. He's in a different time zone from the market, so he has to decide what to trade before it opens. Going through roughly 36,000 data points by hand every day wasn't realistic, so we agreed on a method and I automated it. That's also why the dashboard greets him by name.

## What it does

1. **Download:** pick a date and the app downloads that day's NSE F&O "Bhavcopy" file, unzips it, and saves a cleaned, sorted copy with only the columns the app needs.
2. **Preset Filter:** applies my dad's method to find anomalies. Once the data is sorted by stock and option type, a call (CE) should have a *falling* closing price as the strike price rises, and a put (PE) should have a *rising* one. Any row where the price moves the wrong way gets highlighted as a potential trade.
3. **Watchlist:** a list of stocks to track, with a place for notes on each one. Stocks can be added and removed, and everything is saved to CSV files.
4. **Search:** type a stock name to see all of its positions (closing price, strike price, day high, and so on).
5. **Log:** record trades (stock, date, strike, quantity, amount invested, profit or loss) and view them in a table. My dad asked for this in the second client interview.
6. **Dashboard and sidebar:** a landing page and a collapsible sidebar for moving between pages.

## How it went

Both of us were happy with the finished product. My dad liked having everything in one place and not having to download and unzip the file from the NSE site every day. Things he asked for that I didn't get to:

- A chart of each watchlist stock's recent growth
- A login screen, since the log holds private trading details
- A more interactive dashboard
- Price-target alerts for watchlist stocks
- Typing a company name and having the app look up its stock code

## Files

| File | Purpose |
|---|---|
| `Tanu_ia_interface.py` | The whole application |
| `Watchlist.csv` | Stocks on the watchlist |
| `Notes.csv` | Per-stock notes |
| `Log_Data.csv` | Trade log (example entries from development and testing) |

The downloaded market data goes in a `Files/` folder. It's not included because it's large and the app can re-download it.

## Running it

```bash
pip install PyQt6 requests
python Tanu_ia_interface.py
```

The file paths are hard-coded for my old Windows machine (`C:\Tanu\Coding\CSC IA\Code\...`). Before running, search for `C:\\Tanu` in `Tanu_ia_interface.py` and change the paths to your own folder. The places that need changing are marked with `### CHANGE TO ... PATH` comments.

## Known limitations

- Hard-coded Windows paths, as above.
- The NSE download URL and its access rules may have changed since I wrote this, so the download step might not work now.
- The Preset Filter is slow on large files because it repeatedly looks up each row's position in the list.
- Everything is in one file, and there are no automated tests.
