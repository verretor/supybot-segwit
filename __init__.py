
"""
Gives average Segwit transaction percentage in the last 144 blocks.
"""

import supybot
import supybot.world as world

__version__ = "0.1"

supybot.authors.verretor = supybot.Author('Benoit Verret', 'verretor', 'benoit.verret@protonmail.ch')
__author__ = supybot.authors.verretor

# This is a url where the most recent plugin package can be downloaded.
__url__ = 'https://github.com/verretor/supybot-segwit' 

import config
import plugin
reload(plugin) # In case we're being reloaded.
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    import test

Class = plugin.Class
configure = config.configure


