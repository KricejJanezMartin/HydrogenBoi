import os
import telepot
import openai
import requests
from bs4 import BeautifulSoup

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram group chat ID where you want to send the summaries
group_chat_id = 'YOUR_GROUP_CHAT_ID'

# Define a list of allowed user IDs who can interact with the bot
allowed_user_ids = ['YOUR_USER_ID']

# Function to summarize text using OpenAI with a percentage of the article's length
def summarize_text(text, max_percentage=10):
    max_tokens = int(len(text.split()) * max_percentage / 100)
    response = openai.Completion.create(
        model="gpt-4",
        prompt=text,
        max_tokens=max_tokens,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

# Function to fetch and summarize an article from a URL
def summarize_article(url, max_percentage=10):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the article content from the webpage (you may need to adjust this based on the website's structure)
        article_text = soup.find('div', {'class': 'article-content'}).get_text()

        # Summarize the article
        summary = summarize_text(article_text, max_percentage)

        return summary
    except Exception as e:
        return str(e)

# Function to send the summary to the Telegram group
def send_summary_to_group(chat_id, introduction, summary, full_article_url):
    intro_message = f"Za vas smo danes pripravili povzetek članka:\n\n{introduction}\n\nČe želite izvedeti več kliknite tukaj: {full_article_url}"
    bot.sendMessage(chat_id, intro_message)

# Function to handle incoming Telegram messages
def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        user_message = msg['text']
        
        # Check if the user is allowed to interact with the bot
        if chat_id not in allowed_user_ids:
            bot.sendMessage(chat_id, "Nimate dovoljenja za uporabo tega bota.")
            return
        
        # Check if the user wants to summarize text provided in the message
        if user_message.startswith('/summarize'):
            article_text = user_message[len('/summarize'):].strip()
            
            if article_text:
                summary = summarize_text(article_text)
                send_summary_to_group(group_chat_id, "Povzetek članka:", summary, "")
            else:
                bot.sendMessage(chat_id, "Prosimo, vnesite besedilo članka za povzetek.")
        else:
            bot.sendMessage(chat_id, "Pošljite /summarize, nato pa vnesite besedilo članka za povzetek.")

# Create a Telegram bot using your bot token
bot = telepot.Bot('YOUR_BOT_TOKEN')

# Start listening for incoming messages
bot.message_loop(handle_message)

# Keep the script running
while True:
    pass
