import argparse
import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from webdriver_manager.firefox import GeckoDriverManager



def scrape_x(keyword):
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
    
    # X (Twitter) search URL
    try:
        driver.maximize_window()
        driver.get('https://twitter.com/i/flow/login')
        time.sleep(5)

        username = driver.find_element(
                        "xpath", "//input[@autocomplete='username']"
                    )

        username.send_keys("ViegasMax")


        username.send_keys(Keys.RETURN)
        time.sleep(5)
        password = driver.find_element(
                        "xpath", "//input[@autocomplete='current-password']"
                    )
        password.send_keys("H3ySt4y0un6!")


        password.send_keys(Keys.RETURN)
        time.sleep(5)


        login_window=driver.get_full_page_screenshot_as_png()

        with open("verification_code.png", 'wb') as file:
            file.write(login_window) 


        twofactor = driver.find_element(
                        "xpath", "//input[@autocomplete='on']"
                    )
        verification_code = input("🔑 Enter the verification code sent to your phone/email: ")

        twofactor.send_keys(verification_code)
        twofactor.send_keys(Keys.RETURN)
        time.sleep(5)

        login_window=driver.get_full_page_screenshot_as_png()

        with open("landing_page.png", 'wb') as file:
            file.write(login_window) 


        try:
            accept_cookies_btn = driver.find_element(
            "xpath", "//span[text()='Refuse non-essential cookies']/../../..")
            accept_cookies_btn.click()
        except NoSuchElementException:
            pass

        cookies = driver.get_cookies()

        auth_token = None
        for cookie in cookies:
            if cookie["name"] == "auth_token":
                auth_token = cookie["value"]
                break
        if auth_token is None:
            raise ValueError(
                """This may be due to the following:

                - Internet connection is unstable
                - Username is incorrect
                - Password is incorrect
                """
                    )
    except Exception as e:
            print()
            logging.error(f"Login failed: {e}")
    
    logging.info("Login succeeded!")

    search_url = "https://x.com/search?q=(solana%20OR%20%24SOL)%20(hack%20OR%20exploit%20OR%20vulnerability%20OR%20bug%20OR%20rug%20OR%20phishing%20OR%20scam%20OR%20attack%20OR%20breach%20OR%20failure%20OR%20downtime%20OR%20issue%20OR%20critical)%20since%3A2025-03-19%20until%3A2025-03-26&src=typed_query&f=live"
    driver.get(search_url)
    # Wait for the page to load
    time.sleep(5)
    
    search_window=driver.get_full_page_screenshot_as_png()
    with open("search.png", 'wb') as file:
            file.write(search_window) 

    tweets=driver.find_elements(
            "xpath", '//article[@data-testid="tweet" and not(@disabled)]'
        )
    
    for tweet in tweets:
         print(tweet.text)

    
    driver.get('https://x.com/logout')
    time.sleep(5)

    logout_window=driver.get_full_page_screenshot_as_png()
    with open("logout.png", 'wb') as file:
            file.write(logout_window) 


    text="Log out"
    logout = driver.find_element(By.XPATH, f"//span[contains(text(), '{text}')]")
    logout.click()

    time.sleep(5)

    login_window=driver.get_full_page_screenshot_as_png()

    with open("last.png", 'wb') as file:
            file.write(login_window) 

    driver.close()
    driver.quit()

    
    # Scroll and collect tweets
    tweets_data = []
    """ tweet_count = 50  # Adjust the number of tweets you want to scrape
    while len(tweets_data) < tweet_count:
        tweets = driver.find_elements(By.XPATH, '//article[@role="article"]')
        for tweet in tweets:
            try:
                username = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
                content = tweet.find_element(By.XPATH, './/div[@lang]').text
                date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
                tweet_link = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute("href")
    
                tweets_data.append([date, username, content, tweet_link])
    
                if len(tweets_data) >= tweet_count:
                    break
            except Exception:
                continue
            
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
     """
    # Save tweets to CSV
    df = pd.DataFrame(tweets_data, columns=["Date", "User", "Tweet", "URL"])
    df.to_csv("solana_tweets_selenium.csv", index=False)
    
    print("Scraping complete. Data saved to solana_tweets_selenium.csv")
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

    scrape_x(args.keyword)

    