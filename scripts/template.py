#! /usr/bin/env python

class IRCScript:
    def __init__(self, client):
        self.send_msg = client.msg
        self.send_describe = client.describe
        self.send_whois = client.whois
        self.nickname = client.nickname

    def privmsg(self, user, channel, msg): pass
    def joined(self, channel): pass
    def left(self, channel): pass
    def signedOn(self): pass
    def action(self, user, channel, data): pass
    def userJoined(self, user, channel): pass
    def userLeft(self, user, channel): pass
    def userQuit(self, user, quitMessage): pass
    def userKicked(self, kickee, channel, kicker, message): pass
    def msg(self, channel, msg): pass
    def describe(self, channel, data): pass
