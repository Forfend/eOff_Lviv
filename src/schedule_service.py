import requests
from image_parse import create_schedule
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_LVIV_URL_SCHEDULE_IMAGE = 'https://api.loe.lviv.ua/api/menus?page=1&type=photo-grafic'
API_LVIV_URL = 'https://api.loe.lviv.ua'
HEADERS = {'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

def get_current_schedule():
    urls = get_image_urls()

    logger.info('Searching for the schedule for today ' + datetime.now().strftime('%d %m %Y'))
    result = requests.get(API_LVIV_URL + urls['today'], headers=HEADERS).content
    schedule = create_schedule(result)
    return schedule
    

def get_schedule_for_tomorrow():
    date_url = get_image_urls()

    if not date_url['tomorrow']:
        logger.info('No schedule for tomorrow available now')
        return []
    
    logger.info('Searching for the schedule for tommorow')
    result = requests.get(API_LVIV_URL + date_url['tomorrow'], headers=HEADERS).content
    schedule = create_schedule(result)
    return schedule


def get_image_urls():
    headers = {'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    result = requests.get(API_LVIV_URL_SCHEDULE_IMAGE, headers=headers).content
    headers = {'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    result = requests.get(API_LVIV_URL_SCHEDULE_IMAGE, headers=headers).content
    data = json.loads(result)
    currentSchedule = data[0]['menuItems'][0]['imageUrl']
    scheduleTomorow =  data[0]['menuItems'][2]['imageUrl']

    date_links = {
        'today': currentSchedule,
        'tomorrow': scheduleTomorow
    }

    logger.debug(date_links)
    return date_links 
    

if __name__ == '__main__':
    get_image_urls()