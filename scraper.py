import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://remoteok.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_jobs(keyword="python"):
    print(f"Fetching jobs for keyword: {keyword}")
    url = f"{BASE_URL}/remote-{keyword}-jobs"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch jobs. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    job_elements = soup.find_all("tr", class_="job")

    jobs = []
    for job_elem in job_elements:
        try:
            title_elem = job_elem.find("h2")
            company_elem = job_elem.find("h3")
            link_elem = job_elem.find("a", {"itemprop": "url"})

            title = title_elem.text.strip() if title_elem else "N/A"
            company = company_elem.text.strip() if company_elem else "N/A"
            link = BASE_URL + link_elem['href'] if link_elem else "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "link": link
            })
        except Exception as e:
            print("Error parsing job:", e)

    return jobs


def save_to_csv(jobs, filename="jobs.csv"):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Saved {len(jobs)} jobs to {filename}")


def main():
    keyword = input("Enter a job keyword to search: ")
    jobs = fetch_jobs(keyword)
    if jobs:
        save_to_csv(jobs)
    else:
        print("No jobs found.")


if __name__ == "__main__":
    main()
