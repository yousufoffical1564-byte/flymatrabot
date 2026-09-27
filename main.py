import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
AVIASALES_MARKER = "YOUR_MARKER"
BOOKING_AFF_ID = "YOUR_BOOKING_ID"

MAIN_MENU, FLIGHT_FROM, FLIGHT_TO, FLIGHT_DATE, FLIGHT_RETURN, FLIGHT_PASSENGERS, HOTEL_CITY, HOTEL_CHECKIN, HOTEL_CHECKOUT, HOTEL_GUESTS = range(10)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✈️ Flight", callback_data="flight")],
        [InlineKeyboardButton("🏨 Hotel", callback_data="hotel")]
    ]
    await update.message.reply_text("Welcome to FlyMatra Bot!\nChoose an option:", reply_markup=InlineKeyboardMarkup(keyboard))
    return MAIN_MENU

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "flight":
        await query.message.reply_text("Enter departure city:")
        return FLIGHT_FROM
    elif query.data == "hotel":
        await query.message.reply_text("Enter hotel city:")
        return HOTEL_CITY
    elif query.data == "main":
        await start(update, context)
        return MAIN_MENU

async def flight_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["from"] = update.message.text
    await update.message.reply_text("Enter destination city:")
    return FLIGHT_TO

async def flight_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["to"] = update.message.text
    await update.message.reply_text("Enter travel date (DD-MM-YYYY):")
    return FLIGHT_DATE

async def flight_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    city_from = context.user_data["from"]
    city_to = context.user_data["to"]
    date = context.user_data["date"]
    url = f"https://www.aviasales.com/search/{city_from}{date}{city_to}1?marker={AVIASALES_MARKER}"
    keyboard = [[InlineKeyboardButton("🔍 Search Flights", url=url)],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]]
    await update.message.reply_text(f"✈️ Flights from {city_from} to {city_to}\nDate: {date}", reply_markup=InlineKeyboardMarkup(keyboard))
    return MAIN_MENU

async def hotel_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["city"] = update.message.text
    await update.message.reply_text("Check-in date (DD-MM-YYYY):")
    return HOTEL_CHECKIN

async def hotel_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkin"] = update.message.text
    await update.message.reply_text("Check-out date (DD-MM-YYYY):")
    return HOTEL_CHECKOUT

async def hotel_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["checkout"] = update.message.text
    city = context.user_data["city"]
    checkin = context.user_data["checkin"]
    checkout = context.user_data["checkout"]
    url = f"https://www.booking.com/searchresults.html?ss={city}&aid={BOOKING_AFF_ID}"
    keyboard = [[InlineKeyboardButton("🏨 Search Hotels", url=url)],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]]
    await update.message.reply_text(f"🏨 Hotels in {city}\nCheck-in: {checkin}\nCheck-out: {checkout}", reply_markup=InlineKeyboardMarkup(keyboard))
    return MAIN_MENU

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(menu_callback, pattern="^main$")],
        states={
            MAIN_MENU: [CallbackQueryHandler(menu_callback, pattern="^(flight|hotel|main)$")],
            FLIGHT_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_from)],
            FLIGHT_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_to)],
            FLIGHT_D
