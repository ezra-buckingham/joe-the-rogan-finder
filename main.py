import requests
import click
from bs4 import BeautifulSoup
from pathlib import Path
import json

def send_notification(webhook_url, message):
    
    data = {
        'content': message
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response


@click.command()
@click.option('-d', '--date', required=True, help='''
    Date to check for on the website (ex. "Monday, Oct 23")
''')
@click.option('-u', '--url', required=True, help='''
    Discord URL to notify when found
''')
def cli(date, url):
    
    # Create the path for the file to create if there was already a found item
    found_file = Path('/tmp/joe-found')
    if found_file.exists(): exit()
    
    # Send a GET request to the website
    url = 'https://comedymothership.com/shows'
    response = requests.get(url)
    html = response.text

    # Parse the HTML and extract the date
    soup = BeautifulSoup(html, 'html.parser')
    date_elements = soup.findAll('div', class_='h6')
    
    for current_date in date_elements:
        current_date = current_date.text.strip()
        if not current_date == date: continue
        message = f'The date "{date}" was found on Joe Rogan\'s website!'
        send_notification(url, message)
        found_file.touch()


if __name__ == "__main__":
    cli()