import logging
import configparser
import os
import requests
import time
import datetime
import sys
import json

from telegram import (Bot)

def send_message(name, bot, config):
    message = name + " ist jetzt live!\ntwitch.tv/" + name
    bot.send_message(config["KovenBot"]["KovenID"], message, disable_notification=True)
    bot.send_message(config["KovenBot"]["KanalID"], message, disable_notification=True)

def main():

    # CONFIG

    configLocation = "config.ini"
    config = configparser.ConfigParser()
    config.read(configLocation)

    # LOGGING

    logger = logging.getLogger("uncaught")
    file = logging.FileHandler("errorLog.txt")
    logger.addHandler(file)

    def error(type, value, tb):
        cTime = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        logger.exception(str(cDate) + " - Uncaught exception: {0}".format(str(value)))
        logger.exception(str(cDate) + "Content:" + str(response))

    sys.excepthook = error

    # TELEGRAM

    bot = Bot(config['KovenBot']['TelegramToken'])

    # STREAMER

    streamers = {
        "n0ugatbits": "offline",
        "justfoxtom": "offline",
        "shellusaurr": "offline",
        "dummerdion": "offline",
        "robin_nosterafu": "offline",
        "s0ulfang": "offline",
        "ProfGhost": "offline",
        "halafier": "offline",
        "roteswasser": "offline",
        "joehan130": "offline",
        "retiredhitman": "offline",
        "steinhart17": "offline",
        "itsfreakingrosie": "offline"
    }

    # TWITCH
    oauthParams = { 'client_id' : config['KovenBot']['TwitchToken'], 'client_secret' : config['KovenBot']['clientSecret'], 'grant_type' : 'client_credentials'}
    oauth = requests.post("https://id.twitch.tv/oauth2/token", params=oauthParams)
    oauthResponse = oauth.json()
    accessToken = oauthResponse["access_token"]
    oauthString = "Bearer " + accessToken

    apiHeader = { 'Client-ID': config['KovenBot']['TwitchToken'], 'Authorization': oauthString }

    # LOGIC
    global response
    while True:
        for streamer, status in streamers.items():
            apiParams = { 'user_login': streamer }
            req = requests.get("https://api.twitch.tv/helix/streams", params=apiParams, headers=apiHeader)
            response = req.json()
            if len(response["data"]) > 0 and status != "live" :
                send_message(streamer, bot, config)
                streamers[streamer] = "live"
            elif len(response["data"]) == 0:
                streamers[streamer] = "offline"
        print(streamers)
        time.sleep(60)

if __name__ == '__main__':
    main()

