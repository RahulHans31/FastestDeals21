import telebot
import requests
import re
from bs4 import BeautifulSoup

bot = telebot.TeleBot("5845010274:AAGjg3fca1jycXlbmngJz1YJobLrJiI7nJI")
affiliate_id = "fastestdeals-21"

def convert_amazon_link_to_affiliate_id(link, affiliate_id):
    
    # Retrieve HTML from Amazon product page
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract ASIN from HTML using regular expressions
    asin_pattern = r'/dp/([A-Z0-9]{10})'
    asin_match = re.search(asin_pattern, link)
    if asin_match:
        asin = asin_match.group(1)
    else:
        asin_tag = soup.find('input', {'name': 'ASIN'})
        if asin_tag:
            asin = asin_tag.get('value')
        else:
            return None

    # Construct affiliate ID link
    affiliate_link = f'https://www.amazon.in/dp/{asin}/?tag={affiliate_id}'

    return affiliate_link

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Please enter your Amazon link to encode it with your affiliate ID.")

@bot.message_handler(func=lambda message: True)
def encode_url(message):
    # Convert Amazon link to affiliate link
    affiliate_link = convert_amazon_link_to_affiliate_id(message.text, affiliate_id)

    if affiliate_link:
        # Encode and shorten affiliate link
        encoded_url = "https://fastestdealsfirst.blogspot.com/p/track.html?trackurl=" + affiliate_link
        response = requests.get(f"http://tinyurl.com/api-create.php?url={encoded_url}")
        shortened_url = response.text

        # Reply to user with encoded and shortened URL
        bot.reply_to(message, "Here is your encoded and shortened URL:\n" + shortened_url)
    else:
        bot.reply_to(message, "Invalid Amazon link")

bot.polling()
