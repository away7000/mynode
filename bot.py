import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# API KEYS
TELEGRAM_TOKEN = "8648654865:AAEsThOEU0YiR51MW_C0ptH7DOtIael5kzM"
OPENAI_API_KEY = "sk-0JFj4RoxWDSCcRBB8ikp5sxC8vai9Wtdw32DR3KGStxWTqsg"

client = OpenAI(api_key=OPENAI_API_KEY)

# Ambil harga crypto
def get_price(coin="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    data = requests.get(url).json()
    return data[coin]["usd"]

# AI response
def ai_response(user_input):
    price = get_price("bitcoin")

    prompt = f"""
    Kamu adalah AI crypto analyst.
    Harga BTC sekarang: ${price}

    Pertanyaan user: {user_input}

    Jawab dengan singkat + kasih insight trading.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Handle message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = ai_response(user_text)
    await update.message.reply_text(reply)

# Main
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot jalan...")
app.run_polling()
