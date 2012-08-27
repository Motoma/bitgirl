#! /usr/bin/env python

class IRCScript:
    def __init__(self, msg, describe, nickname):
        self.send_msg = msg
        self.send_describe = describe
        self.nickname = nickname

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
