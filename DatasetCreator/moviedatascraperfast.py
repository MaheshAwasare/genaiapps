import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import urllib.parse
import re
from concurrent.futures import ThreadPoolExecutor

# Logging config for this file
logging.basicConfig(filename='movie_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def clean_movie_name(movie_name):
    movie_name = movie_name.replace("_", " ")
    movie_name = urllib.parse.unquote(movie_name)
    movie_name = re.sub(r'\s*\([^)]*\)', '', movie_name)
    movie_name = movie_name.replace(":", "")
    return movie_name


def get_movie_name_from_url(url):
    parts = url.split("/")
    movie_name = parts[-1]
    movie_name = clean_movie_name(movie_name)
    return movie_name


def get_movie_plot(url):
    movie_name = get_movie_name_from_url(url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        plot_section = soup.find('span', {'id': 'Plot'})
        if plot_section:
            plot_paragraphs = []
            next_heading = plot_section.find_next(['h2', 'h3', 'h4', 'h5', 'h6'])
            for element in plot_section.next_elements:
                if element == next_heading:
                    break
                if element.name == 'p':
                    plot_paragraphs.append(element.get_text())
            if plot_paragraphs:
                plot_text = ' '.join(plot_paragraphs)
                return {
                    'Title': movie_name,
                    'Story': plot_text,
                }
            else:
                logging.warning(f"No plot summary found for movie {movie_name}")
        else:
            logging.warning(f"Plot section not found for movie {movie_name}")
    else:
        logging.error(f"Failed to retrieve Wikipedia page for movie {movie_name}")


def get_movie_urls(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        if table:
            rows = table.find_all('tr')[1:]
            movie_urls = [urljoin(url, row.find('td').find('a')['href']) for row in rows if row.find('td').find('a')]
            return movie_urls
        else:
            logging.error("Table not found on %s", url)
            return []
    else:
        logging.error("Failed to retrieve Wikipedia page: %s", url)
        return []


def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Story']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def fetch_movie_plots(movie_urls_list):
    movie_data_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        plots = list(executor.map(get_movie_plot, movie_urls_list))
    for plot in plots:
        if plot is not None:
            movie_data_list.append(plot)
            logging.info(plot)
    logging.info(movie_data_list)
    write_to_csv(movie_data_list, 'movie_data_2006_2019.csv')


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
    "https://en.wikipedia.org/wiki/List_of_American_films_of_2019"
]

movie_urls_list = []
for url in urls:
    movie_urls = get_movie_urls(url)
    if movie_urls:
        for movie_url in movie_urls:
            logging.info(movie_url)
            movie_urls_list.append(movie_url)
    else:
        logging.error("No movie URLs found for %s", url)

fetch_movie_plots(movie_urls_list)
