import easyocr
import re

def extract_date_and_time():
    schedule_date = {}
    reader = easyocr.Reader(['uk'])
    result = reader.readtext('assets/image5.png', detail=0)

    date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'
    datetime_pattern = r'\b\d{2}:\d{2} \d{2}\.\d{2}\.\d{4}\b'
    
    for text in result:
        datetime_matches = re.findall(datetime_pattern, text)
        if datetime_matches:
            for match in datetime_matches:
                schedule_date['datetime'] = match
                # print("Datetime:", match)
        else:
            # If no datetime matches, search for date pattern
            date_matches = re.findall(date_pattern, text)
            for match in date_matches:
                schedule_date['date'] = match
                # print("Date:", match)
    
    return schedule_date

if __name__ == '__main__':
    data = extract_date_and_time()
    print(data)
    print(data['date'])
    print(data['datetime'])


