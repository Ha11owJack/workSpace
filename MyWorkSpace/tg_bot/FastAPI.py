import httpx
from fastapi import FastAPI, Request
import os
from time import sleep
from confid import Token
from sql_telega import Database
import requests

app = FastAPI()


# async def SendReqTG(message, id_name):
#    tg_msg = {"chat_id": id_name, "text": message, "parse_mode": "Markdown"}
#    API_URL = f"https://api.telegram.org/bot{Token}/sendMessage"
#    async with httpx.AsyncClient() as client:
#        await client.post(API_URL, json=tg_msg)


@app.post("/hook")
async def recWebHook(req: Request):
    """
    Receive the Webhook and process the Webhook Payload to get relevant data
    Refer https://developer.github.com/webhooks/event-payloads for all GitHub Webhook Events and Payloads
    """
    body = await req.json()
    event = req.headers.get("X-Gogs-Event")
    if event == "push":  # check if the event is a star
        sender = Database().hook_get(body["html_url"])
        message = f"Репозиторий обновлен, пожалуйста подтвердите обновление: "
        while Database().state() == 1:
            sleep(10)
            await requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(Token, "sendMessage"),
                                data={'chat_id': sender, 'text': message}).json()
            # await SendReqTG(message, sender)
# В панель другие добавить измениние статуса хука
