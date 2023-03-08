# Forbes_100_Cloud_Jobs
Scraping the career pages of Forbes 100 Cloud startups for job openings and exporting to Airtable database. Each script is developed to scrape the career page of the designated company, saves the data as a CSV file in the job directory, and uploaded into airtable via API.

# Approach
The `run.py` script calls the `import_scrape_scripts.py` which calls the individual script files to scrape the career page. Each function call is enclosed in a `try - except` to catch and display any exception for a script that breaks during execution. The scraped jobs are concatenated into a single file `All_Job_Files.csv`. The concatenated job file is uploaded to Airtable database via API.

# Installations
Instructions on how to create one attached in PDF.

The following need to be installed:

1. requests
2. bs4
3. selenium
4. pyairtable

# Run
Execute the run script `run.py` to do all scrape, and upload data to Airtable.
