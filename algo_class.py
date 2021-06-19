"""

get nifty historical data
calculate ema high -10

get nifty spot data -every minute
pretty much like ema strategy
send email/sms using aws services
pending - make a call when alert triggered
#integrate with bandiwdth api
#integrating with email and sms for now 
"""
from helpers import get_historical_data,get_nifty_spot_data,get_trade_levels,send_email,trade_logger,config
import datetime
import sys
import logging
from kiteconnect import KiteConnect
kite = KiteConnect(api_key="your_api_key")
data = kite.generate_session("request_token_here", api_secret="your_secret")
kite.set_access_token(data["access_token"])

class ema_algo():
    def __init__(self) -> None:
        self.trade_buffer = 10
        self.trade_flag = False
        self.buy_level = 0
        self.sell_level = 0
        self.position = 0
    def send_alert(self,alert_type=None):
        send_email(alert_type)

    def algo(self):
        spx_current_data = get_nifty_spot_data()
        if not self.buy_level and not self.sell_level:
            hist_data = get_historical_data()
            trade_levels = get_trade_levels(hist_data,self.trade_buffer)
            self.buy_level = trade_levels["buy_level"]
            self.sell_level = trade_levels["sell_level"]
        if not self.trade_flag:
            if (self.buy_level >= spx_current_data['High'] >= self.sell_level) or (
                self.buy_level >= spx_current_data['Low'] >= self.sell_level):
                self.trade_flag = True
        if self.position==2 and spx_current_data['Low']<self.sell_level:
            trade_logger(datetime.datetime.now(),"long-exit",self.buy_level)
            self.send_alert(alert_type =  'exit_long')
            self.position = 0
        elif self.position==-2 and spx_current_data['High']<self.buy_level:
            trade_logger(datetime.datetime.now(),"short-exit",self.buy_level)
            self.send_alert(alert_type =  'exit_short')
            self.position = 0
        elif not self.position and self.trade_flag and spx_current_data['High']>= self.buy_level:
            trade_logger(datetime.datetime.now(),"long-entry",self.buy_level)
            self.send_alert(alert_type =  'initial_long_entry')
            self.position=2
        elif not self.position and self.trade_flag and spx_current_data['Low']<= self.sell_level:
            trade_logger(datetime.datetime.now(),"short-entry",self.sell_level)
            self.send_alert(alert_type = 'initial_short_entry')
            if config["real_trade_flag"]:
                kite.place_order(**updated_params)
            self.position=-2

    def zerodha_order():
        kiteconnect.place_order(**updated_params)

    def run_every_minute(self): 
        #get current spx data
        #check trade flag
        #check current spx level between the trade levels
        #trigger buy/sell signals
        #if trigger  notify trader what to do
        print("time in ",datetime.datetime.now())
        print(self.__dict__.items())
        if 9<=datetime.datetime.now().hour <= 15 and 10<=datetime.datetime.now().minute <= 31:
            self.algo()
        elif datetime.datetime.now().hour>15:
            sys.exit()