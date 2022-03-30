#!/usr/bin/python3
#  -*- coding: utf-8 -*-
# Author: Gaston Martres <gastonmartres@gmail.com>

import json
from datetime import datetime
from flask import Flask, render_template, jsonify, make_response, request, abort, flash
from werkzeug.utils import secure_filename
from markupsafe import escape
import telebot
import time
import os

# Unicode chars
mark_ok = u'\U00002705'
mark_error = u'\U0000274C'
mark_warning = u'\U000026A0'

# Health Variables
m_sent = 0
m_unsent = 0
start_timestamp = datetime.timestamp(datetime.now())
http_401 = 0
http_413 = 0
http_420 = 0


# Telegram variables
TG_TOKEN=os.environ['TG_TOKEN']
TG_CHANNEL=os.environ['TG_CHANNEL']

# App variables
APP_DEBUG=os.environ['APP_DEBUG']
APP_TOKEN=os.environ['APP_TOKEN']
APP_VERSION=os.environ['APP_VERSION']

app = Flask(__name__)

# Configuraciones varias
app.config['UPLOAD_FOLDER'] = "/tmp"

@app.route('/')
def index():
    index_file = "index.html"
    return render_template(index_file)

@app.route('/health')
def health():
    global http_401,http_413,http_420,m_sent,m_unsent
    uptime = int(datetime.timestamp(datetime.now())) - int(start_timestamp)
    body = "http_401 " + str(http_401) + "\nhttp_413 " + str(http_413) + "\nhttp_420 " + str(http_420) + "\nmessages_sent " + str(m_sent) + "\nmessages_unsent " + str(m_unsent) + "\npod_started " + str(int(start_timestamp)) + "\npod_uptime " + str(uptime) + "\n\n"
    return body

@app.route("/version")
def version():
    version = {"version": APP_VERSION}
    return jsonify(version)

@app.route("/send")
def send():
    global http_401,http_413,http_420,m_sent,m_unsent
    #tg_token = request.args.get('tg_token')
    #channel = request.args.get('channel')
    message = request.args.get('message')
    token = request.args.get('token')
    severity = escape(request.args.get('severity'))
    if token != APP_TOKEN:
        http_401+=1
        abort(401, "Token no autorizado.")
    else:
        if len(message) >= 4096:
            http_413+=1
            abort(413,"El mensaje no puede superar los 4096 caracteres.")
        if len(message) <= 1:
            http_413+=1
            abort(413,"El mensaje no puede ser menor a 1 caracter.")
        if send_tg_message(TG_TOKEN,TG_CHANNEL,escape(message),severity):
            if APP_DEBUG:
                value = {"status": "sent", "message": escape(message)}
            else:
                value = {"status": "sent"}
            m_sent+=1
            return jsonify(value)
        else:
            http_420+=1
            abort(420,"Whaaaaaaaat?")

@app.route("/post", methods=['POST'])
def post():
    global http_401,http_413,http_420,m_sent,m_unsent
    message = request.form.get('message')
    token = request.form.get('token')
    severity = escape(request.form.get('severity'))
    if token != APP_TOKEN:
        http_401+=1
        abort(401, "Token no autorizado.")
    else:
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        send_tg_image(TG_TOKEN,TG_CHANNEL,os.path.join(app.config['UPLOAD_FOLDER'],filename),message,severity)
        m_sent+=1
        value = value = {"status": "sent"}
        return jsonify(value)

def send_tg_message(TG_TOKEN,TG_CHANNEL,TG_MESSAGE,severity="NORMAL"):
    try:
        if severity == "WARNING":
            message = mark_warning + " WARNING " + mark_warning + "\n" + TG_MESSAGE
        elif severity == "NORMAL":
            message = mark_ok + " SUCCESS " + mark_ok + "\n" + TG_MESSAGE
        elif severity =="ERROR":
            message = mark_error + " ERROR " + mark_error + "\n" + TG_MESSAGE
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_message(TG_CHANNEL,message)
        return True
    except Exception as e:
        print(e)
        return False

def send_tg_image(TG_TOKEN,TG_CHANNEL,image,TG_MESSAGE='',severity="NORMAL"):
    try: 
        if severity == "WARNING":
            message = mark_warning + " WARNING " + mark_warning + "\n" + TG_MESSAGE
            print("WARNING")
        elif severity == "NORMAL":
            message = mark_ok + " SUCCESS " + mark_ok + "\n" + TG_MESSAGE
            print("NORMAL")
        elif severity =="ERROR":
            message = mark_error + " ERROR " + mark_error + "\n" + TG_MESSAGE
            print("ERROR")
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_photo(TG_CHANNEL, photo=open(image,'rb'),caption=message)
        return True
    except Exception as e:
        print(e)
        return False
