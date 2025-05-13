import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import re
from datetime import datetime, timedelta
import os


# Function to get job links from web job page
def get_job_links(hours):
    url = "https://jobs.eu.lever.co/mobileye?lever-via=a5LsYRo7qe&lever-social=job_site"


    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    job_links = []
    current_time = datetime.now()



    pageElement = soup.find_all('a', class_='posting-title')
    if len(pageElement) == 0:
        pageElement =  soup.find_all('a', class_='positionItem')


    for job in  pageElement :
        job_url = job['href']
        job_response = requests.get(job_url)
        job_soup = BeautifulSoup(job_response.text, 'html.parser')

        # Find the script tag that contains the JSON with datePosted
        script_tag = job_soup.find('script', string=re.compile('datePosted'))
        if script_tag:
            try:
                json_text = re.search(r'{.*}', script_tag.string, re.DOTALL).group(0)
                job_data = json.loads(json_text)
                date_posted_str = job_data.get('datePosted', None)

                if date_posted_str:
                    date_posted = datetime.fromisoformat(date_posted_str.replace('Z', '+23:59'))
                    #print(f"Date posted: {date_posted}")  # Debug statement

                    # Check if the job was posted within the specified hours
                    if current_time - date_posted <= timedelta(hours=hours):
                        job_links.append(job_url)
                else:
                    print(f"No datePosted found in JSON for URL: {job_url}")
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error parsing JSON for URL: {job_url} - {e}")
                print(script_tag.string)  # Print the script content for debugging
        else:
            print(f"No datePosted JSON found for URL: {job_url}")
    print(f"Found {len(job_links)} job links in the past 24 hours")
    return job_links


def send_email(job_links):
    sender_email = os.environ.get("SENDER_EMAIL")
    to_email = sender_email
    sender_password = os.environ.get("SENDER_PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Job Links"
    message["From"] = sender_email
    message["To"] = to_email

    body = f"Found {len(job_links)} job links in the last 24 hours:\n\n"
    body += "\n".join(job_links)

    part = MIMEText(body, "plain")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())

