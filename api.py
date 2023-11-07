from selenium import webdriver
import pickle
import time
from bs4 import BeautifulSoup
import re
import json
from selenium.webdriver.chrome.options import Options
import requests

def linenotify(message):
    # URL to the Line Notify API
    url = "https://notify-api.line.me/api/notify"

    # Set up the headers with your token
    headers = {
        "Authorization": f"Bearer fErW5Gnze4MNyNvbQ7FrbKjJQOFBXJTQCs0lfTmoXvG"
    }

    # Set up the payload with the message
    payload = {
        "message": message
    }

    # Send the POST request to Line Notify
    response = requests.post(url, headers=headers, data=payload)

    # Check the response status
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print(f"Notification failed with status code: {response.status_code}")

# Initialize WebDriver (using Chrome in this example)
chrome_options = Options()

# Disable notifications
chrome_options.add_argument("--disable-notifications")

# Create WebDriver with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Open Facebook homepage
driver.get("https://www.facebook.com")

# Load cookies from file
with open("facebook_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)

# List of group IDs
group_ids =["626070986239323","308348996227047","826481480835774","1723939091272863","1524964741086428"]

while True:
    # Iterate through each group
    
    for group_id in group_ids:
        target_url = f"https://www.facebook.com/groups/{group_id}"

        # Visit the Facebook group search page
        driver.get(f"{target_url}/search/?q=ห้องว่าง")

        # Execute JavaScript to zoom out the page (adjust zoom level as needed)
        driver.execute_script("document.body.style.zoom='0.1'")

        time.sleep(15)  # Wait for the page to load

        # Get the page source and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find message divs
        div_tags = soup.find_all('div', {'data-ad-comet-preview': 'message', 'data-ad-preview': 'message'})
        text_content = ""

        matching_links = []
        data_array = []

        # Find links to individual posts in the group
        links = soup.find_all('a', href=True)
        for link in links:
            if target_url in link['href']:
                matching_links.append(f"{target_url}/posts/{str(link['href']).split('/posts/')[-1].split('/')[0]}/")
        # if len(matching_links) >= len(div_tags):
        for i, div_tag in enumerate(div_tags):
                try:
                    text_content = div_tag.get_text()
                    data = {"content": str(text_content).replace(" ", "").replace("\n", ""), "link": matching_links[i]}
                    data_array.append(data)
                except:
                    pass
        else:
            print("Number of matching links is less than expected.")
        with open(f"web/output_{group_id}.json", "r", encoding="utf-8") as json_file:
            old = json.load(json_file)
        if (old[0] != data_array[0] and old[0] is not None):
            print("มีโพสใหม่")
            
        
        with open(f"web/output_{group_id}.json", "w", encoding="utf-8") as json_file:
            json.dump(data_array, json_file, ensure_ascii=False, indent=4)

        # Wait for 2 minutes before repeating the process
    time.sleep(120)
