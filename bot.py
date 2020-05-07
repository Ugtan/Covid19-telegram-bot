#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bot to receive update regarding the COVID-19 epidemic.
"""

import json
import logging

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater)

import config
from fetch import Covid19, getAllCountries, getByCountry, getData
from graph import create_graph, create_vs_graph

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

_WELCOME_MSG = "Hello, Welcome to the Covid19-telegram-bot. Please type /help to view all the available commands."
_COUNTRY = ''
_COLOR_SCHEME = {"cases": "blue", "recovered": "green", "deaths": "red"}


def error(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def get_existing_users():
    """
    Get the json of all the existing users of the bot.
    """
    try:
        with open("users.json") as f:
            data = json.load(f)
            return data
    except Exception as e:
        if type(e).__name__ == "JSONDecodeError":
            open("users.json", "w+").write(json.dumps({}))
            return {}
        else:
            logging.error(
                "Some Exception has occured while getting the existing users.", exc_info=True)
    return False


def add_user(users):
    """
    Add the user to the user.json file.
    """
    try:
        open("users.json", "w").write(json.dumps(users))
    except Exception:
        logging.error("Error occured while adding the user.", exc_info=True)


def check_user(userid, username=None, fname=None):
    """
    Check if the user is already an existing user of the bot. Otherwise, the user will be added to the users.json file. 
    """
    users = get_existing_users()
    userinfo = {
        "username": username,
        "first_name": fname,
    }
    user = users.get(str(userid), None)

    if not user:
        users[str(userid)] = userinfo
        add_user(users)
        LOGGER.info(
            f"New user added to the user.json file with {userid}-{username}")


def start(update: telegram.Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name

    check_user(chat_id, username, first_name)

    context.bot.send_message(
        chat_id=chat_id, text=_WELCOME_MSG, parse_mode=telegram.ParseMode.HTML
    )


def stats(update: telegram.Update, context: CallbackContext):
    params = {'yesterday': True}
    data = getData("all", params=params)
    statistics = Covid19(data)
    message = f"*{statistics.country} Statistics*\n\n*🦠 Total Cases: *{statistics.cases}\n*🤒 Active: *{statistics.active}\n*💪🏼 Recovered: *{statistics.recovered}\n*☠️ Deaths: *{statistics.deaths}\n\n"
    message += f"*Today Statistics*\n\n*🦠 Today Cases: *{statistics.today_cases}\n*💪🏼 Recovered: *{statistics.today_recovered}\n*☠️ Deaths: *{statistics.today_deaths}"
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN
    )


def country_stats(update: telegram.Update, context: CallbackContext):
    country = ' '.join(context.args)
    if country:
        params = {'yesterday': True, 'sort': True}
        data = getData("countries", params=params)
        statistics = getByCountry(country, data)
        if statistics:
            message = f"*{statistics.country} Statistics*\n\n*🦠 Total Cases: *{statistics.cases}\n*🤒 Active: *{statistics.active}\n*💪🏼 Recovered: *{statistics.recovered}\n*☠️ Deaths: *{statistics.deaths}\n\n"
            message += f"*Today Statistics*\n\n*🦠 Today Cases: *{statistics.today_cases}\n*💪🏼 Recovered: *{statistics.today_recovered}\n*☠️ Deaths: *{statistics.today_deaths}"
        else:
            message = "Please enter a valid country name. To view the available country codes names enter /countries"
    else:
        message = "Please enter a country name. Country cannot be a empty string."

    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)


def countries(update: telegram.Update, context: CallbackContext):
    """To Show all the countries available"""
    message = "All the available countries are as follows:\n\n"
    message += ', '.join(getAllCountries())
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)


def available_plots(update: telegram.Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Total Cases", callback_data='cases'),
                 InlineKeyboardButton(
                     "Total Recovered", callback_data='recovered'),
                 InlineKeyboardButton("Total Deaths", callback_data='deaths')],
                [InlineKeyboardButton(
                    "New Cases vs. New Recoveries", callback_data='cases recovered')],
                [InlineKeyboardButton(
                    "New Recoveries vs. New Deaths", callback_data='recovered deaths')],
                [InlineKeyboardButton("New Cases vs. New Deaths", callback_data='cases deaths')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    global _COUNTRY
    _COUNTRY = ' '.join(context.args).strip().lower()
    if _COUNTRY in getAllCountries():
        update.message.reply_text(
            'Please choose a plot you would like to see:', reply_markup=reply_markup)
    else:
        message = "Please enter a valid country name in order to visualize the plots."
        chat_id = update.message.chat_id
        context.bot.send_message(
            chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)


def help(update, context):
    update.message.reply_text("Use /stats to view Covid-19 stats globally.")
    update.message.reply_text(
        "Use /country_stats COUNTRY to view Covid-19 stats for a particular country.")
    update.message.reply_text(
        "Use /countries to all the countries affeted by Covid-19.")
    update.message.reply_text(
        "Use /available_plots COUNTRY to visualize Covid-19 stat via different plots.")


def send_graph(update: telegram.Update, context: CallbackContext):
    """Send the graph to the user"""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(
        text="The plot is being displayed just wait for a while.")
    data = query.data.split()
    if len(data) == 1:
        create_graph(_COUNTRY, data[0], _COLOR_SCHEME[data[0]])
    else:
        create_vs_graph(_COUNTRY, data)
    context.bot.send_photo(chat_id=query.message.chat.id,
                           photo=open('graph.png', 'rb'))


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("countries", countries))
    dp.add_handler(CommandHandler("country_stats",
                                  country_stats, pass_args=True))
    dp.add_handler(CommandHandler("available_plots",
                                  available_plots, pass_args=True))
    dp.add_handler(CallbackQueryHandler(send_graph, pass_user_data=True))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
