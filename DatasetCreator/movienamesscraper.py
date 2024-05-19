import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import urllib.parse
import re
from concurrent.futures import ThreadPoolExecutor


def clean_movie_name(movie_name):
    movie_name = movie_name.replace("_", " ")
    movie_name = urllib.parse.unquote(movie_name)
    movie_name = re.sub(r'\s*\([^)]*\)', '', movie_name)
    movie_name = movie_name.replace(":", "")
    return movie_name


def get_movie_name_from_url(url):
    # Split the URL by "/"
    parts = url.split("/")
    # The movie name is usually the last part after "/wiki/"
    movie_name = parts[-1]
    movie_name = clean_movie_name(movie_name)
    return movie_name


def get_movie_plot(url):
    # Format the movie name for the Wikipedia URL
    #formatted_movie_name = movie_name.replace(' ', '_')

    # Wikipedia URL for the movie
    # url = f"https://en.wikipedia.org/wiki/{formatted_movie_name}"
    movie_name = get_movie_name_from_url(url)
    print(f"Movie Name ----{movie_name}")
    # Send a GET request to the Wikipedia page
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the plot section
        plot_section = soup.find('span', {'id': 'Plot'})
        if plot_section:
            # Find all paragraphs within the plot section until the next section starts
            plot_paragraphs = []
            next_heading = plot_section.find_next(['h2', 'h3', 'h4', 'h5', 'h6'])
            for element in plot_section.next_elements:
                if element == next_heading:
                    break
                if element.name == 'p':
                    plot_paragraphs.append(element.get_text())
            if plot_paragraphs:
                # Join paragraphs into a single string
                plot_text = ' '.join(plot_paragraphs)
                return {
                    'Title': movie_name,
                    'Story': plot_text,

                }
            else:
                return f"No plot summary found for movie {movie_name}"
        else:
            return f"Plot section not found for movie {movie_name}"
    else:
        return f"Failed to retrieve Wikipedia page for movie {movie_name}"


def get_movie_urls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table containing the list of movies
        table = soup.find('table', {'class': 'wikitable'})
        if table:
            # Extract the URLs from the first column
            rows = table.find_all('tr')[1:]
            movie_urls = [urljoin(url, row.find('td').find('a')['href']) for row in rows if row.find('td').find('a')]
            return movie_urls
        else:
            print("Table not found on", url)
            return []
    else:
        print("Failed to retrieve Wikipedia page:", url)
        return []


# List of URLs
# List of URLs for American films from 2006 to 2020


urls = [
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2006",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2007",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2008",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2009",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2010",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2011",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2012",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2013",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2014",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2015",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2016",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2017",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2018",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2019",
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2020"

]


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Story']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)



# Get the movie URLs from each URL
movie_urls_list = []
movie_data_list = []
for url in urls:
    print("Movie URLs from", url)
    movie_urls = get_movie_urls(url)

    if movie_urls:
        for movie_url in movie_urls:
            print(movie_url)
            movie_urls_list.append(movie_url)
    else:
        print("No movie URLs found for", url)
    print("------------------")

print(movie_urls_list)
for murl in movie_urls_list:
    plot = get_movie_plot(murl)
    if plot is not None:
        movie_data_list.append(plot)
        print(plot)

write_to_csv(movie_data_list, 'movie_data_2006_2020.csv')
