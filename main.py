import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, ADMIN_ID
from predict import predict_image

os.makedirs("downloads", exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Assalomu alaykum!\n\n"
        "📷 Menga rasm yuboring.\n"
        "Men uni tahlil qilib beradi."
    )


async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = await update.message.reply_text("🔍 Rasm tahlil qilinmoqda...")

    photo = update.message.photo[-1]

    file = await photo.get_file()

    file_path = f"downloads/{photo.file_unique_id}.jpg"

    await file.download_to_drive(file_path)

    try:

        result = predict_image(file_path)

        # Foydalanuvchiga natija
        await msg.edit_text(result)

        # Adminga rasm va ma'lumot yuborish
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=open(file_path, "rb"),
            caption=
            f"""
📢 Yangi rasm yuborildi

👤 Ism: {update.effective_user.full_name}

🆔 ID: {update.effective_user.id}

📛 Username: @{update.effective_user.username}

📝 Natija:

{result}
"""
        )

    except Exception as e:

        print(e)

        await msg.edit_text(
            f"❌ Xatolik yuz berdi.\n\n{e}"
        )

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            image_handler,
        )
    )

    print("✅ Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    main()