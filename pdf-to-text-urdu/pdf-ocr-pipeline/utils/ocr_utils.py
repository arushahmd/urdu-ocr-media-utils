"""
    Contains utilities to perform ocr on image, directory of images and so on.
"""

from config import ocr_output_path
from log_utils import create_log_entry
from predict_and_save import do_prediction, get_model, do_pred


def format_time(milliseconds):
    hours, rem = divmod(milliseconds, 3600000)
    minutes, rem = divmod(rem, 60000)
    seconds, ms = divmod(rem, 1000)
    time_str = ""
    if hours > 0:
        time_str += f"{int(hours)} hour" + ("s, " if hours > 1 else ", ")
    if minutes > 0:
        time_str += f"{int(minutes)} min" + ("s, " if minutes > 1 else ", ")
    if seconds > 0:
        time_str += f"{int(seconds)} sec" + ("s, " if seconds > 1 else ", ")
    time_str += f"{int(ms)} ms"
    return time_str


import os
import csv
import time
import cv2
import gc
import psutil
import tensorflow as tf

skip_files = ["Irtbat-e-Harf-o-Maani_pg8_ln2.jpg"]


def get_memory_usage():
    """Returns the by the current process and total system memory used."""
    process = psutil.Process(os.getpid())
    # Memory used by the current process (in bytes)
    current_memory = process.memory_info().rss / (1024 * 1024 * 1024)  # Convert bytes to GB
    # Total system memory used (in bytes)
    system_memory_used = psutil.virtual_memory().used / (1024 * 1024 * 1024)  # Convert bytes to GB
    return current_memory, system_memory_used


def clear_folder(folder_path):
    """Clears all files from the given folder."""
    try:
        # Iterate through all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if it is a file (and not a sub-folder)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"Skipped folder: {file_path}")

    except Exception as e:
        print(f"Error clearing folder: {e}")


def format_time(milliseconds):
    """Formats time in ms to a readable string format."""
    seconds = milliseconds / 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)}m {int(seconds)}s"


def ocr_on_images_dir(dir, tech="Updated"):
    start_time = time.time()
    start_time_str = time.strftime("%Y%m%d_%H%M%S")
    log_entry = create_log_entry(dir, process=f"OCR on Lines ({tech} Page to Line Technique)")

    log_dir = os.path.join("logs", f"ocr_log_{start_time_str}")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"OCR_Log_{start_time_str}.txt")

    with open(log_file_path, "w") as log_file:
        log_file.write(f"Process started at: {time.ctime(start_time)}\n")
        log_file.write(f"OCR Technique: {tech}\n")
        log_file.write(f"Processing directory: {dir}\n\n")

    output_path = ocr_output_path
    os.makedirs(output_path, exist_ok=True)

    output_csv = "/media/cle-nb-183/New Volume/CLE/2. Testing Data/3. analysis/1. New Technique Analysis/3. Stats/2. ip/process logs"
    csv_file = os.path.join(output_csv, "ip_colored_process_status.csv")

    processed_files = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode="r", newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                processed_files.add(row[0])

    with open(csv_file, mode="a", newline='') as file:
        writer = csv.writer(file)
        successful_count = 0
        failed_count = 0
        img_files = os.listdir(dir)
        total = len(img_files)

        try:
            with open(log_file_path, "a") as log_file:
                log_file.write("/n Memory usage : ")
            current_memory, system_memory = get_memory_usage()
            print(
                f"before loading model: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
            with open(log_file_path, "a") as log_file:
                log_file.write(
                    f"before loading model: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

            # model = get_model('configs/CNN_RNN_CTC/MMA-UD.json')

            current_memory, system_memory = get_memory_usage()
            print(
                f"after loading model: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
            with open(log_file_path, "a") as log_file:
                log_file.write(
                    f"after loading model: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

        except Exception as e:
            print(f"Failed to load model: {e}")
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Failed to load model: {e}\n")
            return

        for j in range(50):
            clear_folder("test_predictions")
            for i, file in enumerate(img_files):
                if file in skip_files:
                    continue
                file_name = file
                save_path = os.path.join(output_path, file.replace("jpg", "txt"))

                if os.path.exists(save_path):
                    print(f"{i + 1}/{total} Prediction already exists for {file}")
                    continue

                print(f"{i + 1}/{total} Processing: {file}")
                file_start_time = time.time()

                try:
                    image_path = os.path.join(dir, file)
                    current_memory, system_memory = get_memory_usage()
                    print(
                        f"before reading image: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
                    with open(log_file_path, "a") as log_file:
                        log_file.write(
                            f"before reading image: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

                    image = cv2.imread(image_path)
                    if image is None:
                        raise Exception(f"Failed to read image: {file}")

                    current_memory, system_memory = get_memory_usage()
                    print(
                        f"after reading image: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
                    with open(log_file_path, "a") as log_file:
                        log_file.write(
                            f"after reading image: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

                    if image.shape[1] <= 70 or image.shape[0] <= 10:
                        ocr_status = "Failed"
                        error_msg = f"Image dimensions too small: {image.shape}"
                        time_taken_ms = (time.time() - file_start_time) * 1000
                        writer.writerow([file_name, format_time(time_taken_ms), ocr_status, error_msg])
                        failed_count += 1
                        print(f"Failed on file {file}: {error_msg}")
                        with open(log_file_path, "a") as log_file:
                            log_file.write(f"File {file}: {error_msg}\n")
                        del image
                        gc.collect()
                        continue

                    current_memory, system_memory = get_memory_usage()
                    print(
                        f"before prediction: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
                    with open(log_file_path, "a") as log_file:
                        log_file.write(
                            f"before prediction: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

                    model = get_model('configs/CNN_RNN_CTC/MMA-UD.json')
                    prediction = do_pred(image, model)

                    current_memory, system_memory = get_memory_usage()
                    print(
                        f"after prediction: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
                    with open(log_file_path, "a") as log_file:
                        log_file.write(
                            f"after prediction: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

                    tf.keras.backend.clear_session()
                    gc.collect()

                    current_memory, system_memory = get_memory_usage()
                    print(
                        f"after clearing session: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")
                    with open(log_file_path, "a") as log_file:
                        log_file.write(
                            f"after clearing session: {current_memory:.2f} GB (Current), {system_memory:.2f} GB (System Occupied)")

                    with open(save_path, "w") as f:
                        f.write(prediction + '\n')
                    print(f"Saved prediction at: {save_path}")
                    successful_count += 1
                    ocr_status = "Success"
                    error_msg = ""

                    del image
                    del prediction
                    gc.collect()

                    time.sleep(10)

                except Exception as e:
                    print(f"Failed on file {file}: {e}")
                    failed_count += 1
                    ocr_status = "Failed"
                    error_msg = str(e)[:150]

                file_end_time = time.time()
                time_taken_ms = (file_end_time - file_start_time) * 1000
                writer.writerow([str(file_name), format_time(time_taken_ms), ocr_status, error_msg])
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"Processing {file} took {format_time(time_taken_ms)}\n")

            end_time = time.time()
            total_time = (end_time - start_time) * 1000
            print(f"Processing finished. Time taken: {format_time(total_time)}")
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Processing finished. Total time: {format_time(total_time)}\n")

            clear_folder("test_predictions")


def ocr_on_single_image(image_pth):
    image = cv2.imread(image_pth)
    cv2.imshow("demo image", image)
    cv2.waitKey(2000)
    prediction = do_prediction(image)

    print(f"Prediction : \n\t{prediction}")


if __name__ == "__main__":
    path = ("/media/cle-nb-183/New Volume/CLE/2. Testing Data/"
            "7. analysis/1. New Technique Analysis/1. lines/"
            "1. wp/Tehqiq-o-Taruf_pg118_ln16.jpg")

    # Mutala-Talmihat-o-Isharat-e-Iqbal_pg38_ln17.jpg
    # Mutala-Talmihat-o-Isharat-e-Iqbal_pg38_ln23.jpg

    ocr_on_single_image(path)
