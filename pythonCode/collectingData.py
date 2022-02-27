import os 
from binance.client import Client
import pandas as pd 
import datetime as dt
from calendar import monthrange

api_key = os.environ.get('binance_api_key')
api_secret = os.environ.get('binance_secret')

# we initialize our client and pass through the API key and secret.
client = Client(api_key, api_secret)

#Returns the number of days for a given month/year
def getDaysOfMonth(month , year):
    return monthrange(year , month)[1]

#Returns the data of a given crytpo for given dates / default dates
def getCryptoData(cryptoAbbreviation , interval , userStartDate = None):

    crypto = cryptoAbbreviation + "USDT"
    earliestStartDate = client._get_earliest_valid_timestamp(crypto , interval)
    earliestStartDate = dt.datetime.fromtimestamp(earliestStartDate/1000.0)
    userStartDate = dt.datetime.strptime(userStartDate , "%d %B, %Y")


    #If user enters a date smaller than whats available , just default to earliest possible
    if (userStartDate != None) and (userStartDate > earliestStartDate):
        
        #Grabbing the month and year from users inputted date
        day = userStartDate.day
        month = userStartDate.month
        year = userStartDate.year
        dates = getCryptoDates(day , month , year)
    
    else:

        print("Default Dates.")
        #Grabbing the earliest start date as default
        day = earliestStartDate.day
        month = earliestStartDate.month
        year = earliestStartDate.year
        dates = getCryptoDates(day , month , year)
    
    if (len(dates) > 1):
        #Grabbing the data for period between 2 date objects  , looping for amount of data we have then putting them all in list
        dfList = [ datesToDf ( crypto , interval , str(dates[i]) , str(dates[i+1] - dt.timedelta(0,1) ) ) for i in range (0 , len (dates) - 1 ) ]
        dfList = dfList + [ datesToDf ( crypto , interval , str(dates[-1]) ) ]
    
    else:
        dfList = [ datesToDf ( crypto , interval , str(dates[-1]) ) ]

    dfList = pd.concat(dfList)

    dfToCsv(dfList , cryptoAbbreviation , interval)

    return dfList

def datesToDf(crypto , interval , startDate , endDate=None):

    if (endDate != None):
        bars = client.get_historical_klines(crypto, interval, startDate , endDate , limit=1000)
    
    #If only after one day and not between 2 date objects
    else:
        bars = client.get_historical_klines(crypto, interval, startDate , limit=1000)

    #Deleting some variables returned from API
    for line in bars:
        del line[6:]

    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close' , 'volume'])
    df['date']=(pd.to_datetime(df['date'],unit='ms')) 

    #df.index = [dt.datetime.fromtimestamp(x /1000.0) for x in df.date]
    #df.drop(["date"], axis = 1, inplace = True) 
    #print(df.columns)
    return df

    
def getCryptoDates(day , month , year):

    currentYear = dt.date.today().year
    currentMonth = dt.date.today().month
    currentDay = dt.date.today().day
    allCryptoDates = []

    #When accepts users input
    while (currentYear != year) :

        if (day > 1):
            allCryptoDates.extend([dt.datetime(year , month , d ) for d in range(day , getDaysOfMonth(month , year)+1 )])
            month = month + 1 
            #resetting day after new month
            day=1
        
        allCryptoDates.extend([dt.datetime(year , m , 1 ) for m in range( month , 13)])
        #Resetting month for new year
        month = 1
        year=year+1
    
    #Creating date objects for the date range user wants and inserting into a list , everymonth or days if there are any
    if (currentYear == year ):

        if (currentMonth != month):

            if (day > 1):
                allCryptoDates.extend([dt.datetime(year , month , d ) for d in range(day , getDaysOfMonth(month , year)+1 )])
                month = month + 1
            
            allCryptoDates.extend([dt.datetime(year , m , 1 ) for m in range (month, currentMonth+1)])

        elif (day > 1):
            allCryptoDates.extend([dt.datetime(year , month , d ) for d in range(day , currentDay+1)])

        else:
            allCryptoDates.extend([dt.datetime(year , month , 1)])


    print(allCryptoDates)
    return allCryptoDates

def dfToCsv(df , cryptoAbbreviation , interval):

    #Getting the current directory this file is in.
    dir = os.path.dirname(__file__)

    #Create the relative file path where you want to save the data to.
    relative = ('../cryptoData/%s_%s_data.csv' % (cryptoAbbreviation , interval))

    filename = os.path.join(dir, relative)

    #Enter the relative path name you want to save the data to .
    df.to_csv(filename , index=False)

df = getCryptoData("XRP" , "1h" , "1 December, 1999")