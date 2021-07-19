from algo_class import  ema_algo
import unittest

class TestEmaAlgo(unittest.TestCase):
    def test1(self):
        """
        check historical data is retrieved and ema is calculated
        """
        algo_instance = ema_algo()
        algo_instance.algo()
        assert algo_instance.buy_level and algo_instance.sell_level
        

    def test2(self):
        """
        test if trade flag is activated
        """
        algo_instance = ema_algo()
        algo_instance.algo()
        algo_instance.buy_level = algo_instance.spx_current_data['High']+3
        algo_instance.sell_level = algo_instance.spx_current_data['High']-3
        algo_instance.algo()
        assert algo_instance.trade_flag    

    def test3(self):
        """
        test if long triggers
        """
        algo_instance = ema_algo()
        algo_instance.algo()
        algo_instance.trade_flag = True
        algo_instance.buy_level = algo_instance.spx_current_data['High']+3
        algo_instance.sell_level = algo_instance.spx_current_data['High']-3
    


if __name__=="__main__":
    unittest.main()