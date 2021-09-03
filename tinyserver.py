import hprose
import requests
import json
import pika
import sys
import os
import logging
import xmlrpc.client

from datetime import datetime
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from newsapi import NewsApiClient
from xmlrpc.server import SimpleXMLRPCServer
app = Flask(__name__)

nLogger = logging.getLogger('werkzeug')
h = logging.FileHandler('calls.log')
nLogger.addHandler(h)

@app.route('/receive')
def rec():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


@app.route('/getnews')
def get_news():
    # Init
    newsapi = NewsApiClient(api_key='42c6fe851e9247e98841b984ede83d2d')

    #/v2/everything
    all_articles = newsapi.get_everything(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          domains='bbc.co.uk,techcrunch.com',
                                          from_param='2021-03-16',
                                          to='2021-12-12',
                                          language='en',
                                          sort_by='relevancy',
                                          page=1)


    # Find out what data type we are working with
    print(type(all_articles))
    # output buffer
    output = ''
    # loop over the key and values in the dict
    for k, v in all_articles.items():
        print(k, v)
        output = output + str(v) # add the value onto the buffer

    return output # return buffer with data

#JustWeather
@app.route('/justweather')
def testing():
     #r = requests.get('api.openweathermap.org/data/2.5/weather?q=Dublin&appid=66d31282aafd2e0234807bf3463450d5')
    r = requests.get('http://newsapi.org/v2/everything?q=weather forecast&from=2021-03-16&sortBy=publishedAt&apiKey=42c6fe851e9247e98841b984ede83d2d')

    print(r.status_code)

    jsoncontent = r.text #get the json content
    y = json.loads(jsoncontent) #load json
    art = y['articles']

    return str(art)

@app.route('/callClient/<int:sample>')
def rpc(sample):
    with xmlrpc.client.ServerProxy("http://localhost:8001") as proxy:

            print(" the temp  %s" %str(proxy.temp(sample)))

#         sample = int(sample)
#         print(sample)
#         min = 0
#         mid = 10
#         max = 20
#
#         if sample < mid or sample == min:
#             print('It is cold')
#
#         elif sample > mid or sample == max:
#             print("it is warm")

    return 'Called RPC function'


@app.route('/pingrpc')
def pingrpc():
    client = hprose.HttpClient('http://127.0.0.1:8080/')

    return client.hello("World")

@app.route('/insertStudent/<firstname>/<lastname>/<sNumber>')
def student(firstname, lastname, sNumber):

    time = datetime.now()
    timestamp = datetime.timestamp(time)
    date_time = time.strftime("%d/%m/%Y, %H:%M:%S")
    student = firstname, lastname, sNumber, date_time

    file = open("users.log", "a")
    print("Writing to a file")
    file.write(str(student))
    file.close()

    return ''

@app.route('/')
def hello_world():
    nLogger.info("INFO")
    return 'Hello, World!'

@app.route('/sendData')
def send_data():
    data = request.args.get('data')
    return 'Sending data to the server: ' + str(data)

@app.route('/updates')
def justupdates_call():
    f = open('C:/Users/craig/Documents/Atom Projects/XML & Webservices/lab1/updates.txt', 'r')
    x = f.readlines()
    output = '{'

    print(type(x))
    print(x)

    for item in x:
        #line 1 : item 1,
        output = output + '"line": "'+item +'",'
    f.close()

    #remove the last trailing comma
    output = output[:-1]
    output = output + '}'
    return output

@app.route('/ping')
def ping_call():
        time = datetime.now()
        timestamp = datetime.timestamp(time)
        date_time = time.strftime("%d/%m/%Y, %H:%M:%S")


        return 'Pong ' + date_time
