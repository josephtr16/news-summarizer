from transformers import BartForConditionalGeneration, BartTokenizer
import streamlit as st


@st.cache_resource(show_spinner="Loading summarization model...")
def load_summarizer():
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    return tokenizer, model


def summarize(text: str, max_length: int = 150, min_length: int = 40) -> str:
    tokenizer, model = load_summarizer()

    # Split into chunks of ~900 words to stay within token limits
    words = text.split()
    chunk_size = 900
    chunks = [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

    summaries = []
    for chunk in chunks:
        if len(chunk.strip()) < 50:
            continue

        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
        )

        output_ids = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )

        summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        summaries.append(summary)

    if not summaries:
        return "Could not generate a summary."

    # If multiple chunks, do a final pass on the combined summaries
    if len(summaries) > 1:
        combined = " ".join(summaries)
        inputs = tokenizer(
            combined,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
        )
        output_ids = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )
        return tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return summaries[0]