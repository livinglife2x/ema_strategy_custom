import logging
from kiteconnect import KiteConnect
import os
os.environ['TZ'] = 'Asia/Kolkata'
import datetime

logging.basicConfig(level=logging.DEBUG)

#automate login later
#kite = KiteConnect(api_key="your_api_key")

#data = kite.generate_session("request_token_here", api_secret="your_secret")
#kite.set_access_token(data["access_token"])




#somewhere
from algo_class import ema_algo
import time

algo_instance = ema_algo()
#algo_instance.send_alert(alert_type="Program Started")
print("program started")
while True:
    algo_instance.run_every_minute()
    time.sleep(60)


