# Covid19-telegram-bot

A telegram bot which allows you to keep track of the covid-19 all around the globe and analyse the data via plots.

## Features:
* Global Statistics
* Country wise Statistics
* Plots
    * Total cases
    * Total recoveries
    * Total deaths
    * New Cases vs New Recoveries
    * New Recoveries vs New Deaths
    * New Cases vs New Deaths

## Setup
1. Clone the repository.
2. Create a python 3 virtual enviroment:
    
    `python3 -m venv venv`
3. Activate the virtual environment:

    `source venv/bin/activate`

4. Install required Python dependencies: 

    `pip install -r requirements.txt`
5. Create a telegram API token with bot father. Following the [link](https://medium.com/shibinco/create-a-telegram-bot-using-botfather-and-get-the-api-token-900ba00e0f39) to generate your own token.
6. Add token to the *config.py* file.
7. Run python bot.py

## Commands
```
/start
To start the Covid19 Telegram bot.

/stats
To view Covid-19 stats globally.

/country_stats COUNTRY
To view Covid-19 stats for a particular country.

/countries
To show all the countries affected by the Covid-19.

/available_plots
To show different plots to the user to analyse the spread of Covid-19.
```

## Sources
* [Python telegram bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [Novel COVID API](https://github.com/NovelCOVID/API)

## Images
* Statistics
    
    ![Stats](https://github.com/Ugtan/Covid19-telegram-bot/blob/master/images/stats.png)
* Total Cases plot
    
    ![Total Cases](https://github.com/Ugtan/Covid19-telegram-bot/blob/master/images/totaldeaths.png)
* Recovered Cases plot
    
    ![Recovered](https://github.com/Ugtan/Covid19-telegram-bot/blob/master/images/recovered.png)
* Death Cases plot
    
    ![Deaths](https://github.com/Ugtan/Covid19-telegram-bot/blob/master/images/totaldeaths.png)
* Vs Plot
    
    ![VsPlot](https://github.com/Ugtan/Covid19-telegram-bot/blob/master/images/vsplot.png)
