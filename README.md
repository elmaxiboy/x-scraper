# X/Twitter scrapping and sentiment-analysis tool

This tool is intended to scrape tweets on the X platform from the las 7 days, based on search parameters defined by the user, and perform a basic sentiment analysis over the content of the tweets obtained. By default, it is configured to scrape Solana-related tweets.

It uses [Selenium](https://huggingface.co/) to simulate a Firefox webdriver, and 3 open-source models obtained from the [Hugging Face](https://huggingface.co/) repository.

Due to the [anti-scrapping policies of X](https://x.com/en/tos), this tool requires the user to put in a 2FA code while logging-in. The user must have registered X account and [configured to use 2FA](https://help.x.com/en/managing-your-account/two-factor-authentication). During the development process [Microsoft Authenticator App](https://www.microsoft.com/de-de/security/mobile-authenticator-app) was used. 


## Getting started

[Python version 3.12.3](https://www.python.org/downloads/release/python-3123/) was used, make sure your envorinment meets this requirement.

### Create and activate a virtual environment within the project's root directory:

``` sh
python3 -m venv .venv

source .venv/bin/activate # On Linux/MacOS

.venv\Scripts\activate #On Windows
```
### Install requirements using pip

Make sure to have [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) installed, then run:
``` sh
pip install -r requirements.txt
```

### Create environment variables to store user X credentials:

Within the project's root directory create a file named `.env` and add the following variables with your own values:

``` sh
USERNAME=your_X_username
PASSWORD=your_X_password
EMAIL=your_X_email_account
```
### Configure search parameters:

**Warning! The tool has not been tested with many different search configurations and could not work properly if radically changed. To test it first, using the default parameters is recommended.**

The `search_params.json` contains the dictionary of parameters to build the search query, change it to test more configurations:

``` sh
{
    "queries": ["solana"],
    "hashtags": ["#solana", "#crypto","#SOL","#breaking","#scam","#cryptonews"],
    "langs": ["en"],
    "types": ["live", "top"]
}

```

## Run the program

**Note 1: When first runned, the script should download the requirements to emulate a Firefox webdriver and download the 3 sentiment-analysis models. This process can last for several minutes, depending on your internet speed**

**Note 2: The UI interaction might fail due to unhandled exceptions (e.g. New pop-ups, elements not loading fast enough, webdriver failing, etc). Please retrying when such s scenario occur. Error screenshots are saved in the screenshots/ directory for inspection**

With the virtual environment activated and the requirements installed, run the main script.

``` sh
python main.py
```

Upon a successful run, your terminal should look like more or less like this:

``` sh

INFO:root:🤖 Scraping X website for Solana-related tweets
INFO:root:🌐 Initializing WebDriver. This might take a while...
INFO:WDM:====== WebDriver manager ======
INFO:WDM:Get LATEST geckodriver version for 136.0 firefox
INFO:WDM:Get LATEST geckodriver version for 136.0 firefox
INFO:WDM:Driver [/home/max-escobar-viegas/.wdm/drivers/geckodriver/linux64/v0.36.0/geckodriver] found in cache
INFO:root:🚪 Login into X
🔑 Enter the verification code generated by your Auth App: ******
INFO:root:Login succeeded!
INFO:root:💻 Scraping tweets from the past 7 days. CTRL-C to interrupt.
INFO:root:6 new tweets were found.
INFO:root:13 new tweets were found.
INFO:root:Scraping finalized. 18 tweets were obtained. Data saved to results/scraped_tweets.json
INFO:root:🚪 Logging out
INFO:root:🧐 Performing sentiment analysis
Asking to truncate to max_length but no maximum length is provided and the model has no predefined maximum length. Default to no truncation.
Device set to use cpu
Device set to use cpu
INFO:root:Sentiment analysis ended. Results saved into results/scraped_tweets_with_sentiment.json
INFO:root:👋 Process concluded successfully. Tschüss!

```

## Results and Interpretation

2 files are saved under the  `/results` directory, which is created if it does not exist. `scraped_tweets.json`, contains all the tweets obtained from the scrapping process, and `scraped_tweets_with_sentiment.json` is the same file but with the sentiment analysis results for every tweet. One result example would look like:


``` sh

        "tweet": {
            "name": "Oliver James {CRYPTO RECOVERY EXPERT}",
            "username": "@zishere99",
            "date": "2025-03-27 00:38:27.550300",
            "content": "ALERT \n\n &  are scamming investors by blocking withdrawals!  Lost ETH, USDT, or other assets? DM me for recovery help!\n\n             \n1\n95",
            "citations": [],
            "hashtags": [
                "#Fonnbit",
                "#Civodex",
                "#CryptoScam",
                "#Asdebit",
                "#CryptoRecovery",
                "#Scam",
                "#Girdex",
                "#Solana",
                "#Blofin",
                "#Dexozer",
                "#Macord",
                "#Helius",
                "#Xdoxo",
                "#Axellbit",
                "#RexoSwap",
                "#Bitex24"
            ],
            "engagement_numbers": [
                1,
                95
            ],
            "base_sentiment": {
                "label": "negative",
                "score": 0.7736554145812988
            },
            "risk_sentiment": {
                "label": "neutral",
                "score": 0.7449170351028442
            },
            "crypto_sentiment": {
                "label": "negative",
                "score": 0.952109694480896
            }
        }
```

| **Attribute** | **Descritpion**                    |**Calculation**                    | **Interpretation** |
|---------------|------------------------------------|--------------------|
|name|||
|username|||
|date|||
|content|||
|citations|||
|hashtags|||<>
|engagement_numbers|||
|base_sentiment|||
|risk_sentiment|||
|crypto_sentiment|||
