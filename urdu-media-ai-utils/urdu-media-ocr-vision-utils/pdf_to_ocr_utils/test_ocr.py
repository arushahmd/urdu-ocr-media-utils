"""
Author : M.Zeeshan Javed
Date  : May-11-2022
Description : This script will use the trained model to predict the text from all images of a directory
and save the output text in a given folder with same image name
"""
import os
import time

import cv2
import run_model


model_config_path = 'pipeline_utils/configs/CNN_RNN_CTC/MMA-UD.json'


def do_prediction(image):
    """
    Author : M.Zeeshan Javed
    Date : Mar-09-2022
    Description : This function will call the necessary scripts to do prediction
    of Urdu text strip and will return the text.
    """
    encoded, predicted_text = run_model.recognize_strip(model_config_path, image)
    return predicted_text



images_dir = '/home/cle-dl-10/Desktop/SAIM/News Channels/Geo News/Dataset 50 50 20000/Test/images/'  # Testing images dir
output_dir = '/home/cle-dl-10/Desktop/Zeeshan/2.TestOCR_LM/geo predictions new'
out_files = os.listdir(output_dir)
image_files = os.listdir(images_dir)
print("Images to test :", len(image_files))


count = 0
start_time = time.time()
# Iterating on all images one by one
for image_file in image_files:
    count += 1
    print(f"\n{count}/{len(image_files)} Working on {image_file}")
    image_path = os.path.join(images_dir, image_file)
    
    image_name = image_file.split('.jpg')[0]
    
    if image_name + '.txt' in out_files:
        print("Skipping:", image_name)
        continue
        
    # Reading image and calling function to do prediction
    # %matplotlib inline
    image = cv2.imread(image_path)
    # plt.imshow(image)
    
    tic = time.time()
    text = do_prediction(image)
    toc = time.time()
    print(f"Predicted Text : {text}")
    # print("Inferring Time :", toc - tic)
    text_file_path = os.path.join(output_dir, image_name + '.txt')
    with open(text_file_path, 'w+', encoding='utf-8') as file:
        file.write(text)
        file.close()

end_time = time
