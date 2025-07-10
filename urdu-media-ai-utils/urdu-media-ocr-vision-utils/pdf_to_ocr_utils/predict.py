"""
Author : M.Zeeshan Javed
Date Modified : May-11-2022
Description : This script will use the trained model to predict the text from an input image
"""

import cv2
import run_model


def do_prediction(image, model_config_path):
    """
    Author : M.Zeeshan Javed
    Date : Mar-09-2022
    Description : This function will call the necessary scripts to do prediction
    of Urdu text strip and will return the text.
    """
    print("predict.py -> do_prediction")
    encoded, predicted_text = run_model.recognize_strip(model_config_path, image)
    print("Predicted Text is:", predicted_text)


# image_path = '/home/cle-dl-05/Documents/1.OCR/2.TestOCR_LM/Test Images/file12 page134 ln10 rnk23340.jpg'
# model_config_path = '/home/cle-dl-05/Documents/1.OCR/2.TestOCR_LM/configs/CNN_RNN_CTC/MMA-UD.json'
# image = cv2.imread(image_path)
# do_prediction(image, model_config_path)
