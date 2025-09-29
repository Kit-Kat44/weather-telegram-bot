import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Используй /weather <город> чтобы узнать погоду'
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('Укажи город: /weather Москва')
        return
    
    city = ' '.join(context.args)
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            
            message = f"""
🌍 Погода в городе {city}:
🌡️ Температура: {temp}°C
🤚 Ощущается как: {feels_like}°C
☁️ Описание: {description}
💧 Влажность: {humidity}%
            """
            
            await update.message.reply_text(message)
        else:
            await update.message.reply_text('Город не найден!')
            
    except Exception as e:
        await update.message.reply_text('Ошибка получения данных о погоде')

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
