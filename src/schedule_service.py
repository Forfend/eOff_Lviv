import requests
from image_parse import create_schedule
from bs4 import BeautifulSoup, NavigableString
import json
import re
from datetime import datetime

# DATE_PATTERN = r'\d+\s+(?:січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)'
API_LVIV_URL_SCHEDULE_IMAGE = 'https://api.loe.lviv.ua/api/menus?page=1&type=photo-grafic'
API_LVIV_URL = 'https://api.loe.lviv.ua'

MONTH_NUMBER_MAP = {
    '01': 'січня',
    '02': 'лютого',
    '03': 'березня',
    '04': 'квітня',
    '05': 'травня',
    '06': 'червня',
    '07': 'липня',
    '08': 'серпня',
    '09': 'вересня',
    '10': 'жовтня',
    '11': 'листопада',
    '12': 'грудня'
}

MONTH_MAP = {
    'січня': '1',
    'лютого': '2',
    'березня': '3',
    'квітня': '4',
    'травня': '5',
    'червня': '6',
    'липня': '7',
    'серпня': '8',
    'вересня': '9',
    'жовтня': '10',
    'листопада': '11',
    'грудня': '12'
}

def get_current_schedule():
    urls = get_image_urls()

    print('Searching for the schedule for today ', datetime.now().strftime('%d %m %Y'))
    result = requests.get(API_LVIV_URL + urls['today']).content
    schedule = create_schedule(result)
    return schedule
    

def get_schedule_for_tomorrow():
    date_url = get_image_urls()

    if not date_url['tomorrow']:
        print('No schedule for tomorrow available now')
        return []
    
    print('Searching for the schedule on date =', parsed_date)
    result = requests.get(date_url[1]).content
    schedule = create_schedule(result)
    return schedule


def get_image_urls():
    result = requests.get(API_LVIV_URL_SCHEDULE_IMAGE).content
    data = json.loads(result)
    contentToday = data['hydra:member'][0]['menuItems'][0]['imageUrl']
    # soup = BeautifulSoup(content, 'html.parser')
    contentTomorrow = data['hydra:member'][0]['menuItems'][2]['imageUrl']
    
    # print(contentTomorrow)
    date_links = {
        'today': contentToday,
        'tomorrow': contentTomorrow
    }

    print(date_links)
    return date_links 
    

if __name__ == '__main__':
    get_image_urls()