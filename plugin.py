import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from random import choice

import json
import requests

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def is_number(test_str):
  try:
    float(test_str)
  except ValueError, e:
    return False
  return True

def parse_segwit(json_data):
    segwit = '0.0%'
    total_segwit = 0.0
    total_tx = 0.0
    day_average = 0.0

    if is_json(json_data):
        lst_segwit = json.loads(json_data)
    else:
        return('HTTP response is not a valid JSON.')

    if not isinstance(lst_segwit, list):
        return('JSON is broken and should contain a list of blocks.')

    if len(lst_segwit) < 144:
        return('Not enough blocks.')

    # 144 blocks is approximately 1 day.
    for i in range(0, 144):
        if not 'txsegwit' or not 'txtotal' in lst_segwit[i]:
            return('JSON is broken.')
        if not is_number(lst_segwit[i][u'txsegwit']):
            return('JSON is broken (txsegwit).')
        if not is_number(lst_segwit[i][u'txtotal']):
            return('JSON is broken (txtotal).')
        total_segwit += float(lst_segwit[i][u'txsegwit'])
        total_tx += float(lst_segwit[i][u'txtotal'])

    if total_tx == 0:
        return('Cannot divide by 0.')
    day_average = total_segwit / total_tx * 100
    segwit = str(day_average) + '%'

    return(segwit)

class Segwit(callbacks.Plugin):
    """Add the help for "@plugin help Segwit" here
    This should describe *how* to use this plugin."""
    threaded = True

    def segwit(self, irc, msg, args):
        timeout = False
        segwit_usage = '0.0%'
        str_out = ''

        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'
        sess = requests.session()
        sess.headers = headers

        # This is where segwit.party/charts data is.
        url = 'http://enyo.gk2.sk/data.json'

        try:
            response = sess.get(url, headers=headers, timeout=30)
        except:
            timeout = True

        if timeout == False:
            if response.status_code == 200:
                json_data = response.content
                segwit_usage = parse_segwit(json_data)

                irc.reply(segwit_usage, prefixNick=False)
            else:
                str_out = 'Error ' + str(response.status_code)
                irc.reply(str_out, prefixNick=False)
        else:
            str_out = 'Connection timed out'
            irc.reply(str_out, prefixNick=False)

Class = Segwit

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
