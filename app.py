import streamlit as st
from scraper import fetch_article_text
from summarizer import summarize
from utils import detect_language, truncate_preview

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="News Summarizer",
    page_icon="📰",
    layout="centered",
)

st.title("📰 Multilingual News Summarizer")
st.markdown("Paste any news article URL to get a clean, concise summary.")

# ── Inputs ─────────────────────────────────────────────────────────────────────
url = st.text_input(
    "News article URL",
    placeholder="https://www.bbc.com/news/...",
)

max_length = st.slider(
    "Summary length (words, approx.)",
    min_value=50,
    max_value=300,
    value=150,
    step=10,
)

summarize_btn = st.button("Summarize", type="primary", use_container_width=True)

# ── Main logic ─────────────────────────────────────────────────────────────────
if summarize_btn:
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        # Step 1 — Fetch article
        with st.spinner("Fetching article..."):
            article_text = fetch_article_text(url)

        if not article_text:
            st.error(
                "❌ Could not extract article text from this URL.\n\n"
                "Some sites block automated access. Try a different article or source."
            )
        else:
            # Step 2 — Detect language
            language = detect_language(article_text)
            st.info(f"🌐 Detected language: **{language}**")

            # Step 3 — Summarize
            with st.spinner("Summarizing..."):
                summary = summarize(article_text, max_length=max_length)

            # Step 4 — Display results
            st.subheader("Summary")
            st.success(summary)

            with st.expander("View raw article text"):
                st.write(truncate_preview(article_text, max_chars=1000))

            st.caption(f"Article word count: {len(article_text.split()):,}")