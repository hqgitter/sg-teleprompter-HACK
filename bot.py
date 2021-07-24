#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, shelve

flashcards = shelve.open('flashcards.db',writeback=True)


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    update.message.reply_text('To add/review flashcards, start with /flashcard')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def flashcard(update,context):
    chat_id=update.message.chat_id
    keyboard = [['/old'],['/new']]
    reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    update.message.reply_text("Would you like to enter new flashcards or review old ones",reply_markup=reply_markup)
def old(update,context):
    keyboard = []
    for key in flashcards:
        keyboard.append(["/review "+key])
    reply_markup=ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
    update.message.reply_text("select the flashcard you would like to review by title:",reply_markup=reply_markup)

def new(update,context):
    if context.args ==[]:
        update.message.reply_text("Enter title of your flashcard (/new (insert title here))")
    else:
        update.message.reply_text("Entered title: ")
        answer = " ".join(context.args)
        update.message.reply_text(answer)
        flashcards[answer]={'chat_id':update.message.chat_id,'qn':'','ans':''}
        flashcards[answer]['chat_id']=update.message.chat_id
        update.message.reply_text("next you can add your question via '/question (title of flashcard) (insert question here)")
        flashcards.close()


def question(update,context):
    flashcards = shelve.open('flashcards.db', writeback=True)
    for key in flashcards:

        if key == context.args[0]:
            userqn = " ".join(context.args[1:])
            flashcards[key]['qn']=(userqn)
            flashcards.close()
    update.message.reply_text("then you may add your answer to this question via '/addanswer (title of flashcard) (insert answer here)")

def addanswer(update,context):
    flashcards = shelve.open('flashcards.db', writeback=True)
    for key in flashcards:
        if key ==context.args[0]:
            userans=" ".join(context.args[1:])
            flashcards[key]['ans']=userans
    update.message.reply_text('Added answer. You may review by doing /review (title of question)')

flashcards.close()
def review(update,context):
    for key in flashcards:
        if key==context.args[0]:
            update.message.reply_text("Question: "+flashcards[key]['qn'])
            update.message.reply_text("answer with '/ans (title of qn) (answer here):")
def ans(update,context):
    for key in flashcards:
        if key==context.args[0]:

            userans = " ".join(context.args[1:])
            if userans==flashcards[key]['ans']:
                update.message.reply_text('Correct')
            else:
                update.message.reply_text('Incorrect')

flashcards = shelve.open('flashcards.db',writeback=True)









def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1920506010:AAGEOzFN_17e3O9_6MWLG24yvvczgP17lwI", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("flashcard",flashcard))
    dp.add_handler(CommandHandler("old",old))
    dp.add_handler(CommandHandler("new",new))
    dp.add_handler(CommandHandler("question",question))
    dp.add_handler(CommandHandler("addanswer",addanswer))
    dp.add_handler(CommandHandler("review",review))
    dp.add_handler(CommandHandler("ans",ans))



    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, review))

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
flashcards.close()
