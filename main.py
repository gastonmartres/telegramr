#!/usr/bin/python3
#  -*- coding: utf-8 -*-
# Author: Gaston Martres <gastonmartres@gmail.com>

import json
from flask import Flask, render_template, jsonify, make_response, request
from markupsafe import escape
import telebot
import time
import os

TG_TOKEN=os.environ['TG_TOKEN']
TG_GROUP=os.environ['TG_GROUP']
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

@app.route("/send/<message>")
def send(message):
    if len(message) >= 4096:
        value = {"status": "not sent","reason": "El mensaje no puede superar los 4096 caracteres."}
        return jsonify(value)
    if send_tg_message(TG_TOKEN,TG_GROUP,escape(message)):
        value =  {"status": "sent", "message": escape(message)}
        return jsonify(value)
    else:
        value = {"status": "not sent", "reason": "not sent"}
        return jsonify(value)


def send_tg_message(TG_TOKEN,TG_GROUP,TG_MESSAGE):
    try:
        bot = telebot.TeleBot(TG_TOKEN)
    
        bot.send_message(TG_GROUP,TG_MESSAGE)
        return True
    except Exception as e:
        print(e)
        return False

