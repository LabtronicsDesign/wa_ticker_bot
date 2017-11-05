# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:13:41 2017

@author: SPWC
"""

from coinmarketcap import Market

class ticker_sym(object):
    
    def messaged_ticker(self, ticker_call):
        
        currency_dict = {"€" : ["EUR","price_eur","market_cap_eur","€"],
                         "£" : ["GBP","price_gbp","market_cap_gbp","£"], 
                         "$" : ["dollar","price_usd","market_cap_usd","$"],
                         "฿" : ["bitcoin","price_btc","market_cap_usd","$"],
                         "Ƀ" : ["bitcoin","price_btc","market_cap_usd","$"]}
        
        coinmarketcap = Market()
        
        currency = ticker_call[0]
        out_curr = (currency_dict[currency][0])
        ticker1 = ticker_call[1:]
        
        if currency == '€' or '£':
            crypto_market = coinmarketcap.ticker(convert = out_curr)
        else:
            crypto_market = coinmarketcap.ticker(convert = "")

        if currency == "฿":
            currency = "Ƀ"
        
        coin_data = self.sym_to_list(ticker1,crypto_market)
        if coin_data == False:
            return False
        
        url_name = self.list_to_id(coin_data)

        try:
            if currency != "Ƀ":
                self.ticker_info = (
                      coin_data.get('name')+'\n'
                      'Price: '+ currency +" {:0,.2f}".format(float(coin_data.get(currency_dict[currency][1])))+'\n'
                      '1h: '+ coin_data.get('percent_change_1h')+' %'+'\n'
                      '24h: '+ coin_data.get('percent_change_24h')+' %'+'\n'
                      '7d: '+ coin_data.get('percent_change_7d')+' %'+'\n'
                      'Market Cap: '+ currency_dict[currency][3] +' {:0,.2f}'.format(float(coin_data.get(currency_dict[currency][2])))
                      )
            else:
                self.ticker_info = (
                      coin_data.get('name')+'\n'
                      'Price: '+ currency +" {:0,.8f}".format(float(coin_data.get(currency_dict[currency][1])))+'\n'
                      '1h: '+ coin_data.get('percent_change_1h')+' %'+'\n'
                      '24h: '+ coin_data.get('percent_change_24h')+' %'+'\n'
                      '7d: '+ coin_data.get('percent_change_7d')+' %'+'\n'
                      'Market Cap: '+ currency_dict[currency][3] +' {:0,.2f}'.format(float(coin_data.get(currency_dict[currency][2])))
                      )
         
        except:
            self.ticker_info = 'Error, not found'
        
        return self.ticker_info

    def sym_to_list(self,currency,data):
        try:
            self.coin_info = next((item for item in data if item["symbol"] == currency))
            return self.coin_info
        except:
            return False

    def list_to_id(self,coin_info):
        self.coin_id = self.coin_info.get('id')
        return self.coin_id