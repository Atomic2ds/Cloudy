from flask import Flask
from threading import Thread

app = Flask('')

@app.route("/ping", methods=["GET"])
def ping():
  return "OK", 200

def run():
  app.run(host='0.0.0.0',port=39192)

def uptime_ping():
    t = Thread(target=run)
    t.start()