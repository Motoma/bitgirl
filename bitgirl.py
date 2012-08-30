#! /usr/bin/env python

import os
import sys

from twisted.internet import protocol
from twisted.internet import reactor
from twisted.words.protocols import irc

# IRC info
CHAN = '#dreamincode'
CHAN = '#MotomaBot'
SERVER = 'irc.efnet.org'
PORT = 6667
NICK = 'BitGirl'

# Dynamically loaded script configuration
script_dir = 'scripts'
initial_load = ['logger', 'bucket', 'thegame']

# Helpers
def clean_user(user):
    return user.split('!')[0]

loaded_modules = {}

# Main class
class DICBot(irc.IRCClient):
    def connectionMade(self):
        # Load initial scripts
        for module_name in initial_load:
            module = __import__(module_name)
            loaded_modules[module_name] = module.IRCScript(self)
        irc.IRCClient.connectionMade(self)

    def _get_nickname(self):
        return self.factory.nickname
    def _get_channel(self):
        return self.factory.channel

    nickname = property(_get_nickname)
    channel = property(_get_channel)

    def privmsg(self, user, channel, msg):
        user = clean_user(user)
        for module in loaded_modules:
            loaded_modules[module].privmsg(user, channel, msg)

        # Direct message to bot
        if channel.lower() == self.nickname.lower():
            if msg.lower() == 'list':
                a_mods = []
                i_mods = []
                modules = os.listdir(script_dir)
                modules = [module[:-3] for module in modules 
                           if module[-3:] == '.py' and module != 'template.py']
                for module in modules:
                    if module in loaded_modules.keys():
                        i_mods.append(module)
                    else:
                        a_mods.append(module)
                self.msg(user, 'The following modules are installed: %s.' % (
                        ', '.join(i_mods,)))
                self.msg(user, 'The following modules are available: %s.' % (
                        ', '.join(a_mods,)))
            elif msg.lower()[0:5] == 'load ':
                module = __import__(msg[5:])
                reload(module)
                loaded_modules[msg[5:]] = module.IRCScript(self)
            elif msg.lower()[:7] == 'unload ':
                loaded_modules.pop(msg[7:])
            elif msg.lower()[:7] == 'reload ':
                loaded_modules.pop(msg[7:])
                module = __import__(msg[7:])
                reload(module)
                loaded_modules[msg[7:]] = module.IRCScript(self)
            elif msg.lower()[:5] == 'join ':
                self.join(msg[5:])
            elif msg.lower()[:6] == 'leave ':
                self.leave(msg[6:], reason='Instructed by %s.' % (user,))

    def joined(self, channel):
        for module in loaded_modules:
            loaded_modules[module].joined(channel)

    def left(self, channel):
        for module in loaded_modules:
            loaded_modules[module].left(channel)

    def signedOn(self):
        self.join(self.channel)
        print("Signed on as %s." % (self.nickname,))
        for module in loaded_modules:
            loaded_modules[module].signedOn()

    def action(self, user, channel, data):
        user = clean_user(user)
        for module in loaded_modules:
            loaded_modules[module].action(user, channel, data)

    def userJoined(self, user, channel):
        user = clean_user(user)
        for module in loaded_modules:
            loaded_modules[module].userJoined(user, channel)

    def userLeft(self, user, channel):
        user = clean_user(user)
        for module in loaded_modules:
            loaded_modules[module].userLeft(user, channel)

    def userQuit(self, user, quitMessage):
        user = clean_user(user)
        for module in loaded_modules:
            loaded_modules[module].userQuit(user, quitMessage)

    def userKicked(self, kickee, channel, kicker, message):
        kickee = clean_user(kickee)
        kicker = clean_user(kicker)
        for module in loaded_modules:
            loaded_modules[module].userKicked(kickee, channel, kicker, message)

    def msg(self, channel, msg):
        for module in loaded_modules:
            loaded_modules[module].msg(channel, msg)
        irc.IRCClient.msg(self, channel, msg)

    def describe(self, channel, data):
        for module in loaded_modules:
            loaded_modules[module].describe(channel, data)
        irc.IRCClient.describe(self, channel, data)

# Class factory
class DICBotFactory(protocol.ClientFactory):
    protocol = DICBot

    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print('Lost connection (%s), reconnecting.' % (reason,))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print('Cound not connect: %s' % (reason,))

# Main code execution
if __name__ == '__main__':
    sys.path.append('./%s' % (script_dir))

    if len(sys.argv) > 1: SERVER = sys.argv[1]
    if len(sys.argv) > 2: PORT = sys.argv[2]

    # Launch bot
    reactor.connectTCP(SERVER, PORT, DICBotFactory(CHAN, NICK))
    reactor.run()
