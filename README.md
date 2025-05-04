# Remote Job Scraper

This is a simple Python project to scrape remote job listings from [RemoteOK](https://remoteok.com).

## Features

- Search by job keyword (e.g. `python`, `data-scientist`)
- Scrapes job title, company, and job link
- Saves results to a CSV file

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```bash
python scraper.py
```

You will be prompted to enter a keyword. The scraper will then fetch jobs and save them in `jobs.csv`.
