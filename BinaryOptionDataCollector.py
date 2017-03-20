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

        formattedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(element["lt_dts"], "%Y-%m-%dT%H:%M:%SZ")) # Reformat date
        tableName = element['e'] + ":" + element["t"] # Concatenate exchange and ticker for table name
        value = element["l"].replace(",", "") # Remove comma from price

        cursor = cnx.cursor(buffered=True)
        cursor.execute("SELECT * FROM BinaryOptionData.`" + tableName + "` WHERE `DateTime` = '" + formattedDate + "'")

        if cursor.rowcount == 0:

            print "Inserted: " + formattedDate + " " + tableName + " " + value

            cursor.execute("INSERT INTO `" + tableName + "` (`DateTime`, `Price`) VALUES (%s, %s)", (formattedDate, value))
            cnx.commit()

        else:

            print "Repeat: " + formattedDate + " " + tableName + " " + value

        cursor.close()

    time.sleep(60)

cnx.close()
