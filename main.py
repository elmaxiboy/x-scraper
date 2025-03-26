import argparse
from datetime import datetime, timedelta
import logging
import re
import time
from urllib.parse import quote_plus
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import os
from dotenv import load_dotenv

# Initialize WebDriver globally
driver = None

#Initialize environment variables
load_dotenv()

# Dictionary with useful fields for Solana-related tweets
search_params = {
    'queries': ['solana', '#solana', 'solana crypto'],  # List of main queries or hashtags
    'hashtags': ['#solana', '#cryptocurrency'],  # List of hashtags to track
    'langs': ['en', 'es'],  # List of languages
    'types': ['live', 'top']  # Types of tweets (e.g., 'live', 'top')
}

tweets_data = {"tweets": []}

def get_new_height(driver,last_tweet):

    driver.execute_script("arguments[0].scrollIntoView();", last_tweet)

    for _ in range(50):  # Simulate a user scrolling gradually
        #driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(0.2) 

    
    new_height = driver.execute_script("return document.body.scrollHeight")

    logging.debug("New height is: {}",new_height)

    return new_height

def init_web_driver():
    
    global driver

    # Configure Selenium WebDriver
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--user-agent={}".format("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"))
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Initialize WebDriver
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    driver.maximize_window()

def take_screenshot(step):
    
    global driver 

    os.makedirs("screenshots/",exist_ok=True)

    login_window=driver.get_full_page_screenshot_as_png()

    with open("screenshots/"+str(step)+".png", 'wb') as file:
            file.write(login_window)      

def two_factor_authentication():

    global driver

    try:
        
        verification_code = input("🔑 Enter the verification code sent to your Auth App: ") 

        twofactor = driver.find_element("xpath", "//input[@autocomplete='on']")
        twofactor.send_keys(verification_code)
        twofactor.send_keys(Keys.RETURN)
        time.sleep(5)

    except Exception as e:
        logging.warning(f"Unable to type 2FA code: {e}")
        raise(e)
    

def login():
     
    global driver 

    try:

        driver.get('https://x.com/i/flow/login')
        time.sleep(5)
        
        username = driver.find_element("xpath", "//input[@autocomplete='username']")
        username.send_keys(os.getenv('USERNAME'))
        username.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
           driver.find_element("xpath", "//span[contains(text(), 'please enter your phone number')]")
           phone_or_email= driver.find_element("xpath", "//input[@data-testid='ocfEnterTextTextInput']")
           phone_or_email.send_keys(os.getenv('EMAIL'))
           phone_or_email.send_keys(Keys.RETURN)
           time.sleep(5)

        except NoSuchElementException as e:
            pass   

        password = driver.find_element("xpath", "//input[@autocomplete='current-password']")
        password.send_keys(os.getenv('PASSWORD'))
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        two_factor_authentication()

        handle_cookies()
        
        logging.info("Login succeeded!")

    except Exception as e:
        logging.error(f"Error logging in, you might check the screenshots for any clue: {e}")
        take_screenshot("error_login")
        raise(e)
    


def handle_cookies():

    global driver
    
    try:
            
        cookies_banner = driver.find_element("xpath", "//span[text()='Refuse non-essential cookies']/../../..")    
        cookies_banner.click()

    except NoSuchElementException:
            pass
    
    try:
         
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie["name"] == "auth_token":
                break    
    except Exception as e:
         raise(e)


def get_dynamic_dates():
    # Get today's date
    today = datetime.today()
    # Get the date 7 days ago
    seven_days_ago = today - timedelta(days=7)
    
    # Format both dates in YYYY-MM-DD format
    until_date = today.strftime('%Y-%m-%d')
    since_date = seven_days_ago.strftime('%Y-%m-%d')
    
    return since_date, until_date


# Function to generate the URL for the search with dynamic dates
def generate_search_url(params):

    base_url = "https://x.com/search?q="
    
    since_date, until_date = get_dynamic_dates()
    
    query_parts = []
    
    # Combine multiple queries and hashtags
    for query in params['queries']:
        query_parts.append(quote_plus(query))
    
    for hashtag in params['hashtags']:
        query_parts.append(f"({quote_plus(hashtag)})")
    
    query_str = " ".join(query_parts) + f"%20until%3A{quote_plus(until_date)}%20since%3A{quote_plus(since_date)}"
    
    lang = params['langs'][0]
    tweet_type = params['types'][0]
    
   
    query_str += f"&lang={lang}&src=typed_query&f={tweet_type}"
    
    return base_url + query_str


def scrape_x(keyword):
    
    global driver
    global search_params
    global tweets_data

    try:
        
        search_url= generate_search_url(search_params)
        driver.get(search_url)
        time.sleep(5)
    
        take_screenshot("tweet_search")

        last_height = driver.execute_script("return document.body.scrollHeight")
        scraped_tweet_ids=set()


        while True:

            new_tweets=driver.find_elements("xpath", '//article[@data-testid="tweet"]')

            if len(new_tweets)>0:

                for tweet in new_tweets:

                    if tweet.id not in scraped_tweet_ids:

                        scraped_tweet_ids.add(tweet.id)
                        
                        tweet_lines = tweet.text.split("\n")

                        full_date_format = "%b %d, %Y"  # Example: "Oct 17, 2015"
                        short_date_format = "%b %d" # Example: "Mar 26"

                        # Get today's date and calculate the cutoff date (7 days ago)
                        today = datetime.today()
                        cutoff_date = today - timedelta(days=7)
                        
                        tweet_name = tweet_lines[0]
                        tweet_username = tweet_lines[1]
                        tweet_date_str = tweet_lines[3]
                        tweet_content ="\n".join(tweet_lines[4:])

                        if re.match(r"^\d+[smh]$", tweet_date_str):  # Matches "5s", "10m", "3h"
                            num = int(re.findall(r"\d+", tweet_date_str)[0])
                            unit = tweet_date_str[-1]
                    
                            if unit == "s":  # Seconds ago
                                tweet_date = today - timedelta(seconds=num)
                            elif unit == "m":  # Minutes ago
                                tweet_date = today - timedelta(minutes=num)
                            elif unit == "h":  # Hours ago
                                tweet_date = today - timedelta(hours=num)

                        elif "," in tweet_date_str:  # Full date format
                            tweet_date = datetime.strptime(tweet_date_str, full_date_format)
                    
                        else:  # Short date format (assume current year)
                            tweet_date = datetime.strptime(tweet_date_str, short_date_format)
                            tweet_date = tweet_date.replace(year=today.year)

                        print("Tweet date ="+str(tweet_date))

                        if tweet_date < cutoff_date:
                            break
                        
                        tweet_details = {
                            "name": tweet_name,  
                            "username": tweet_username,
                            "date": str(tweet_date), 
                            "content": tweet_content
                        }

                        tweets_data["tweets"].append(tweet_details)

                new_height= get_new_height(driver,new_tweets[-1])

                if  new_height== last_height:
                    logging.info("Reached end of page or no new tweets found.")
                    break  # Stop scrolling if no more content is loading
                last_height = new_height  # Update last height   
    
    

    except Exception as e:
         logging.error(f"Error while scraping, check screenshot for more clues: {e}")
         take_screenshot("error_scrapping")
    
    finally:
        df = pd.DataFrame(tweets_data)
        df.to_csv("solana_tweets.csv", index=False)
        logging.info("Scraping finalized with errors. Data saved to solana_tweets_selenium.csv")


    
def logout():

    global driver

    try:

        driver.get('https://x.com/logout')
        time.sleep(5)

        text="Log out"
        logout = driver.find_element(By.XPATH, f"//span[contains(text(), '{text}')]")
        logout.click()
        time.sleep(5)

    except Exception as e:

        logging.error(f"Error while logging out, check screenshot for more clues: {e}")
        take_screenshot("error_logout")

    finally:
        driver.close()
        driver.quit()



if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO)


    # Initialize the parser
    parser = argparse.ArgumentParser(description='Scraper X tweets')
    
    # Add arguments
    parser.add_argument('--keyword', action="store", dest='keyword', default='Solana')

    # Parse the arguments
    args = parser.parse_args()
    
    logging.info("Scraping X website for tweets of {}".format(args.keyword))

    try:
        init_web_driver()
        login()
        scrape_x(args.keyword)
        logout()
    except Exception as e:
        logging.error(f"Error while scraping: {e}")    

    