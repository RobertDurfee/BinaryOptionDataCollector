import urllib2
import json
import mysql.connector
import time

url = 'http://finance.google.com/finance/info?q=INDEXDJX:.DJI,INDEXSP:.INX,INDEXNASDAQ:.IXIC,INDEXRUSSELL:RUT,INDEXFTSE:XIN0,INDEXFTSE:UKX,INDEXFTSE:WIDEU,INDEXFTSE:JAPAN,CURRENCY:EURUSD,CURRENCY:GBPUSD,CURRENCY:USDJPY,CURRENCY:EURJPY,CURRENCY:AUDUSD,CURRENCY:USDCAD,CURRENCY:GBPJPY,CURRENCY:USDCHF,CURRENCY:EURGBP,CURRENCY:AUDJPY'

cnx = mysql.connector.connect(user='<CENSORED>', password='<CENSORED>', host='<CENSORED>', database='BinaryOptionData')

while True:

    response = urllib2.urlopen(url)
    html = response.read()
    
    html = html[4:] # Remove the prefix '//'

    html = html.decode('utf-8', 'ignore').encode('utf-8') # Remove non-ascii characters

    data = json.loads(html)

    for element in data:

        cursor = cnx.cursor()
        cursor.execute("INSERT INTO `" + element['e'] + ":" + element["t"] + "` (`DateTime`, `Price`) VALUES (%s, %s)", (time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(element["lt_dts"], "%Y-%m-%dT%H:%M:%SZ")), element["l"].replace(",", "")))
        cnx.commit()
        cursor.close()

        print element['lt'] + ' ' + element['e'] + ":" + element['t'] + ' ' + element['l']

    time.sleep(60)

cnx.close()
