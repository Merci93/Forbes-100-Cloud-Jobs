import os
import csv
import glob
import requests
import pandas as pd
from pyairtable import Table, Api

# API token
# Replace this with the token created for the main account.
api_token = 'Add API token'

# Import and run scripts
from import_scrape_scripts import run_scripts
run_scripts()

# Delete old job file
os.remove('Jobs/All_Job_Files.csv')

# Get all files in the Job folder
all_files = glob.glob('Jobs/*.csv')

# Concatenate csv files
df = pd.concat(pd.read_csv(file) for file in all_files)
df.fillna('N/A', inplace = True)
df.drop_duplicates(inplace = True)
df.to_csv('Jobs/All_Job_Files.csv', index = False)

# Import data into airtable
# Replace the table_id with the id for the original table
# Same with the table name
table_id = 'appZvFSgHOBDFPSOg'
table_name = '/Cloud_100_Jobs'
post_url = 'https://airtable.com/' + table_id + table_name
post_headers = {'Authorization' : 'Bearer' +  api_token,
				'Content-Type': 'application/json'}

data_file = open('Jobs/All_Job_Files.csv')
csv_data = csv.reader(data_file)

api_key = os.getenv('PERSONAL_ACCESS_TOKEN', api_token)
table = Table(api_key, 'appZvFSgHOBDFPSOg', 'Cloud_100_Jobs')

for row in csv_data:
	Company = row[0]
	Role = row[1]
	Team = row[2]
	Location  = row[3]
	Job_URL = row[4]

	data = {'Company': Company, 'Role': Role, 'Team': Team, 'Location':Location, 
			'Job_URL': Job_URL}

	post_airtable_request = table.create(data)
