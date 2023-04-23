from unidecode import unidecode


# Normalize name
def normalize_str(text: str) -> str:
    return unidecode(text).upper()
