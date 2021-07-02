import yfinance as yf
import datetime
import pandas as pd
from datetime import timedelta
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

with open("config.json") as file:
    config = json.load(file)

def get_nifty_spot_data():
    try:
        data = yf.download("^NSEI", period = "1d",interval = '1m')
        today = str(datetime.datetime.now().date())
        data_index = list(map(lambda x:str(x)==today ,data.index.to_series().apply(lambda x: x.date())))
        data = data[data_index]
        data_dict = {}
        data_dict['High'] = data['High'][-1]
        data_dict['Close'] = data['Close'][-1]
        data_dict['Low'] = data['Low'][-1]
        data_dict['Open'] = data['Open'][-1]
        return data_dict
    except Exception as e:
        print(e)
        print("failed to get spot data")

def get_historical_data():
    try:
        start = str((datetime.now().date()-timedelta(days = 60)))
        #end = str(datetime.now(est).date().date())
        yesterday = str((datetime.now().date()-timedelta(days = 1)))
        data = yf.download("^NSEI", start=start, end=yesterday)
        return data
        
    except Exception as e:
        print(e)
        print("Failed to get historical data")

def get_trade_levels(data,trade_buffer):
    trade_level = pd.Series.ewm(data['High'], span=10,adjust = False).mean()[-1]
    buy_level = trade_level+trade_buffer
    sell_level = trade_level-trade_buffer
    return {"trade_level":trade_level,"buy_level":buy_level,"sell_level":sell_level}

def send_email(alert_type):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = receiver_email= "emailfortrading434@gmail.com"
    password = "eirgjdvexlrbfumc"

    # Create a secure SSL context
    context = ssl.create_default_context()
    message = MIMEMultipart()
    message["Subject"] = "Trade Alert"
    body = f"""\
    trade alert {alert_type}"""
    message.attach(MIMEText(body,'plain'))
    text = message.as_string()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        print("sending email failed")
        print(e)
    finally:
        server.quit() 

def trade_logger(*args):
    args = [str(x) for x in args]
    msg = " ".join(args)
    msg = msg+"\n"
    with open("trade_log.csv","a+") as file:
        file.write(str(msg))
    return True

def get_nifty_fut_symbol(self):
    #instruments = kite.instruments(exchange = "NFO")
    pass