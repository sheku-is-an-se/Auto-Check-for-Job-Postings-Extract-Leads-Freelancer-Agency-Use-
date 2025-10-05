# Cornerstone – schedule or run everything
import os

# Import project modules
from scraper.remoteok_scraper import scrape_remoteok
from output.file_writer import save_jobs_to_csv
from output.notion_uploader import notion_upload

# Import configuration
from config import OUTPUT_DIR, OUTPUT_FILENAME


def main():
    """
    Main function to orchestrate the job scraping and processing workflow.
    """
    print("Starting the job scraping process...")
    scraped_jobs = []
    try:
        # 1. Scrape jobs from RemoteOK
        scraped_jobs = scrape_remoteok()
    except Exception as e:
        print(f"\nThe main process failed: {e}")
        print("Aborting operation. No file will be saved.")

    print(f"\n--- Scraping Summary ---")
    # 2. If jobs were found, save them to a file
    if scraped_jobs:
        print(f"Successfully scraped {len(scraped_jobs)} jobs.")
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
        save_jobs_to_csv(scraped_jobs, output_path)
        notion_upload(scraped_jobs)
    else:
        print("Scraping process finished, but no jobs were returned.")
    print("------------------------\n")

if __name__ == "__main__":
    main()