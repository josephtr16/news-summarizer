from langdetect import detect, LangDetectException

LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "ar": "Arabic",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
}


def detect_language(text: str) -> str:
    """
    Detects the language of the given text.
    Returns a human-readable language name, or 'Unknown'.
    """
    try:
        code = detect(text)
        return LANGUAGE_NAMES.get(code, f"Unknown ({code})")
    except LangDetectException:
        return "Unknown"


def truncate_preview(text: str, max_chars: int = 500) -> str:
    """Returns a truncated preview of the article text."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."