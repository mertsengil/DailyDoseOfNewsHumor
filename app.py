#import libs
import streamlit as st
from db_read import DBReader
from model import generate_funny_summary
from scraper import Scraper
from db_ops import DBManager

# DB INFO
DB_HOST = 'HOST'
DB_USER = 'USER'
DB_PASSWORD = 'PASSWORD'
DB_DATABASE = 'DB_NAME'
BASE_URL = "https://www.donanimhaber.com/" #YOU MUST USE THIS URL
OUTPUT_PATH = "/path/to/your/articles.json"

scraper = Scraper(BASE_URL, OUTPUT_PATH)
scraper.scrape()

writer = DBManager(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)
data=writer.read_json_file(OUTPUT_PATH)
writer.insert_data_into_db(data)
writer.close()


db_reader = DBReader(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)
titles = db_reader.fetch_all_titles()

# START STREAMLIT
st.title('Funny News Summarizer')

# Show titles in dropdown menu
title = st.selectbox('Select tittle:', titles)

# Summarize button
if st.button('Summarize'):
    # Fetch content based on user-selected title
    content = db_reader.fetch_content_by_title(title)
    content = content['content']
    # send to AI model
    summary = generate_funny_summary(content)
    # SUM
    st.write('funny summary:', summary)


if st.button('Detayları Göster'):
    # Fetch details based on the title chosen by the user
    details = db_reader.fetch_content_by_title(title)
    # write details
    st.write('Başlık:', details['title'])
    st.write('İçerik:', details['content'])
    st.write('URL:', details['url'])

# close connection
db_reader.close()
