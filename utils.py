from langdetect import detect

SUPPORTED = {
    "en": "English", "fr": "French",
    "ar": "Arabic",  "de": "German",
    "es": "Spanish", "zh-cn": "Chinese"
}

def detect_language(text: str) -> tuple[str, str]:
    try:
        code = detect(text)
        name = SUPPORTED.get(code, "Unknown")
        return code, name
    except:
        return "en", "English"