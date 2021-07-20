# ema_strategy_custom

##Idea of the strategy
How this strategy is different from MA crossover...
The entry point for entry/exit has a buffer
The exit is not static...it gets updated along with MA

1. Take one moving average indicator like SMA/EMA...based on close/high/low/open on some window (10,11.....)
2. For entry exits on n+1 day Calculate buffer ema_level_nth_day+x/ema_level_nth_day-x.... 
3. ema_level_nth_day+x is for buy and ema_level_nth_day-x is for sell. The price has to open between the buffer zone for the entry/exits to be valid.
4. if algo generated a position (buy/sell)..the exit price would be the rolling buffer level. If the position is long then the exit is when the price hits sell level on any given day.
5. Position Sizing..enter with 2x lots/positions.exit 1x on partial profit (x pips for forex, x points or ATR for index/stocks) exit the second lot/positions at exit.

