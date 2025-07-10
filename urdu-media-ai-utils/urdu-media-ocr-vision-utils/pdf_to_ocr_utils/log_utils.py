import csv
import os
from datetime import datetime

# Set the log file path
log_file_path = "output/log/log.csv"

def initialize_csv():
    """
    Initialize the CSV with headers at the fixed log file path.
    If the log directory does not exist, create it.
    Only create the CSV file if it does not already exist.
    """
    log_dir = os.path.dirname(log_file_path)

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create and initialize the CSV if it does not already exist
    if not os.path.exists(log_file_path):
        with open(log_file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["date", "file_name", "file_path", "process", "start_time", "end_time", "duration","details",
                                                "error", "status"])
            writer.writeheader()

def create_log_entry(file_path, process, details="", error="", status="In Progress"):
    """
    Create a log entry for a given process.
    """
    start_time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().strftime("%d-%m-%Y")  # Add date field
    max_error_length = 100  # Define a maximum length for error messages
    if len(error) > max_error_length:
        error = error[:max_error_length] + "..."  # Truncate error message if it's too long

    return {
        "date": date,
        "file_name": file_path.split("/")[-1],
        "file_path": file_path,
        "process": process,
        "start_time": start_time,
        "end_time": "",
        "duration": "",
        "details": details,
        "error": error,
        "status": status
    }


def format_duration(start_time, end_time):
    """
    Format the duration between start_time and end_time as hours, minutes, and seconds.
    """
    delta = end_time - start_time
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Return the duration in "X hours, Y minutes, Z seconds" format
    return f"{hours} hours, {minutes} minutes, {seconds} seconds"

def update_log_entry(log_entry):
    """
    Update the log entry by writing it to the CSV if the status is "Success" or "Failed".
    """
    if log_entry["status"] in ["Success", "Failed"]:
        log_entry["end_time"] = datetime.now().strftime("%H:%M:%S")
        start_time = datetime.strptime(log_entry["start_time"], "%H:%M:%S")
        end_time = datetime.strptime(log_entry["end_time"], "%H:%M:%S")
        log_entry["duration"] = format_duration(start_time, end_time)

        # Open the file in append mode to add new entries without modifying existing content
        with open(log_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["date", "file_name", "file_path", "process", "start_time", "end_time",
                                                "duration", "details",
                                                "error", "status"])
            writer.writerow(log_entry)
