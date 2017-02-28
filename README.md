# NICAR 2017 Schedule as Structured Data

This repository contains the [NICAR 2017 conference schedule](https://ire.org/events-and-training/event/2702/) as JSON and CSV files, plus the underlying Python scraper.

*Going to NICAR? You might be interested in the [data, analyses, and tools we've open-sourced at BuzzFeed News](https://github.com/buzzfeednews/everything) and the [BuzzFeed Open Lab](https://github.com/buzzfeed-openlab). You might also be interested in [Data Is Plural](https://tinyletter.com/data-is-plural), my weekly newsletter of useful/curious datasets.*

## Get the data

*Last updated Feb. 27, 2017 @ 7:30pm  Eastern*

- [JSON schedule](schedule/nicar-2017-schedule.json?raw=true)
- [CSV schedule](schedule/nicar-2017-schedule.csv?raw=true)

## Run the scraper yourself

To run the scraper, you'll need Python 3. To get started, execute the following commands in your terminal:

```bash
mkvirtualenv nicar-2017-schedule # Optional, recommended
git clone https://github.com/jsvine/nicar-2017-schedule.git
cd nicar-2017-schedule
pip install -r requirements.txt
```

To run the scraper, execute this command:

```bash
make schedule
```

*Or*, more verbosely:

```bash
python ./scripts/scrape.py > schedule/nicar-2017-schedule.json
in2csv schedule/nicar-2017-schedule.json > schedule/nicar-2017-schedule.csv
```

## Look beneath the hood

You can find the Python script that extracts and formats the schedule [here](scripts/scrape.py).

## Fix/improve things

Pull requests are welcome.
