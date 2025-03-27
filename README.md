# X/Twitter scrapping and sentiment-analysis tool

This tool is intended to scrape posts on the X platform from the las 7 days, based on search parameters defined by the user, and perform a basic sentiment analysis over the content of the tweets/posts obtained. By default, it is configured to scrape Solana-related posts from the feed page, directly after a search.

It uses [Selenium](https://huggingface.co/) to simulate a Firefox webdriver, and 3 pre-trained, open-source models obtained from the [Hugging Face](https://huggingface.co/) repository.

Due to the [anti-scrapping policies of X](https://x.com/en/tos), and to avoid getting my accout blocked due to [suspicious activity](https://github.com/elmaxiboy/x-scraper/blob/main/screenshots/common_errors/suspicious_login.png), this tool requires the user to put in a 2FA code while logging-in. The user must have a registered X account and [configured to use 2FA](https://help.x.com/en/managing-your-account/two-factor-authentication). For this purpose, during the development process [Microsoft Authenticator App](https://www.microsoft.com/de-de/security/mobile-authenticator-app) was used. 


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

**Note: Currently, the tool considers only the first item in the "langs" and "types" keys present in the dictionary**

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

**Warning: When running the program, log out from every instance of your X account. Otherwise you risk getting temporally blocked due to suspicious activity**

**Note 1: When first runned, the script should download the requirements to emulate a Firefox webdriver and download the 3 pre-trained sentiment-analysis models. This process can last for several minutes, depending on your internet speed**

**Note 2: The UI interaction might fail due to unhandled exceptions (e.g. New pop-ups, elements not loading fast enough, webdriver failing, etc). Please retrying when such s scenario occur. Error screenshots are saved in the screenshots/ directory for inspection**

With the virtual environment activated and the requirements installed, run the main script.

``` sh
python main.py
```

When asked to, write your 2FA code in the terminal to and hit enter:

``` sh
...
🔑 Enter the verification code generated by your Auth App: ******
...

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

## Results interpretation and possible scoring approaches

2 files are saved under the  `/results` directory, which is created if it does not exist. `scraped_tweets.json`, contains all the tweets obtained from the scrapping process, and `scraped_tweets_with_sentiment.json` is the same file but with the sentiment analysis results for every tweet. One result example would look like the following:


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
To generate a score for each post/tweet based on relevance, risk and reliability, lets first explain the output parameters obtained from the scrapping and sentiment analysis. The following table serves this explanatory purpose:

| **Attribute**        | **Description**                                 | **Interpretation** |
|----------------------|-------------------------------------------------|--------------------|
| **name**             | Name of the post author                         | Credibility of the human behind the account |
| **username**         | Username of the post author                     | More followers, more relevance  |
| **date**             | Date and time when the post was made            | More recent, more relevance|
| **content**          | Main body of the post                           | N/A |
| **citations**        | Mentions of other Twitter users in the post     | Interaction and relevance |
| **hashtags**         | Hashtags used in the post                       | Relevance and "trendiness" associated with the post |
| **engagement_numbers**| Number of likes, comments, reposts, views, respectively. (Might be incomplete)     | Interaction and relevance|
| **base_sentiment**   | General sentiment of the post's content (positive, neutral, negative) [link to model](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) | General emotional tone|
| **risk_sentiment**   | Sentiment regarding potential financial risk or uncertainty (bearish, neutral, bullish) [link to model](https://huggingface.co/ElKulako/cryptobert) | Perceived risk or uncertainty |
| **crypto_sentiment** | Sentiment regarding cryptocurrency topics (positive, negative) [link to model](https://huggingface.co/kk08/CryptoBERT) | Emotional tone in regards Crypto topics |

As they are, these output parameters can be used to further build a basic scoring mechanism to complement decision-making situations.

### A score for Relevance
The relevance score of a tweet can be calculated as a function of:
- The amount of followers a user has, higher scores are assigned with incresing amount of followers.
- The date of the post, where recent posts receive higher scores. The logic behind is that a 1-week old post does not add novelty and its effect is likely already absorved by the market, in comparison to a recent post.
- The relevance of the accounts that are cited. If the usernames cited are popular, the tweet might belong to a relevant event. This parameter can also consider keeping track of how many times different accounts/usernames are cited in the posts scrapped.
- Something similar occurs with hashtags. Eventhough the posters might not be popular, if a hashtag is used many times within a timeframe it might indicate more relevance.
- The engagement numbers (likes, comments, reposts, views) can also add to the relevance of the post, higher numbers mean that people got interested and engaged with the content. An engagement could have derived in a concrete market decision made by the viewer afterwards. 

### A score for Risk

The risk score given by the **risk_sentiment** output parameter, can be complemented by:
- Tracking price and volume changes. The risk score can be weighted by the delta change based on the previous values. A post its going to be more risky if the change from the previous post associated to the same content exhibits great changes.
- Hashtag clustering could serve to calculate risk respectively for different categories. E.g. #CryptoHack vs #CryptoLaw could mean different degrees of risk regarding the timeframe of action.
- Timestamp the post could also moderate the risk of a post. For certain categories, a post can be more or less risky based on how old it is.
- **base_sentiment** and **crypto_sentiment** can also serve as weights to the risk score. Positive-sentiment posts could decrease the risk score, and viceversa. 


### A score for Reliability

Reliability can be calculated as a function of:
- The nature of the post user. Different weights can apply for humans, bots, exchanges, politics, celebrities, etc.
- The amount of followers. A post belonging to a popular account can serve as a proxy to credibility and trustworthiness.
- Timestamp can also moderate the score, similar to the previously explained.


## TODOs

In order to achieve such a scoring mechaism, the current tool must be improved and iterated. The current scraping mechanism only retrieves the visible text present on the feed page after a search is performed, and is lacking relevant data related to the user that posted (E.g. Number of followers, nature). This could be achieved by scraping the profiles respectively and storing the values in a separated dictionary. The **engagement_numbers** must be appropiately identified. The sentiment analysis models could be specifically trained and validated for this use case. **hashtags** can be appropiately clustered to allow for a more specfic analysis of relevance. The [search query](https://x.com/search-advanced?lang=en) that is concatenated must be further studied and tested, as adding or removing hashtags or keywords can result in different groups of posts being retrieved. The use of a pay-per-use API could greatly improve the data-retrieving process (speed and completeness) and would be more compliant to the terms of use of X, or any other digital social network. Once this checklist is carried out, the scoring mechanism should be on a more solid platform to be built upon.

## Aknowledgements

This project was developed as a coding challenge for the TUM BlockSprint 2025, in less than 48 hours. It contains many details, feel free to contribute. A similar and more complete project that I used for reference on X web selectors and UI navigation is on [this repo](https://github.com/godkingjay/selenium-twitter-scraper).

The models used for sentiment-analysis can be found here:

- [cardiffnlp, twitter-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)
- [ElKulako, cryptobert](https://huggingface.co/ElKulako/cryptobert)
- [kk08, CryptoBERT](https://huggingface.co/kk08/CryptoBERT)
