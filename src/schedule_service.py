import requests
from image_parse import create_schedule
import json
import re
from datetime import datetime

API_LVIV_URL_SCHEDULE_IMAGE = 'https://api.loe.lviv.ua/api/menus?page=1&type=photo-grafic'
API_LVIV_URL = 'https://api.loe.lviv.ua'


def get_current_schedule():
    urls = get_image_urls()
    headers = {'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

    print('Searching for the schedule for today ', datetime.now().strftime('%d %m %Y'))
    result = requests.get(API_LVIV_URL + urls['today'], headers=headers).content
    schedule = create_schedule(result)
    return schedule
    

def get_schedule_for_tomorrow():
    date_url = get_image_urls()

    if not date_url['tomorrow']:
        print('No schedule for tomorrow available now')
        return []
    
    print('Searching for the schedule for tommorow')
    result = requests.get(date_url[1]).content
    schedule = create_schedule(result)
    return schedule


def get_image_urls():
    headers = {'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    result = requests.get(API_LVIV_URL_SCHEDULE_IMAGE, headers=headers).content
    data = json.loads(result)
    children = currentSchedule = data[0]['menuItems'][1]['children']
    scheduleTomorow =  None
    currentSchedule = None
    for chield in children[::-1]:
        if currentSchedule:
            break
        date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', chield['name'])
        date = date_match.group() if date_match else None
        if date and datetime.strptime(date, '%d.%m.%Y') > datetime.now():
            scheduleTomorow =  chield['imageUrl']
        elif date and datetime.strptime(date, '%d.%m.%Y') < datetime.now():
            currentSchedule = chield['imageUrl']
        else:
            print('Error extracting date from response')

    date_links = {
        'today': currentSchedule,
        'tomorrow': scheduleTomorow
    }

    print(date_links)
    return date_links 
    

if __name__ == '__main__':
    get_image_urls()