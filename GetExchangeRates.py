#Public libraries
import requests
import time
from Token import apiKey
from DBH import UpdateExchangeRatesDB, GetExchangeRates, UpdateCryptoRatesDB, GetCryptoRates
from random import randint
import json

#Own libraries
from NewPrint import Print

exchangeRates = {}
cryptoRates = []

headers={'Cache-Control': 'no-cache'}

def SheduleUpdate():
    global exchangeRates
    while True:
        exchangeRates = UpdateExchangeRates()
        time.sleep(86400)

def SheduleCryptoUpdate():
    global cryptoRates
    while True:
        cryptoRates = UpdateCryptoRates()
        cryptoRates['TON'] = UpdateTON()
        UpdateCryptoRatesDB(cryptoRates.copy())
        time.sleep(randint(10,30))  

def UpdateExchangeRates() -> dict:
    global exchangeRates
    Print("Updating of exchange rates has started.", "S")
    try:
        url = "http://data.fixer.io/api/latest?access_key=" + apiKey
        response = requests.get(url,headers=headers)
        exchangeRates = response.json()['rates']
        exchangeRates['TMT'] = exchangeRates['RUB']/2
        UpdateExchangeRatesDB(exchangeRates.copy())
        Print("Updating of exchange rates is successfull.", "S")
    except:
        Print("Updating ER failed.", "E")
        Print("Using exchange rates from DB.", "W")
        exchangeRates = GetExchangeRates()
    return exchangeRates.copy()


def UpdateCryptoRates() -> dict:
    global cryptoRates
    #read cryptolist from crypto.json
    with open('Dictionaries/crypto.json') as json_file:
        cryptoData = json.load(json_file)
    
    cryptoList = [crypto['code'] for crypto in cryptoData['crypto']]
    

    Print("Updating of crypto rates has started.", "S")
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(url,headers=headers)
        cryptoRates = {}
        for pair in response.json():
            if pair['symbol'].find("USDT") != -1 and any(pair['symbol'][:-4] == s for s in cryptoList):
                cryptoRates[pair['symbol'][:-4]]=float(pair['price'])
        Print("Updating of crypto rates is successfull.", "S")
    except:
        Print("Updating CR failed. Trying different endpoint", "E")
        try:
            url = "https://api1.binance.com/api/v3/ticker/price"
            response = requests.get(url, headers=headers)
            cryptoRates = {}
            for pair in response.json():
                if pair['symbol'].find("USDT") != -1 and any(pair['symbol'][:-4] == s for s in cryptoList):
                    cryptoRates[pair['symbol'][:-4]]=float(pair['price'])
            Print("Updating of crypto rates is successfull.", "S")
        except:
            Print("Updating CR failed. Trying different endpoint", "E")
            try:
                url = "https://api2.binance.com/api/v3/ticker/price"
                response = requests.get(url,headers=headers)
                cryptoRates = {}
                for pair in response.json():
                    if pair['symbol'].find("USDT") != -1 and any(pair['symbol'][:-4] == s for s in cryptoList):
                        cryptoRates[pair['symbol'][:-4]]=float(pair['price'])
                Print("Updating of crypto rates is successfull.", "S")
            except:
                Print("Updating CR failed. Trying different endpoint", "E")
                try:
                    url = "https://api3.binance.com/api/v3/ticker/price"
                    response = requests.get(url,headers=headers)
                    cryptoRates = {}
                    for pair in response.json():
                        if pair['symbol'].find("USDT") != -1 and any(pair['symbol'][:-4] == s for s in cryptoList):
                            cryptoRates[pair['symbol'][:-4]]=float(pair['price'])
                    Print("Updating of crypto rates is successfull.", "S")
                except:
                    Print("Using crypto rates from DB.", "S")
                    cryptoRates = GetCryptoRates()
        
    return cryptoRates.copy()

def UpdateTON() -> float:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
        response = requests.get(url,headers=headers)
        Print("Updating TON rate is successfull.", "S")
    except:
        Print("Updating TON rate failed.", "E")
        Print("Using TON rate from DB.", "W")
        return GetCryptoRates()['TON']
    return response.json()['the-open-network']['usd']