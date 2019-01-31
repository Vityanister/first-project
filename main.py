import argparse
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import datetime

DATE = datetime.datetime.now()

DATA={
      "XRP":"https://coinmarketcap.com/currencies/ripple/historical-data/?start=20130428&end={}{}{}".format(DATE.year,DATE.month,DATE.day),
      "BTC":"https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end={}{}{}".format(DATE.year,DATE.month,DATE.day),
      "ETH":"https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20130428&end={}{}{}".format(DATE.year,DATE.month,DATE.day),
      "LTC":"https://coinmarketcap.com/currencies/litecoin/historical-data/?start=20130428&end={}{}{}".format(DATE.year,DATE.month,DATE.day),
      "BCH":"https://coinmarketcap.com/currencies/bitcoin-cash/historical-data/?start=20130428&end{}{}{}".format(DATE.year,DATE.month,DATE.day)
      }
'''
Create dataframe taking history from the site coinmarketcap.com
'''
def historical_data(data):
    url = data
    content = requests.get(url).content
    soup = BeautifulSoup(content,"html.parser")
    table = soup.find("table",{"class":"table"})
    data = [[td.text.strip() for td in tr.findChildren('td')]
        for tr in table.findChildren('tr')]
    df = pd.DataFrame(data)
    df.drop(df.index[0], inplace=True)
    df[0] =  pd.to_datetime(df[0])
    for i in range(1,7):
        df[i] = pd.to_numeric(df[i].str.replace(",","").str.replace("-",""))
    df.columns = ['Date','Open','High','Low','Close','Volume','Market Cap']
    df.set_index('Date',inplace=True)
    df.sort_index(inplace=True)
    return df
'''
Visualization of data by the schedule
'''
def visual(data,type,frm,to):
    data.sort_index()
    visual_data = data.loc[frm:to,[type]]
    visual_data.plot()
    plt.show()

parser = argparse.ArgumentParser()

parser.add_argument("Coin", type=str,
                    help="Enter a coin:BTC, XRP, ETH, LTC, BCH")
parser.add_argument("Type", type=str,
                    help="Enter a type:Open, High, Low, Close, Volume,Market_Cap")
parser.add_argument("Date_from", type=str,
                    help="Enter date from(format yyyy-mm-dd)")
parser.add_argument("Date_to", type=str,
                    help="Enter date to(format yyyy-mm-dd)")
args = parser.parse_args()
if args.Coin in DATA:
    link = DATA[args.Coin]
    inf = historical_data(link)
    visual(data = inf,type = args.Type,frm= args.Date_from,to = args.Date_to)
else:
    print("Unknown coin")
