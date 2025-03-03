import requests
from bs4 import BeautifulSoup


def scrape_latest_ipl_results(url, num_results=5):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        match_info_divs = soup.find_all('div', class_='match-info')
        results = []

        for match_info_div in match_info_divs:
            status_div = match_info_div.find('div', class_='status')
            if status_div:
                result = status_div.get_text().strip()
                results.append(result)
                if len(results) >= num_results:
                    break

        return results
    else:
        print("Failed to fetch data from the URL")
        return None


# URL of the IPL 2024 match schedule and results page
url = "https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/match-schedule-fixtures-and-results"

# Scrape the latest 5 IPL results
latest_results = scrape_latest_ipl_results(url, num_results=5)
if latest_results:
    print("Latest IPL Results:")
    for idx, result in enumerate(latest_results, start=1):
        print(f"{idx}. {result}")
else:
    print("Failed to scrape IPL results from the given URL")
