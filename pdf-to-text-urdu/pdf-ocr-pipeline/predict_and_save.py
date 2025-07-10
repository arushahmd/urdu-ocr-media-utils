"""
    Predict and Save the image strip prediction.
"""

import os
import cv2
from . import run_model


def get_model(model_config_path):
    model, config= run_model.create_and_run_model(model_config_path)
    return model


def do_pred(image, model):
    out, urdu_out = model(image)

    predicted_text = urdu_out[0]

    return predicted_text


def do_prediction(image):
    """
    Author : M.Zeeshan Javed
    Date : Mar-09-2022
    Description : This function will call the necessary scripts to do prediction
    of Urdu text strip and will return the text.

    :param image: Input image for recognition
    :param model_config_path: Path to config file of model CNN_RNN_CTC/MMA-UD.json can be found in config folder
    :param channel_name: The channel name of the video strip so that respective model is called
    :return:

    """
    # cv2.imshow("Image for prediction", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # encoded, predicted_text = run_model.recognize_strip(model_config_path, image)
    model = get_model('pdf_ocr_pipeline/configs/CNN_RNN_CTC/MMA-UD.json')
    out, urdu_out = model(image)

    predicted_text = urdu_out[0]

    return predicted_text


def bulk_predictions(input_path):
    """
    Process images from a directory or a single image, predict text, and save results to text files.

    Args:
        input_path (str): Path to a single image or directory containing images.
        model (callable): The model used for prediction.
    """

    output_dir = "output/book_text_predictions"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    predictions = {}

    if os.path.isfile(input_path):
        # Process single image
        img_pth = input_path
        img_name = os.path.splitext(os.path.basename(img_pth))[0]
        print(f"Processing single image: {img_pth}")

        image = cv2.imread(img_pth)
        if image is None:
            print(f"Error reading image {img_pth}. Skipping.")
            return

        predicted_text = do_prediction(image)
        predictions[img_name] = predicted_text

    elif os.path.isdir(input_path):
        # Process all images in the directory
        print(f"Processing directory: {input_path}")
        for img_file in os.listdir(input_path):
            if img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
                img_pth = os.path.join(input_path, img_file)
                img_name = os.path.splitext(img_file)[0]

                print(f"Processing image: {img_pth}")
                image = cv2.imread(img_pth)
                if image is None:
                    print(f"Error reading image {img_pth}. Skipping.")
                    continue

                predicted_text = do_prediction(image)
                predictions[img_name] = predicted_text

    else:
        raise ValueError("Provided path is neither a file nor a directory.")

    # Organize and save predictions
    for img_name, text in predictions.items():
        # Parse img_name to extract page and line numbers
        parts = img_name.split('_')
        if len(parts) >= 3:
            book_name = parts[0]
            page_info = parts[1]
            line_info = parts[2]

            # Format for text file
            output_file = os.path.join(output_dir, f"{book_name}.txt")

            # Append to file
            with open(output_file, 'a', encoding="utf-8") as file:
                page_number = page_info.split('pg')[1]
                line_number = line_info.split('ln')[1]
                file.write(f"Page{page_number} Line{line_number}: {text}\n")
            print(f"Appended predictions to {output_file}")


