import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = "8133872651:AAEMudvAUb7e9wE275H2ca4ikVo6HokD29Y"
RAPIDAPI_KEY = "3075e723a0mshc801b0c9ebb0305p12e44fjsn0e60031210c6"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me your 10-digit PNR number.")

def get_pnr(update: Update, context: CallbackContext):
    pnr = update.message.text

    url = f"https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{pnr}"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "irctc-indian-railway-pnr-status.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data["success"]:
        d = data["data"]

        train_name = d.get("trainName")
        train_no = d.get("trainNumber")
        doj = d.get("dateOfJourney")
        from_station = d.get("sourceStation")
        to_station = d.get("destinationStation")
        boarding = d.get("boardingPoint")

        passenger = d.get("passengerList")[0]
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

        update.message.reply_text(message)

    else:
        update.message.reply_text("Invalid PNR number.")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_pnr))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
