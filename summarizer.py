from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL = "csebuetnlp/mT5_multilingual_XLSum"

import streamlit as st

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL, use_fast=False
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    return tokenizer, model

# Call this once at app startup
tokenizer, model = load_model()

WHITESPACE_HANDLER = lambda k: " ".join(
    k.strip().split()
)

def summarize(text: str, max_len=84, min_len=30) -> str:
    text = WHITESPACE_HANDLER(text)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )
    ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        max_length=max_len,
        min_length=min_len,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    return tokenizer.decode(ids[0], skip_special_tokens=True)