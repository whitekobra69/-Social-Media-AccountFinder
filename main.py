import constants as keys
from telegram.ext import *
import Responses as R
import requests
from bs4 import BeautifulSoup

print("Bot Started...")

def start_command(update,context):
    update.message.reply_text("Ask Questions like who are you?,creator?")

def help_command(update, context):
    update.message.reply_text("Type /info_{username} to search for the person")
def info(update,context):
  id = update.message.text.replace('/info_', '')
  headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
  try:
    url="https://www.google.com/search?q="+id
    response=requests.get(url,headers=headers)
    socialmedia=["instagram","facebook","twitter","linkedin","github","scholar","hackerearth","hackerrank","hackerone","tiktok","youtube","books","researchgate","publons","orcid","maps"]
    linklist=[]
    soup=BeautifulSoup(response.content,'html.parser')
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if 'href' in str(anchors[0]):
            linklist.append(anchors[0]['href'])
    c=0
    foundedlinks=[]
    update.message.reply_text("Social Media Links")
    for i in socialmedia:
        sm=str(i)
        for j in linklist:
            if sm in str(j):
                c=c+1
                foundedlinks.append(j)
                update.message.reply_text(j)
    update.message.reply_text("[-] Checking for any pdf documents associated with this name .....")
    url="https://www.google.com/search?q=%22"+id+"%22+filetype%3Apdf&oq=%22"+id+"%22+filetype%3Apdf"
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'html.parser')
    f=0
    for g in soup.find_all('div', class_='g'):
        links = g.find_all('a')
        if 'href' in str(links[0]):
            update.message.reply_text(links[0]['href'])
    if c == 0:
        update.message.reply_text("No Info about this person")
  except Exception as e:
    print(e)

  update.message.reply_text(id, parse_mode='Markdown')

def handle_message(update,context):
    text=str(update.message.text).lower()
    response=R.sample_response(text)

    update.message.reply_text(response)

def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater=Updater(keys.API_KEY,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(RegexHandler("^(/info_[\w]+)$", info))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

main()
