#!/usr/bin/python3
#  -*- coding: utf-8 -*-
# Author: Gaston Martres <gastonmartres@gmail.com>

import json
from flask import Flask, render_template, jsonify, make_response, request, abort
from markupsafe import escape
import telebot
import time
import os

TG_TOKEN=os.environ['TG_TOKEN']
#TG_GROUP=os.environ['TG_GROUP']
TG_CHANNEL=os.environ['TG_CHANNEL']
APP_TOKEN=os.environ['APP_TOKEN']
print(APP_TOKEN)
APP_VERSION=os.environ['APP_VERSION']
app = Flask(__name__)

@app.route('/')
def index():
    index_file = "index.html"
    return render_template(index_file)

@app.route("/version")
def version():
    version = {"version": APP_VERSION}
    return jsonify(version)

@app.route("/send")
def send():
    #tg_token = request.arts.get('tg_token')
    #channel = request.args.get('channel')
    message = request.args.get('message')
    token = request.args.get('token')
    if token != APP_TOKEN:
        value = {"status": "not sent","reason": "El token no es conocido."}
        abort(401, "Token no autorizado.")
    else:
        if len(message) >= 4096:
            abort(413,"El mensaje no puede superar los 4096 caracteres.")
        if len(message) <= 1:
            abort(413,"El mensaje no puede ser menor a 1 caracter.")
        if send_tg_message(TG_TOKEN,TG_CHANNEL,escape(message)):
            value =  {"status": "sent", "message": escape(message)}
            return jsonify(value)
        else:
            abort(420,"Whaaaaaaaat?")

def send_tg_message(TG_TOKEN,TG_GROUP,TG_MESSAGE):
    try:
        bot = telebot.TeleBot(TG_TOKEN)
    
        bot.send_message(TG_GROUP,TG_MESSAGE)
        return True
    except Exception as e:
        print(e)
        return False

