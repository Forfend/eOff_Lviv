import requests
from image_parse import create_schedule
from bs4 import BeautifulSoup, NavigableString
import json
import re

DATE_PATTERN = r'\d+\s+(?:січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)'
API_LVIV_URL = 'https://api.loe.lviv.ua/api/pages?page=1&synonym=power-top'

def get_current_schedule():
    urls = get_image_urls()
    print('Searching for the schedule on date =', urls[0][0])
    result = requests.get(urls[0][1]).content
    schedule = create_schedule(result) #replace None with the image response from the API
    return schedule


def get_image_urls():
    result = requests.get(API_LVIV_URL).content
    data = json.loads(result)
    content = data['hydra:member'][0]['content']
    soup = BeautifulSoup(content, 'html.parser')

    date_links = []
    current_date = None

    for element in soup.descendants:
        if isinstance(element, NavigableString):
            if current_date is None:  # Look for a date if we don't have one yet
                date_match = re.search(DATE_PATTERN, element)
                if date_match:
                    current_date = date_match.group()
            continue

        if element.name == 'img' and current_date is not None:  # Found an img tag after a date
            img_url = element['src']
            date_links.append((current_date, img_url))
            current_date = None

    for date, img_url in date_links:
        print(f"Date: {date}, Image URL: {img_url}")

    return date_links 