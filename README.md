# X/Twitter scrapping and sentiment-analysis tool

This tool is intended to scrape tweets on the X platform, based on search parameters defined by the user, and perform a basic sentiment analysis over the content of the tweets obtained . By default, it is configured to scrape Solana-related tweets.

It uses [Selenium](https://huggingface.co/) to simulate a Firefox webdriver, and 3 open-source models obtained from the [Hugging Face](https://huggingface.co/) repository.

Due to the [anti-scrapping policies of X](https://x.com/en/tos), this tool requires the user to put in a 2FA code. The user must have registered X account and [configured to use 2FA](https://help.x.com/en/managing-your-account/two-factor-authentication). During the development process [Microsoft Authenticator App](https://www.microsoft.com/de-de/security/mobile-authenticator-app) was used.


## Getting started

