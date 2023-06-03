import requests
import click
from bs4 import BeautifulSoup
from pathlib import Path
import json

COUNT_THRESHOLD = 3

def send_notification(webhook_url, message):
    
    data = {
        'content': message
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response


def get_count_from_found_joe(path):
    path = Path(path)
    if not path.exists(): raise FileNotFoundError(f'File not found at { str(path.absolute()) }')
    return int(path.read_text())


def add_count_to_found_joe(path):
    # Get the current count from the file
    path = Path(path)
    path_contents = path.read_text()
    if len(path_contents) == 0: current_count = 1
    else: current_count = int(path_contents)
    
    # Delete the file
    path.unlink()
    
    # Create the file and add the updated count
    path.touch()
    path.write_text(str(current_count + 1))
    

@click.command()
@click.option('-d', '--date', required=False, default=None, help='''
    Date to check for on the website (ex. "Monday, Oct 23")
''')
@click.option('-d', '--date_file', required=False, default=None, help='''
    A file containing the dates to check for
''')
@click.option('-u', '--url', required=True, help='''
    Discord URL to notify when found
''')
def cli(date, date_file, url):
    
    # Create the path for the file to create if there was already a found item
    found_file = Path(__file__).joinpath('joe-found')
    if found_file.exists(): 
        count = get_count_from_found_joe(found_file)
        if count >= COUNT_THRESHOLD: exit()
    
    # Create the dates to check for array
    dates_to_check = []
    
    # Add the dates to the array
    if date_file:
        date_file = Path(date_file)
        if not date_file.exists(): raise FileNotFoundError(f'File not found at { str(date_file.absolute()) }')
        dates_to_check = date_file.read_text().splitlines()
    if date:
        dates_to_check.append(date)

    # Send a GET request to the website
    url = 'https://comedymothership.com/shows'
    response = requests.get(url)
    html = response.text

    # Parse the HTML and extract the date
    soup = BeautifulSoup(html, 'html.parser')
    date_elements = soup.findAll('div', class_='h6')
    
    for current_date in date_elements:
        current_date = current_date.text.strip()
        if not current_date in dates_to_check: continue
        message = f'The date "{date}" was found on Joe Rogan\'s website!'
        send_notification(url, message)
        add_count_to_found_joe(found_file)


if __name__ == "__main__":
    cli()