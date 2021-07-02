
#test signals first
#fetch instrument token

"""
order_id = kite.place_order(exchange="NFO",
                                        tradingsymbol="NIFTY18FEBFUT",
                                        transaction_type="BUY",
                                        quantity="75",
                                        product="NRML",
                                        order_type="LIMIT",
                                        validity="DAY",
                                        price = "10366",
                                        variety="regular")
order_history(order_id)
"""

from helpers import get_historical_data,get_nifty_spot_data,get_trade_levels,send_email,trade_logger,config
import datetime
import sys
import json
from kiteconnect import KiteConnect
#kite = KiteConnect(api_key="your_api_key")
#data = kite.generate_session("request_token_here", api_secret="your_secret")
#kite.set_access_token(data["access_token"])

class ema_algo():
    def __init__(self) -> None:
        self.trade_buffer = config["trade_buffer"]
        self.trade_flag = False
        self.buy_level = 0
        self.sell_level = 0
        self.trade_price = 0
        self.lot_1_exit_buffer = config["first_lot_exit"]
        self.position = config["position"]
        self.spx_current_data = None
    def send_alert(self,alert_type=None):
        send_email(alert_type)

    def algo(self):
        self.spx_current_data = get_nifty_spot_data()
        if not self.buy_level and not self.sell_level:
            hist_data = get_historical_data()
            trade_levels = get_trade_levels(hist_data,self.trade_buffer)
            self.buy_level = trade_levels["buy_level"]
            self.sell_level = trade_levels["sell_level"]
        if not self.trade_flag and (self.buy_level >= self.spx_current_data['High'] >= self.sell_level) or (
            self.buy_level >= self.spx_current_data['Low'] >= self.sell_level):
            self.trade_flag = True

        if self.position==2 and self.spx_current_data['High']>self.trade_price+self.lot_1_exit_buffer:
            trade_logger(datetime.datetime.now(),"partial-long-exit",spx_current_data['High'])
            self.send_alert(alert_type =  'partial_exit_long')
            self.trade_price = self.spx_current_data['High']
            self.position = config["position"]=1     
            self.update_config(config)
        elif self.position>0 and self.spx_current_data['Low']<self.sell_level:
            trade_logger(datetime.datetime.now(),"long-exit",spx_current_data['Low'])
            self.send_alert(alert_type =  'exit_long')
            self.trade_price = self.spx_current_data['Low']
            self.position = config["position"]=0
            self.update_config(config)
        elif self.position==-2 and self.spx_current_data['Low']<self.sell_level-self.lot_1_exit_buffer:
            trade_logger(datetime.datetime.now(),"partial_exit_short",spx_current_data['Low'])
            self.send_alert(alert_type =  'partial_exit_short')
            self.trade_price = self.spx_current_data['Low']
            self.position =config["position"]= -1
            self.update_config(config)
        elif self.position<0 and self.spx_current_data['High']>self.buy_level:
            trade_logger(datetime.datetime.now(),"short-exit",spx_current_data['High'])
            self.send_alert(alert_type =  'exit_short')
            self.trade_price = self.spx_current_data['High']
            self.position = config["position"]=0
            self.update_config(config)
        elif not self.position and self.trade_flag and self.spx_current_data['High']>= self.buy_level:
            trade_logger(datetime.datetime.now(),"long-entry",self.buy_level)
            self.send_alert(alert_type =  'initial_long_entry')
            self.trade_price = self.buy_level
            self.position=config["position"]=2
            self.update_config(config)
        elif not self.position and self.trade_flag and self.spx_current_data['Low']<= self.sell_level:
            trade_logger(datetime.datetime.now(),"short-entry",self.sell_level)
            self.send_alert(alert_type = 'initial_short_entry')
            self.trade_price = self.sell_level
            self.position=config["position"]=-2
            self.update_config(config)

    def update_config(self,dict):
        with open("config.json","w") as file:
            json.dump(dict,file)


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