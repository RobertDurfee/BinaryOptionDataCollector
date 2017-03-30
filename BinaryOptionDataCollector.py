import urllib2
import json
import mysql.connector
import time

while True:

    try:

        url = 'http://finance.google.com/finance/info?q=INDEXDJX:.DJI,INDEXSP:.INX,INDEXNASDAQ:.IXIC,' \
              'INDEXRUSSELL:RUT,INDEXFTSE:XIN0,INDEXFTSE:UKX,INDEXFTSE:WIDEU,INDEXFTSE:JAPAN,CURRENCY:EURUSD,' \
              'CURRENCY:GBPUSD,CURRENCY:USDJPY,CURRENCY:EURJPY,CURRENCY:AUDUSD,CURRENCY:USDCAD,CURRENCY:GBPJPY,' \
              'CURRENCY:USDCHF,CURRENCY:EURGBP,CURRENCY:AUDJPY'

        cnx = mysql.connector.connect(user='<CENSORED>', password='<CENSORED>', host='<CENSORED>',
                                      database='BinaryOptionData')

        lastAddedDateTime = {'INDEXDJX:.DJI': '', 'INDEXSP:.INX': '', 'INDEXNASDAQ:.IXIC': '', 'INDEXRUSSELL:RUT': '',
                             'INDEXFTSE:XIN0': '', 'INDEXFTSE:UKX': '', 'INDEXFTSE:WIDEU': '', 'INDEXFTSE:JAPAN': '',
                             'CURRENCY:EURUSD': '', 'CURRENCY:GBPUSD': '', 'CURRENCY:USDJPY': '', 'CURRENCY:EURJPY': '',
                             'CURRENCY:AUDUSD': '', 'CURRENCY:USDCAD': '', 'CURRENCY:GBPJPY': '', 'CURRENCY:USDCHF': '',
                             'CURRENCY:EURGBP': '', 'CURRENCY:AUDJPY': ''}

        # Initialize last added datetimes
        for tableName in lastAddedDateTime:

            query = "SELECT `DateTime` FROM BinaryOptionData.`" + tableName + "` WHERE `ID` = (SELECT MAX(ID) FROM `" \
                    + tableName + "`)"

            cursor = cnx.cursor()
            cursor.execute(query)

            for (dateTime,) in cursor:

                lastAddedDateTime[tableName] = dateTime.strftime("%Y-%m-%d %H:%M:%S")

            cursor.close()

        while True:

            response = urllib2.urlopen(url)
            html = response.read()

            html = html[4:]  # Remove the prefix '//'

            html = html.decode('utf-8', 'ignore').encode('utf-8')  # Remove non-ascii characters

            data = json.loads(html)

            for element in data:

                formattedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(element["lt_dts"],
                                                                                 "%Y-%m-%dT%H:%M:%SZ"))  # Reformat date
                tableName = element['e'] + ":" + element["t"]  # Concatenate exchange and ticker for table name
                value = element["l"].replace(",", "")  # Remove comma from price

                if lastAddedDateTime[tableName] != formattedDate:

                    query = "INSERT INTO `" + tableName + "` (`DateTime`, `Price`) VALUES (%s, %s)"

                    cursor = cnx.cursor()
                    cursor.execute(query, (formattedDate, value))
                    cnx.commit()
                    cursor.close()

                    lastAddedDateTime[tableName] = formattedDate

            time.sleep(60)  # Do not remove this! Your IP will be blocked.

        cnx.close()

    except mySQLConnectionError:

        continue
