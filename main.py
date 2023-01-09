from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bot import dp, bot, TOKEN
from models.msg_model import Msg
from aiogram import types, Dispatcher, Bot
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')

# Инициализация бота
WEBHOOK_PATH = f'/bot/{TOKEN}'
# Нужон ngrok такемта aiogram слушает вебхук на localhost, а он занят uvicorn'ом
WEBHOOK_URL = 'https://dfeb-217-66-159-32.eu.ngrok.io' + WEBHOOK_PATH


@app.on_event('startup')
async def startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    tel_update = types.Update(**update)
    await dp.feed_update(
        bot=bot,
        update=tel_update
    )


@app.on_event('shutdown')
async def stop():
    await bot.session.close()


# Хэндлеры (Потом уберу в отедльный роутер)

@app.get('/', response_class=HTMLResponse)
async def home(req: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': req,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


@app.post('/api/sendmsg', response_class=JSONResponse)
async def bot_send_msg(msg: Msg):
    await bot.send_message(
        chat_id='986572732',
        text=msg.text
    )
