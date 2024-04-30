from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging

# Configura il token del tuo bot
TOKEN = "7181402460:AAFcsknMEgoUWOS_m0pY39DMeLKD2KzDImQ"

# Configura il logger per visualizzare i log di debug
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dizionario per memorizzare lo stato del menu dell'utente (ID_utente: stato_menu)
user_menu_state = {}


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user_menu_state[user_id] = "main"  # Imposta lo stato del menu come "main" per l'utente
    context.bot.send_message(chat_id=user_id, text="Benvenuto! Scegli un'opzione:", reply_markup=main_menu_keyboard())


def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Shop", callback_data='shop')],
        [InlineKeyboardButton("Profilo", callback_data='profile')],
        [InlineKeyboardButton("Carrello", callback_data='cart')],
        [InlineKeyboardButton("Chat con l'Admin", callback_data='admin_chat')]
    ]
    return InlineKeyboardMarkup(keyboard)


def shop_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Prova1", callback_data='product_1')],
        [InlineKeyboardButton("Prova2", callback_data='product_2')],
        [InlineKeyboardButton("Prova3", callback_data='product_3')],
        [InlineKeyboardButton("Torna al Menu Principale", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


def profile_menu_keyboard(user_id) -> InlineKeyboardMarkup:
    username = context.bot.get_chat(user_id).username
    keyboard = [
        [InlineKeyboardButton(f"Username: {username}", callback_data='dummy')],
        [InlineKeyboardButton(f"ID Utente: {user_id}", callback_data='dummy')],
        [InlineKeyboardButton("Torna al Menu Principale", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)


def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.message.chat_id
    data = query.data

    if data == 'shop':
        user_menu_state[user_id] = "shop"
        query.edit_message_text(text="Scegli un prodotto:", reply_markup=shop_menu_keyboard())
    elif data == 'profile':
        user_menu_state[user_id] = "profile"
        query.edit_message_text(text="Informazioni Profilo:", reply_markup=profile_menu_keyboard(user_id))
    elif data == 'cart':
        # Implementa la gestione del carrello
        query.edit_message_text(text="Carrello (in costruzione)", reply_markup=main_menu_keyboard())
    elif data == 'admin_chat':
        # Implementa la chat con l'amministratore
        query.edit_message_text(text="Chat con l'Admin (in costruzione)", reply_markup=main_menu_keyboard())
    elif data == 'main_menu':
        user_menu_state[user_id] = "main"
        query.edit_message_text(text="Torna al Menu Principale:", reply_markup=main_menu_keyboard())
    else:
        # Implementa la gestione dei prodotti
        product_name = data.replace('product_', '')
        query.edit_message_text(text=f"Hai selezionato: {product_name}", reply_markup=shop_menu_keyboard())


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
