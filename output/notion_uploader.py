# 📤 Sends filtered leads to Notion (or Airtable/email)
import sys
import os
from notion_client import Client
from dotenv import load_dotenv
from pprint import pprint
import csv

# Add the project root to the Python path to allow for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.remoteok_scraper import scrape_remoteok

# Import configuration


# Load the environment variables from the .env file
load_dotenv()

# Access your secrets
api_key = os.getenv('API_KEY')

# Use them in your application
notion = Client(auth=api_key)
list_users_response = notion.users.list()
pprint(list_users_response)



def notion_upload(jobs):
    # Load the environment variables from the .env file
    load_dotenv()
    # Access your secrets
    api_key = os.getenv('API_KEY')

    # Use them in your application
    notion = Client(auth=api_key)
    list_users_response = notion.users.list()
    pprint(list_users_response)
    pprint(jobs)
    return jobs

    pass





'''
#CSVPARSER FOR BACKUP(OPTIONAL)
def csv_parser(file_path):
    """
    Reads a CSV file and processes its data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        with open(file_path, 'r', newline='') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)

            # Optional: Skip the header row if your CSV has one
            header = next(csv_reader)
            print(f"Header: {header}")

            # Iterate over each row in the CSV file
            for row in csv_reader:
                print(f"Row: {row}")
            # Accessing specific columns:
                title = row[0]
                company = row[1]
                location = row[2]
                salary = row [3]
                link = row[4]
                print(f"Name: {title}, Company: {company}, Location: {location}, Salary: {salary}, Link: {link}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
''' 



