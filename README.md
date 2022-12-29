# Binance

## Functionality
- To download interest data among different coins from https://www.binance.com/bapi/margin/v1/public/margin/vip/spec/history-interest-rate

## Prerequisite
- Python 3.0.0+

## Config in binance.py
<pre>
startYear  = 2020
startMonth = 1
endYear    = 2022
endMonth   = 12
coins      = ["BTC"]
</pre>

## Run
> python3 binance.py

## Data
- https://www.binance.com/bapi/margin/v1/public/margin/vip/spec/history-interest-rate
- stored in JSON format
- stored coin by coin
- stored according to months
- no json files will be generated if no data for particular coin in particular period

## Sample Output
```
[
    {"asset": "WAN", "timestamp": "1609372800000", "dailyInterestRate": "0.xxxxxxxx", "vipLevel": "0"}, 
    {"asset": "WAN", "timestamp": "1609286400000", "dailyInterestRate": "0.xxxxxxxx", "vipLevel": "0"},
    ...
]
```
##  Destination
```
	    dist/
        ├── <coin A>
        ├── <coin B>                   
        │   ├── <date>.json          
        │   ├── <date>.json         
        │   └── <date>.json 
        └── ...
```
