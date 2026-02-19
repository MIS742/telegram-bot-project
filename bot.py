import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me your 10-digit PNR number.")


async def get_pnr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pnr = update.message.text

    url = f"https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{pnr}"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "irctc-indian-railway-pnr-status.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("success"):
        d = data.get("data", {})

        train_name = d.get("trainName")
        train_no = d.get("trainNumber")
        doj = d.get("dateOfJourney")
        from_station = d.get("sourceStation")
        to_station = d.get("destinationStation")
        boarding = d.get("boardingPoint")

        passenger = d.get("passengerList", [{}])[0]
        coach = passenger.get("coachPosition")
        seat = passenger.get("berthNo")
        current_status = passenger.get("currentStatus")

        message = f"""
🚆 Train: {train_name} ({train_no})
📅 Date: {doj}

📍 From: {from_station}
📍 To: {to_station}
📍 Boarding: {boarding}

💺 Coach: {coach}
🛏 Seat: {seat}
📌 Status: {current_status}
"""

        await update.message.reply_text(message)

    else:
        await update.message.reply_text("Invalid PNR number.")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_pnr))

    print("PNR Bot running on Render...")
    app.run_polling()


if __name__ == "__main__":
    main()
