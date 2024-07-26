import io
import cv2
import numpy as np
import json

image_path = 'assets/image5.png'

groups = [
    '1.1', '1.2', 
    '2.1', '2.2',
    '3.1', '3.2'
]
hours = [
    '0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12',
    '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-0'
]

rgb_red = [252, 143, 56]
rgb_green = [151, 200, 64]


def analyze_cell_color(image, cell_region):
    x1, y1, w, h = cell_region
    x2, y2 = x1 + w, y1 + h

    cell_image = image[y1:y2, x1:x2]

    hsv_cell_image = cv2.cvtColor(cell_image, cv2.COLOR_BGR2HSV)

    # print(f'hsv_cell_image={hsv_cell_image}')

    lower_red = np.array([0, 75, 75])
    upper_red = np.array([30, 255, 255])
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    red_mask = cv2.inRange(hsv_cell_image, lower_red, upper_red)
    green_mask = cv2.inRange(hsv_cell_image, lower_green, upper_green)

    cv2.rectangle(image, (x1, y1), (x2, y2), (104, 188, 255), 2)

    # Display the image with all identified regions
    # cv2.imshow('Identified Regions', image)

    # Wait for a key press to close the window
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    red_count = np.count_nonzero(red_mask)
    green_count = np.count_nonzero(green_mask)

    if red_count > green_count:
        return 'off'
    else:
        return 'on'


def find_cell_region(image):
    # Convert to grayscale for processing
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    # equalized_image = cv2.equalizeHist(gray_image)

    # Adaptive thresholding after histogram equalization
    # thresh = cv2.adaptiveThreshold(equalized_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                cv2.THRESH_BINARY, 11, 2)

    hsv_cell_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 75, 75])
    upper_red = np.array([30, 255, 255])
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    red_mask = cv2.inRange(hsv_cell_image, lower_red, upper_red)
    green_mask = cv2.inRange(hsv_cell_image, lower_green, upper_green)

    mask = cv2.bitwise_or(red_mask, green_mask)

    countrous, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    countrous = [cnt for cnt in countrous if cv2.contourArea(cnt) > 50]

    cell_regions = [cv2.boundingRect(cnt) for cnt in countrous]

    cell_regions = sorted(cell_regions, key=lambda x: (x[1], x[0]))

    for x, y, w, h in cell_regions:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the image with all identified regions
    # cv2.imshow('Identified Regions', image)

    # Wait for a key press to close the window
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return cell_regions

def create_schedule(image_bytes):
    print('Running color analyzer using OpenCV')
    # np_bytes = np.frombuffer(image_bytes, np.uint8)
    # image = cv2.imdecode(np_bytes, cv2.IMREAD_COLOR)
    image = cv2.imread(image_path)
    img_height= image.shape[0]
    # startX, startY = 85, img_height - 220
    # width, height = 1200, 230
    # endX, endY = startX + width, startY + height

    # image = image[startY:endY, startX:endX]

    # cv2.imshow('Image', image)

    # Wait for a key press to close the window
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cell_regions = find_cell_region(image)
    # print(f'cell_regions={cell_regions}')
    # print(f'cell_regions={len(cell_regions)}')
    schedule_data = {}

    for i, group in enumerate(groups):
        group_data = {}
        for j, hour in enumerate(hours):
            cell_index = i * len(hours) + j
            # print(f'cell_index={cell_index}')
            cell_region = cell_regions[cell_index]
            status = analyze_cell_color(image, cell_region)
            group_data[hour] = status
        schedule_data[group] = group_data
    return json.dumps(schedule_data, indent=4)

if __name__ == '__main__':
    print('Running text extraction using OpenCV')
    schedule = create_schedule(image_path)
    print(schedule)
    print('Text extraction completed')
    