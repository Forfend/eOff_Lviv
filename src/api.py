from flask import Flask, Response
import requests
from schedule_service import get_current_schedule
from bs4 import BeautifulSoup, NavigableString
import json
import re

app = Flask(__name__)

DATE_PATTERN = r'\d+\s+(?:січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)'
API_LVIV_URL = 'https://api.loe.lviv.ua/api/pages?page=1&synonym=power-top'

@app.route('/')
def ping():
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

    return 'pong'

@app.route('/schedule')
def get_schedule():
    print('Received request for schedule')
    # result = requests.get('https://api.loe.lviv.ua/media/669801fb33014_IMG_4807.png').content
    
    schedule = get_current_schedule()
    print('Got schedule')
    return Response(schedule, mimetype='application/json', content_type='application/json')
    # return Response(result, mimetype='image/png', content_type='image/png')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5050)