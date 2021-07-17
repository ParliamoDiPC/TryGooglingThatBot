from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from uuid import uuid4

def start(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Hi! I'm @TryGooglingThatBot, the bot for people that are too lazy to search something!\n\nEveryone knows at least one person who usually asks things that he can search on Google: with this bot, you can ditch him in seconds. This bot makes you able to do a search on some search engines and it makes fun of the questioning person.\n\nUse me in inline mode: @TryGooglingThatBot [query].")

def search(update: Update, context: CallbackContext) -> None:
        query = update.inline_query.query

        if query == "":
                result = [InlineQueryResultArticle(id = str(uuid4()), title = "Please input a query", input_message_content = InputTextMessageContent("Please input a query."))]
                update.inline_query.answer(result)
        else:
                import urllib
                processedquery = urllib.urlencode(query)
                import json
                with open("insults.json", "r") as insultsfile:
                        insults = json.load(insultsfile)
                with open("search_engines.json", "r") as enginesfile:
                        engines = json.load(enginesfile)
                import random
                insult = random.choice(insults["insults"])

                results = [
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with Google", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["google"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["google"]["name"])),
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with Bing", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["bing"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["bing"]["name"])),
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with StackOverflow", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["StackOverflow"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["stackoverflow"]["name"])),
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with DuckDuckGo", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["duckduckgo"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["duckduckgo"]["name"])),
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with GitHub", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["github"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["github"]["name"])),
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with Google News", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["news"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["news"]["name"])),
                        InlineQueryResultArticle(id = str(uuid4()), title = "Search with Amazon.com", input_message_content = InputTextMessageContent(insult.replace("%URL%", engines["amazon"]["queryurl"].replace("%QUERY%", processedquery)).replace("%SEARCHENGINE%", engines["amazon"]["name"])),
                ]

                update.inline_query.answer(results)

def main() -> None:
        bot = Updater("") # no token for you

        commands = bot.dispatcher

        commands.add_handler(CommandHandler("start", start))
        commands.add_handler(InlineQueryHandler(search))

        bot.start_polling()
        bot.idle()

if __name__ == "__main__":
        main()
