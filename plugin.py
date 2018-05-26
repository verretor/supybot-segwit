import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import json
import requests

class Segwit(callbacks.Plugin):
    threaded = True

    def segwit(self, irc, msg, args):
        timeout = False
        segwit_usage = '0.0%'
        str_out = ''

        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
        sess = requests.session()
        sess.headers = headers

        # Take Segwit data from transactionfee.info
        url = 'https://transactionfee.info/static/data/paymentsSegwit.csv'

        try:
            response = sess.get(url, headers=headers, timeout=30)
        except:
            timeout = True

        if timeout == False:
            if response.status_code == 200:
                # Segwit data comes in CSV format.
                # Segwit usage for today is the last column of the last row.

                csv_data = response.content
                last_row = csv_data.split('\n')[-2]
                segwit_usage = last_row.split(',')[-1]

                irc.reply(segwit_usage, prefixNick=False)
            else:
                str_out = 'Error ' + str(response.status_code)
                irc.reply(str_out, prefixNick=False)
        else:
            str_out = 'Connection timed out'
            irc.reply(str_out, prefixNick=False)

Class = Segwit

# vim:set shiftwidth=4 tabstop=4 expandtab:
