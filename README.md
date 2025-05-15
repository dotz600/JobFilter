# 📬 Daily Job Notifier via Google Cloud Functions

A serverless solution that monitors job listings, filters by posting date, and delivers daily email notifications with new opportunities.

## 🚀 Overview

This project automatically scrapes job listings (currently configured for Mobileye's Lever page), identifies positions posted within the last 24 hours, and sends a concise email summary with direct links to apply. The entire workflow runs as a **Google Cloud Function** triggered daily by **Google Cloud Scheduler**.

---

## ✨ Key Features

- 🕸️ **Intelligent Scraping**: Extracts job listings from target websites
- ⏱️ **Time-Based Filtering**: Shows only positions posted within the last 24 hours
- 📊 **Smart Summarization**: Organizes job listings by category for easy scanning
- 📧 **Automated Notifications**: Delivers results via email using Gmail SMTP
- ☁️ **Serverless Architecture**: Runs on Google Cloud with zero infrastructure management
- 🔐 **Secure Credential Handling**: Protects sensitive information via environment variables

---

## 🛠️ Technology Stack

- **Runtime**: Python 3.12
- **Cloud Services**: 
  - Google Cloud Functions (serverless execution)
  - Google Cloud Scheduler (time-based triggering)
- **Email Delivery**: Gmail SMTP with App Password
- **Data Processing**:
  - BeautifulSoup4 (HTML parsing)
  - Requests (HTTP client)

---

## 📁 Project Structure

```
.
├── main.py            # Cloud Function entry point 
├── job_filter_GCP.py  # Cloud Function core logic
├── requirements.txt   # Python dependencies
└── README.md          # Documentation
```

---

## 🚀 Setup & Deployment Guide

### Prerequisites

- Google Cloud Platform account
- Gmail account with 2-Step Verification enabled
- Google Cloud CLI installed locally

### 1. Clone the Repository

```bash
git clone https://github.com/dotz600/JobFilter/.git
cd job-notifier
```

### 2. Local Development & Testing

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test locally
python main.py
```

### 3. Google Cloud Function Deployment

```bash
gcloud functions deploy job-notify \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point job_notify \
  --set-env-vars SENDER_EMAIL="your_email@gmail.com",SENDER_PASSWORD="your_app_password",RECIPIENT_EMAIL="destination@example.com" \
  --region=us-central1
```

> **Note**: Replace placeholder email addresses and password with your actual values.

### 4. Configure Daily Trigger with Cloud Scheduler

```bash
gcloud scheduler jobs create http job-notify-daily \
  --schedule="0 15 * * *" \
  --http-method=GET \
  --uri=https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/job-notify \
  --time-zone="Asia/Jerusalem" \
  --location=us-central1
```

> **Important**: Replace the URI with your actual Cloud Function URL displayed after deployment.

---

## 📧 Gmail Configuration

To enable email notifications, you'll need to create an App Password:

1. Ensure 2-Step Verification is enabled on your Google Account
2. Visit [Google Account Security](https://myaccount.google.com/security)
3. Under "Signing in to Google," select "App Passwords"
4. Generate a new password for "Mail"
5. Use this generated password in your `SENDER_PASSWORD` environment variable

---

## 🔍 Monitoring & Troubleshooting

- **Cloud Function Logs**: 
  - Navigate to [Cloud Logging](https://console.cloud.google.com/logs) in GCP
  - Filter for your function name to view execution logs

- **Common Issues**:
  - Email delivery failures: Verify SMTP credentials and recipient address
  - Scraping errors: Check if target website structure has changed
  - Timeout errors: Consider optimizing the scraping process

---

## 🛠️ Customization Options

To adapt this tool for different job sites:

1. Modify the scraping logic in `main.py` to target your desired website
2. Adjust the HTML parsing to match the structure of the new target site
3. Update the time filter logic if needed (currently set to 24 hours)
4. Run Locally Using Selenium, to handle dynamic content (e.g., JavaScript-rendered job listings), you can replace requests + BeautifulSoup with Selenium:
---

