"""
    This is the new and better version of the news strip localizer code.
"""

import time
import cv2
import os
import tempfile
import numpy as np
import progressbar
from ultralytics import YOLO


def extract_frames(video_path):
    v_stream = cv2.VideoCapture(video_path)
    print('- Frame extraction started ...')

    frames = []
    success, image = v_stream.read()

    if not success:
        print('Error in loading the video, check the path...')
        raise SystemExit(1)

    count = 0
    while success:
        v_stream.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        frames.append([image, count])
        success, image = v_stream.read()
        count += 1

    print(f'--- Extracted {count} frames')
    return frames


def get_strip_type(y_min, image_height):
    upper_threshold = 0.20 * image_height
    lower_threshold = 0.70 * image_height

    if y_min < upper_threshold:
        return 'top'
    elif y_min > lower_threshold:
        return 'bottom'
    else:
        return 'middle'


def optimize_strip(frame, base_coordinates, strip_type):
    base_x1, base_y1, base_x2, base_y2 = base_coordinates
    cropped_image = frame[base_y1:base_y2, base_x1:base_x2]
    gray_img = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (7, 7), 0)
    _, threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    totalLabels, _, values, _ = cv2.connectedComponentsWithStats(threshold, 4, cv2.CV_32S)

    x_values, y_values = [], []

    for j in range(1, totalLabels):
        x = values[j, cv2.CC_STAT_LEFT]
        y = values[j, cv2.CC_STAT_TOP]
        x2 = x + values[j, cv2.CC_STAT_WIDTH]
        y2 = y + values[j, cv2.CC_STAT_HEIGHT]
        x_values.extend([x, x2])
        y_values.extend([y, y2])

    if x_values:
        min_x, min_y = min(x_values) + base_x1, min(y_values) + base_y1
        max_x, max_y = max(x_values) + base_x1, max(y_values) + base_y1
        optimized_image = frame[min_y:max_y, min_x:max_x]
        return [min_x, min_y, max_x, max_y, strip_type, cropped_image, optimized_image]
    else:
        print("Skipping current ...")
        return None


def locate_news_strip(frame, model):
    all_strips = []
    confidence_threshold = 0.7
    temp_image_path = os.path.join(tempfile.gettempdir(), "temp_frame.jpg")
    cv2.imwrite(temp_image_path, frame)

    prediction = model.predict(source=temp_image_path, save=False, save_txt=False, verbose=False)
    filtered_boxes = [(box, score) for box, score in zip(prediction[0].boxes.xyxy, prediction[0].boxes.conf) if score > confidence_threshold]

    for box, score in filtered_boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        strip_type = get_strip_type(y_min, frame.shape[0])
        optimized_strip = optimize_strip(frame, [x_min, y_min, x_max, y_max], strip_type)

        if optimized_strip:
            all_strips.append(optimized_strip)

    os.remove(temp_image_path)
    return all_strips


def extract_news_strips(frames, weights):
    model = YOLO(weights)
    strips = []
    total_frames = len(frames)

    with progressbar.ProgressBar(max_value=total_frames) as bar:
        for frame_no, frame in enumerate(frames):
            try:
                image, timestamp = frame
                rect_boxes = locate_news_strip(image, model)

                if rect_boxes:
                    rect_boxes[0].append(timestamp)
                    strips.append(rect_boxes[0])
                bar.update(frame_no)
            except Exception as e:
                print(f"Exception {e} occurred in extract_news_strips on frame no {frame_no}. Skipping frame!")
                continue

    return strips


def orb_sim(img1, img2):
    orb = cv2.ORB_create()
    img1, img2 = np.array(img1, dtype=np.uint8), np.array(img2, dtype=np.uint8)
    kp_a, desc_a = orb.detectAndCompute(img1, None)
    kp_b, desc_b = orb.detectAndCompute(img2, None)

    if desc_a is None or desc_b is None:
        max_height, max_width = max(img1.shape[0], img2.shape[0]), max(img1.shape[1], img2.shape[1])
        img1, img2 = cv2.resize(img1, (max_width, max_height)), cv2.resize(img2, (max_width, max_height))
        kp_a, desc_a = orb.detectAndCompute(img1, None)
        kp_b, desc_b = orb.detectAndCompute(img2, None)

    if desc_a is None or desc_b is None:
        return None

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc_a, desc_b)
    similar_regions = [i for i in matches if i.distance < 60]

    return len(similar_regions) / len(matches) if matches else 0



def differentiate_news_strips_orb(news_strips):
    uniques = []
    similar_clusters = []
    total_strips = len(news_strips)

    with progressbar.ProgressBar(max_value=total_strips) as bar:
        for i in range(total_strips - 1):
            try:
                current_strip, next_strip = news_strips[i][-3], news_strips[i + 1][-3]
                score = orb_sim(cv2.cvtColor(current_strip, cv2.COLOR_BGR2GRAY), cv2.cvtColor(next_strip, cv2.COLOR_BGR2GRAY))

                if score is not None and score < 0.80:
                    uniques.append(news_strips[i])
                    similar_clusters.append([news_strips[i]])
                else:
                    similar_clusters[-1].append(news_strips[i + 1])

                bar.update(i)
            except Exception as e:
                print(f"Error processing strip {i}: {str(e)}")
                continue

        # Handle the last strip
        if total_strips > 0:
            if not similar_clusters or news_strips[-1] not in similar_clusters[-1]:
                similar_clusters.append([news_strips[-1]])
            elif similar_clusters:
                similar_clusters[-1].append(news_strips[-1])

    # Construct final_uniques with timestamps
    final_uniques = []
    for cluster in similar_clusters:
        timestamps = [strip[-1] for strip in cluster]  # Collect timestamps
        cluster[0][-1] = timestamps  # Replace last element (timestamp) of the first strip in cluster
        final_uniques.append(cluster[0])

    # Filter out blank strips based on aspect ratio
    not_blank_strips = []
    for strip in final_uniques:
        if strip[-3].shape[0] / strip[-3].shape[1] < 0.25:
            not_blank_strips.append(strip)

    return not_blank_strips


def show_img(image):
    cv2.imshow("Image", image)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key in {ord('q'), ord('c')}:
            break
    cv2.destroyAllWindows()

