import streamlit as st
from scraper import scrape_article
from summarizer import summarize
from utils import detect_language

st.set_page_config(page_title="News Summarizer", page_icon="🌍")
st.title("Multilingual News Summarizer")

url = st.text_input("Paste a news article URL")

col1, col2 = st.columns(2)
max_len = col1.slider("Summary length", 40, 150, 84)

if st.button("Summarize") and url:
    with st.spinner("Fetching article..."):
        text = scrape_article(url)
    
    lang_code, lang_name = detect_language(text)
    st.caption(f"Detected language: {lang_name}")
    
    with st.spinner("Summarizing..."):
        summary = summarize(text, max_len=max_len)
    
    st.subheader("Summary")
    st.write(summary)
    
    with st.expander("View raw article text"):
        st.write(text[:3000] + "...")