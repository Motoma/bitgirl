#! /usr/bin/env python

import template

class IRCScript(template.IRCScript):
    def privmsg(self, user, channel, msg):
        print(' [%s] <%s> %s' % (channel, user, msg))
    def action(self, user, channel, data):
        print(' [%s] * %s %s' % (channel, user, data))
    def userJoined(self, user, channel):
        print('J[%s] * %s has joined the channel.' % (channel, user))
    def userLeft(self, user, channel):
        print('L[%s] * %s has left the channel.' % (channel, user))
    def userQuit(self, user, quitMessage):
        print('Q * %s has quit (%s).' % (user, quitMessage))
    def userKicked(self, kickee, channel, kicker, message):
        print('K[%s] * %s has kicked %s from the channel (%s).' % (channel, kicker, kickee, message))
    def msg(self, channel, msg):
        print(' [%s] <%s> %s' % (channel, self.nickname, msg))
    def describe(self, channel, data):
        print(' [%s] * You %s' % (channel, data))



