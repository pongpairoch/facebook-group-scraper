from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle

# Initialize WebDriver (using Chrome in this example)
driver = webdriver.Chrome()

# Navigate to Facebook login page
driver.get("https://www.facebook.com")

# Find the email and password fields, and input your credentials
email_input = driver.find_element(By.ID, "email")
password_input = driver.find_element(By.ID, "pass")

email = "pongpairoch.pongpairoch@gmail.com"
password = "0880831674Oat_"

email_input.send_keys(email)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Wait for the user to interact and log in manually if needed
input("Please log in manually and press Enter after logging in...")

# Save cookies to a file
cookies = driver.get_cookies()
with open("facebook_cookies.pkl", "wb") as f:
    pickle.dump(cookies, f)

# Close the browser
driver.quit()
