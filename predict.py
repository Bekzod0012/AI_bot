from google import genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
    os.getenv("GEMINI_API_KEY_6"),
    os.getenv("GEMINI_API_KEY_7"),
]

PROMPT = """
Siz rasmni tahlil qiluvchi AI siz.

Javobni faqat quyidagi formatda yozing:

📌 Nomi:
...

📝 Tavsif:
...

🎯 Ishonchlilik:
...%

Boshqa hech narsa yozmang.
"""

def predict_image(image_path):
    image = Image.open(image_path)

    last_error = None

    for key in API_KEYS:

        if not key:
            continue

        try:
            client = genai.Client(api_key=key)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[PROMPT, image]
            )

            return response.text

        except Exception as e:
            last_error = str(e)

            # Limit tugagan bo'lsa keyingi API ga o'tadi
            if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
                continue

            # Server band bo'lsa ham keyingisini sinaydi
            if "503" in last_error or "UNAVAILABLE" in last_error:
                continue

            # Boshqa xato bo'lsa darhol qaytaradi
            return f"❌ Xatolik:\n\n{last_error}"

    return (
        "⚠️ Bot vaqtincha ishlamayapti.\n\n"
        "⏳ Iltimos, keyinroq qayta urinib ko'ring."
    )