# Import required libraries
import requests  # For making HTTP requests to fetch job data from a website
from bs4 import BeautifulSoup  # For parsing HTML content
import pandas as pd  # For working with data and saving it to CSV
import time  # (Imported but unused here — useful if adding delays or timing later)

# Base URL of the job listing site
BASE_URL = "https://remoteok.com"

# HTTP headers to mimic a real web browser (helps avoid blocking)
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Function to fetch job listings from the site based on a keyword (e.g., "python")
def fetch_jobs(keyword="python"):
    print(f"Fetching jobs for keyword: {keyword}")
    
    # Build the full URL to search for jobs related to the keyword
    url = f"{BASE_URL}/remote-{keyword}-jobs"
    
    # Send an HTTP GET request to the site
    response = requests.get(url, headers=HEADERS)

    # If the response is not successful, return an empty list
    if response.status_code != 200:
        print(f"Failed to fetch jobs. Status code: {response.status_code}")
        return []

    # Parse the HTML content of the response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all table rows (`tr`) with class "job" — each represents a job post
    job_elements = soup.find_all("tr", class_="job")

    jobs = []  # List to store job data

    # Loop through each job element and extract relevant details
    for job_elem in job_elements:
        try:
            # Extract job title (usually inside an <h2> tag)
            title_elem = job_elem.find("h2")
            # Extract company name (usually inside an <h3> tag)
            company_elem = job_elem.find("h3")
            # Extract the link to the job posting
            link_elem = job_elem.find("a", {"itemprop": "url"})

            # Clean and store extracted data, or default to "N/A" if not found
            title = title_elem.text.strip() if title_elem else "N/A"
            company = company_elem.text.strip() if company_elem else "N/A"
            link = BASE_URL + link_elem['href'] if link_elem else "N/A"

            # Add the job info to the jobs list as a dictionary
            jobs.append({
                "title": title,
                "company": company,
                "link": link
            })
        except Exception as e:
            # Log any errors encountered during parsing
            print("Error parsing job:", e)

    return jobs  # Return the list of job dictionaries

# Function to save job listings to a CSV file
def save_to_csv(jobs, filename="jobs.csv"):
    # Convert the job list to a pandas DataFrame
    df = pd.DataFrame(jobs)
    # Save the DataFrame to a CSV file without row numbers
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")

# Main function to run the job scraping tool
def main():
    # Prompt the user to enter a job keyword
    keyword = input("Enter a job keyword to search: ")
    # Fetch jobs related to the keyword
    jobs = fetch_jobs(keyword)
    # If jobs are found, save them to a CSV file
    if jobs:
        save_to_csv(jobs)
    else:
        print("No jobs found.")  # Inform the user if nothing was found

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
