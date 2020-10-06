import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

# function to get latest finance news articles
def get_news():
    res = requests.get("https://www.cnbc.com/world/?region=world")
    soup = BeautifulSoup(res.text, 'html.parser')
    news = soup.select('#MainContent > div:nth-child(2) > div > div > div:nth-child(6) > div.PageBuilder-col-6.PageBuilder-col')[0]
    links = news.find_all('a')

    headlines = []
    for link in links:
        if len(link.text) > 30:
            headlines.append(link.text)

    hrefs = []
    for link in links:
        if len(link.text) > 30:
            hrefs.append(link['href'])

    top5 = "Here's your latest finance news articles:\n"
    for i in range(0, 5):
        top5 += headlines[i] + "\n" + hrefs[i] + "\n"
    return top5

# function to get top 10 articles from quantstart systematic trading
def get_quantstart_articles():
    res = requests.get("https://www.quantstart.com/articles/topic/systematic-trading/")
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select("body > div > section.mb-2 > div")[0]

    lines = []
    for post in posts.findAll('p')[:10]:
        lines.append(post.text)

    hrefs = []
    for href in posts.findAll('a')[:10]:
        hrefs.append(href['href'])

    links = []
    for href in hrefs:
        link = 'https://www.quantstart.com' + href
        links.append(link)

    top10 = "Here's the top 10 articles from Quantstart Systematic Trading:\n"
    for i in range(0, 10):
        top10 += lines[i] + "\n" + links[i] + "\n"
    return top10


# command to be executed at the starting of the bot for the first time
def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = '''
    Use these commands to use the bot:
    /news - get the latest finance news articles
    /quantstart - get top articles of Algorithmic Trading from Quantstart
    /help - get list of commands of the bot''')

# function to display top 5 finance news headlines
def get_top_news(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Just a sec! Fetching latest finance news!")
    top5 = get_news()
    context.bot.send_message(chat_id = update.effective_chat.id, text = top5)

# function to display top 10 quantstart articles
def get_quantstart(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Just a sec! Fetching the top quant finance articles!")
    top10 = get_quantstart_articles()
    context.bot.send_message(chat_id = update.effective_chat.id, text = top10)

# function to get list of all commands
def get_commands(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = '''
    /news - get the latest finance news articles
    /quantstart - get top articles of Algorithmic Trading from Quantstart
    /help - get list of commands of the bot''')

def main():
    updater = Updater('1115939597:AAFJr-WpQz96yJ_ulJXwNApv_q32WuMg2Jk')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('news', get_top_news))
    dp.add_handler(CommandHandler('quantstart', get_quantstart))
    dp.add_handler(CommandHandler('help', get_commands))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
