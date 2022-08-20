from unittest import result
import requests, time
import datetime

# 1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
def q1():
    symbol_info = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()
    ticker_price = requests.get('https://api.binance.com/api/v3/ticker/24hr').json()
   
    btc_symbols = []
    s_info = symbol_info["symbols"]
    for s in s_info:
        if s["quoteAsset"] == "BTC":
            btc_symbols.append(s["symbol"])

    ticker_price = sorted(ticker_price, key=lambda x: float(x["volume"]), reverse = True)
    results = []
    counter = 0
    for ticker in ticker_price:
        symbol = ticker["symbol"]
        if symbol in btc_symbols:
            counter = counter + 1
            results.append(symbol)

        if counter == 5:
            break 

    return results

# 2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.
def q2():
    symbol_info = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()
    ticker_price = requests.get('https://api.binance.com/api/v3/ticker/24hr').json()
   
    usdt_symbols = []    # all symbols with 'USDT' quoteAsset
    s_info = symbol_info["symbols"]
    for s in s_info:
        if s["quoteAsset"] == "USDT":
            usdt_symbols.append(s["symbol"])

    # number of trades in descend over last 24 hr
    ticker_price = sorted(ticker_price, key=lambda x: float(x["count"]), reverse = True)
    results = []    
    counter = 0
    for ticker in ticker_price:
        symbol = ticker["symbol"]
        if symbol in usdt_symbols:
            counter = counter + 1
            results.append(symbol)

        if counter == 5:
            break 

    return results

# 3. Using the symbols from Q1, what is the total notional value of the top 200 bids-and-asks currently on each order book?
def q3():
    symbols = q1()
    results = {}
    for symbol in symbols:
        total_notional = 0
        order_info = requests.get('https://api.binance.com/api/v3/depth?symbol='+symbol+'&limit=200').json()
        bids = order_info["bids"]
        asks = order_info["asks"]

        for b in bids:
            notional = float(b[0]) * float(b[1])
            total_notional = total_notional + notional

        for a in asks:
            notional = float(a[0]) * float(a[1])
            total_notional = total_notional + notional
        
        results[symbol] = total_notional
    return results

# 4. What is the price spread for each of the symbols from Q2?
def q4():
    results = {}
    symbols = q2()
    symbols = ",".join('"{}"'.format(i) for i in symbols )         
    ticker_price = requests.get('https://api.binance.com/api/v3/ticker/24hr?symbols=['+symbols+']').json()        
    for ticker in ticker_price:
        price = float(ticker["bidPrice"]) - float(ticker["askPrice"])
        results[ticker['symbol']]=price
    
    return results

# 5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
def q5():
    prev = q4()
    curr = prev
    while True:
        results = []
        for sym in curr:
            abs_price = abs(curr[sym]-prev[sym]) 
            results.append({sym+'_p_spread':curr[sym], sym+'_abs_delta':abs_price})
        
        print('[timestamp:'+datetime.datetime.now().strftime('%H:%M:%S')+']')
        print(results)
        time.sleep(10)
        prev = curr
        curr = q4()
        
    return None

# call function here q1() q2() q3() q4() q5()
# res = q1() 
# print(res)


