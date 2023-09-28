from requests_html import HTMLSession
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Movie:
    """
    Represents movie information.
    
    Attributes:
        name (str): The name of the movie.
        release_datetime (datetime): The release date and time of the movie.
        poster_url (str): The URL of the movie poster.
        screenshots (List[str]): List of screenshot URLs.
        torrents (List[Torrent]): List of torrent data.
    """
    name: str
    release_datetime: datetime
    poster_url: str
    screenshots: List[str]
    torrents: List['Torrent']

    def __str__(self):
        return f"Movie: {self.name} (Released on: {self.release_datetime})"

@dataclass
class Torrent:
    """
    Represents torrent data.
    
    Attributes:
        file_name (str): The name of the torrent file.
        torrent_link (str): The URL to download the torrent file.
        magnet_link (str): The magnet link for the torrent.
    """
    file_name: str
    torrent_link: str
    magnet_link: str

    def __str__(self):
        return f"Torrent File: {self.file_name}"

def scrape_from_url(url: str) -> Movie:
    """
    Scrape movie information from a given URL.
    
    Args:
        url (str): The URL of the movie page to scrape.
        
    Returns:
        Movie: A Movie object containing scraped information.
    """

    session = HTMLSession()
    response = session.get(url)
    page = response.html

    # Scrape data
    name = page.find("h3")[0].text
    release_datetime_str = page.find("time")[0].attrs["datetime"]
    date_format = "%Y-%m-%dT%H:%M:%SZ"

# Convert the string to a datetime object
    release_datetime = datetime.strptime(release_datetime_str, date_format)
    img_tags = page.find("img.ipsImage")
    pics = [img.attrs["src"] for img in img_tags if img.attrs["src"].lower().split(".")[-1] in ("jpg", "jpeg", "png")]
    poster_url = pics[0] if pics else ""
    screenshots = pics[1:]

    magnet_links = [a.attrs["href"] for a in page.find("a.skyblue-button")]
    torrent_links = [a.attrs["href"] for a in page.find("a[data-fileext='torrent']")]
    file_names = [span.text.strip() for span in page.find('span[style="color:#0000ff;"]')]

    # Create Torrent objects
    torrents = [Torrent(file_name, torrent_link, magnet_link) for file_name, torrent_link, magnet_link in zip(file_names, torrent_links, magnet_links)]

    # Create and return a Movie object
    movie = Movie(name, release_datetime, poster_url, screenshots, torrents)
    return movie



if __name__ == "__main__":
    # Example usage:
    url = "https://www.1tamilmv.prof/index.php?/forums/topic/175496-kumari-srimathi-2023-s01-ep-01-07-true-web-dl-1080p-720p-x264-tamil-telugu-hindi-malayalam-39gb-16gb-900mb-esub/"
    movie_data = scrape_from_url(url)
    print(movie_data)
