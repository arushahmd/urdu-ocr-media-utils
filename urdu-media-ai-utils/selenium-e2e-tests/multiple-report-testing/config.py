# Configuration file for Selenium multi-user testing

# ---------------------------
# URLs
# ---------------------------
login_url = "http://127.0.0.1:8000/login/"
generate_report_dashboard_url = "http://127.0.0.1:8000/reports_manager/report_dashboard/"

# ---------------------------
# Folder Paths
# ---------------------------
temp_folder = "TEMP"  # Folder to store temporary files (if any)

# ---------------------------
# Timing Settings (in seconds)
# ---------------------------
elemental_wait = 2     # Wait after locating or interacting with an element
result_wait = 3        # Wait after submitting a form to receive results
sleep_wait = 2         # Sleep between user actions to simulate human interaction
timeout = 5            # Max wait time before timing out on any action

# ---------------------------
# User Simulation Settings
# ---------------------------
prefix = 'guest'       # Email prefix (e.g., guest1@gmail.com, guest2@gmail.com, ...)
no_users = 50          # Total number of simulated users for concurrent testing
