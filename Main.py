import logging
import sqlite3
import time

from telegram import Bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
bot  = Bot(token="1300652419:AAFTJbMj0meJYJWVx41P2Ki6Wbeh0p_kj-4")
activeBot = ""

logger = logging.getLogger(__name__)

SELECTION, LINK, MESSAGE, SENDMESSAGE, BUTTON, GETSERVERINFO = range(6)

#conn = sqlite3.connect("adData.db")


def mainMenu(update, context):
    context.user_data["bot"] = ""
    context.user_data["link"] = ""
    context.user_data["message"] = ""
    reply_keyboard = [['First', 'Second', 'Third']]

    update.message.reply_text(
        'Hi! Select bot plz or write /end to stop conversation',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return SELECTION

def chose(update, context):
    data = update.message.from_user
    text = update.message.text
    logger.info(data)
    logger.info(text)
    context.user_data["bot"] = text
    logger.info(context.user_data)
    update.message.reply_text("You chose " + text + " bot!")
    return ConversationHandler.END


def active(update, context):
    global activeBot
    if context.user_data["bot"] == "":
        update.message.reply_text("Active bot is NONE")
    else:
        update.message.reply_text("Active bot is " + context.user_data["bot"])
    
def adMessage(update, context):
    if context.user_data["bot"] != "First":
        update.message.reply_text("Please, select First bot for this function")
        return
    oldMessage = update.message.text
    update.message.reply_text("Please, enter ur channel name: ")
    return LINK

def getLink(update, context):
    link = update.message.text
    context.user_data["link"] = link
    #bot.send_message(chat_id = "@%s" % link, text = "HELLO GUYS")
    
    #update.message.reply_text("Ur link is " + link)
    
    update.message.reply_text("Please, enter ur message text: ")
    
    return MESSAGE
        
def getMessage(update, context):
    message = update.message.text
    context.user_data["message"] = message
    update.message.reply_text("Please, enter button name: ")
    return BUTTON
    
def getButton(update, context):
    buttonName = update.message.text
    context.user_data["button"] = buttonName
    bot.send_message(chat_id = "@%s" % context.user_data["link"], text = context.user_data["message"], reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(buttonName, callback = "t.me/" + context.user_data["link"])]]))
    update.message.reply_text("Message was sent to " + context.user_data["link"] + " channel.")
    return ConversationHandler.END

def serverNameGet(update, context):
    update.message.reply_text("Please enter server id")
    return GETSERVERINFO

def serverInfoShow:
    serverID = update.message.text

def end(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("Bye! I hope we can talk again some day.",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1300652419:AAFTJbMj0meJYJWVx41P2Ki6Wbeh0p_kj-4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('select', mainMenu)],

        states={
            SELECTION: [MessageHandler(Filters.regex('^(First|Second|Third)$'), chose)]
            
        },

        fallbacks=[CommandHandler('end', end), CommandHandler('chose', chose)]
    )
    
    serverInfo_handler = ConversationHandler(entry_points=[CommandHandler('serverinfo', serverNameGet)],
    states={
        GETSERVERINFO:[MessageHandler(Filters.all(), serverInfoShow)]
        },
        fallbacks=[CommandHandler('end', end)])
    
    firstBot_conv_handler = ConversationHandler(
    entry_points = [CommandHandler("admessage", adMessage)],
    states = {
    LINK: [MessageHandler(Filters.text, getLink)],
    MESSAGE: [MessageHandler(Filters.text, getMessage)],
    BUTTON: [MessageHandler(Filters.text, getButton)]
    },
    
    fallbacks=[CommandHandler('end', end)]
                                                )

    dp.add_handler(main_conv_handler)
    dp.add_handler(firstBot_conv_handler)
    dp.add_handler(CommandHandler("active", active))
    #dp.add_handler(CommandHandler("send", send))
    #dp.add_handler(CommandHandler("adMessage", adMessage))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
