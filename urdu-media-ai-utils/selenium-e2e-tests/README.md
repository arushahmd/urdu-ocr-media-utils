# Selenium-Based Multi-User Testing 

## Project Overview

This project tests **Urdu Multimedia multi-user support and functionality** using Selenium-based automation. It simulates real-world usage where **multiple users log in simultaneously** and interact with different services in parallel.

The core scripts reside in the `multiple_reports_testing/` folder. Additional scripts for testing individual services (e.g., Signup, Audio Transcription) are organized separately in the `individual_service_tests/` folder.

---

## Folder Structure

```
    selenium-testing/
    ├── multiple-report-testing/
    │ ├── config.py # URL and configuration settings
    │ ├── utils.py # Common utility functions (e.g., sign in)
    │ ├── report_testing.py # Runs parallel tests for each module
    │ ├── results/ # CSV logs of test results (pass/fail)
    │
    ├── individual-report-tests/
    │ ├── signup.py # Tests the signup functionality
    │ ├── sudioTranscription.py # Single-user test for Audio Transcription
    │ ├── multiuser_audio_transcription.py # Simulates multiple users for audio transcription
    │
    ├── credentials.json # Username/password pairs for test logins
    ├── user_queries.sql # Dummy data SQL for user roles/emails
    ├── downloadlog.sql # SQL logs of download and interaction events
```
---

## Services Tested

This suite verifies both **UI rendering** and **backend response** across these  modules:

- Sign In
- Sign Up
- Audio Transcription
- Subtitle Generation
- Keyword-Based Search
- Speaker-Based Search
- News Ticker Analysis
- Trending Topics Extraction

---

## How It Works

1. **Multiple users log in concurrently.**
2. Each accesses a different service, using Selenium automation.
3. System behavior (response time, errors, etc.) is recorded.
4. Results are saved in `.csv` under the `results/` folder.

---

## Test Coverage

| Test Area                     | Tool/Script                        | Notes                                      |
|------------------------------|------------------------------------|--------------------------------------------|
| Multi-user simulation        | `report_testing.py`                | Main test script                           |
| Login, Service Testing       | `utils.py`, `config.py`            | Shared utilities                           |
| Signup                       | `Signup.py`                        | Single-service test                        |
| Audio Transcription (load)   | `multiuser_audio_transcription.py` | Simulates concurrency                      |
| Test accounts & logs         | `credentials.json`, `user_queries.sql` | Used for consistent test setup         |

---

## Notes

- Tests use Selenium WebDriver (Chrome recommended).
- Ensure test accounts and URLs are correctly configured in `config.py` and `credentials.json`.
- CSV output in `results/` helps evaluate pass/fail rate, latency, and module health.

---

