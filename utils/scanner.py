import pytesseract

from PIL import (
    ImageEnhance,
    ImageFilter
)

# =========================================================
# TESSERACT PATH
# =========================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =========================================================
# IMAGE PROCESSING
# =========================================================

def preprocess_image(image):

    image = image.convert("L")

    enhancer = ImageEnhance.Contrast(image)

    image = enhancer.enhance(2)

    image = image.filter(ImageFilter.SHARPEN)

    return image

# =========================================================
# OCR
# =========================================================

def extract_text(image, lang="eng"):

    processed = preprocess_image(image)

    text = pytesseract.image_to_string(

        processed,

        lang=lang,

        config="--psm 6"
    )

    return " ".join(text.split())