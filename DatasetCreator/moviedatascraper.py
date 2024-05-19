import requests
from bs4 import BeautifulSoup
import csv

def scrape_movie_data(movie_title):
    # Construct Wikipedia URL
    wikipedia_url = f"https://en.wikipedia.org/wiki/{movie_title.replace(' ', '_')}"

    # Send a GET request to Wikipedia
    response = requests.get(wikipedia_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the plot section
        plot_section = soup.find('span', {'id': 'Plot'})
        if not plot_section:
            plot_section = soup.find('span', {'id': 'Plot_summary'})
        if not plot_section:
            plot_section = soup.find('span', {'id': 'Story'})

        if plot_section:
            plot_paragraphs = plot_section.find_next_siblings('p')
            plot = ' '.join([p.text for p in plot_paragraphs])

            # Find the title of the movie
            title = soup.find('h1', {'id': 'firstHeading'}).text

            # Find the genre of the movie
            genre = "TBD"

            return {
                'Title': title,
                'Story': plot.text if plot else 'N/A',
                'Genre': genre if genre else 'N/A'
            }
        else:
            return None
    else:
        return {
            'Title': movie_title,
            'Story': 'Failed to fetch data from Wikipedia',
            'Genre': 'N/A'
        }


def get_movie_plot(url):
    # Format the movie name for the Wikipedia URL
    #formatted_movie_name = movie_name.replace(' ', '_')

    # Wikipedia URL for the movie
   # url = f"https://en.wikipedia.org/wiki/{formatted_movie_name}"

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
                return plot_text
            else:
                return f"No plot summary found for movie {movie_name}"
        else:
            return f"Plot section not found for movie {movie_name}"
    else:
        return f"Failed to retrieve Wikipedia page for movie {movie_name}"



def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Story', 'Genre']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)
if __name__ == "__main__":
    movies = [
        "Dangal",
        "Baahubali 2: The Conclusion",
        "RRR",
        "KGF: Chapter 2",
        "Jawan",
        "Pathaan",
        "Bajrangi Bhaijaan",
        "Animal",
        "Secret Superstar",
        "PK",
        "Salaar: Part 1 – Ceasefire",
        "2.0",
        "Gadar 2",
        "Sultan",
        "Jailer",
        "Leo",
        "Baahubali: The Beginning",
        "Sanju",
        "Padmaavat",
        "Tiger Zinda Hai",
        "Dhoom 3",
        "War",
        "Tiger 3",
        "Dunki",
        "Andhadhun",
        "Ponniyin Selvan: I",
        "Vikram",
        "Saaho",
        "Brahmāstra: Part One – Shiva",
        "Simmba",
        "3 Idiots",
        "Chennai Express",
        "Kantara",
        "Krrish 3",
        "Kabir Singh",
        "Dilwale",
        "Tanhaji",
        "Prem Ratan Dhan Payo",
        "Pushpa: The Rise",
        "Bajirao Mastani",
        "Rocky Aur Rani Kii Prem Kahaani",
        "Adipurush",
        "Kick",
        "Happy New Year",
        "Ponniyin Selvan: II",
        "Hanu-Man",
        "Drishyam 2",
        "Uri: The Surgical Strike",
        "The Kashmir Files",
        "Fighter"
    ]

    movie_data_list = []

    print(movies)
    for movie in movies:
        movie_data = get_movie_plot(movie)
        if movie_data is not None:
            movie_data_list.append(movie_data)
            print(movie_data)
    write_to_csv(movie_data_list, 'movie_data2.csv')
