#! /usr/bin/env python

# Unfinished.
# Use whois and http://www.hostip.info/use.html to report a user's location.

import template

class IRCScript(template.IRCScript):
    def privmsg(self, user, channel, msg):
        # Talking to me ?
        if msg[:len(self.nickname)] == self.nickname:
            # Grab the rest of the message
            msg = msg.split(' ', 1)[1].lower()
            if msg[:8] == "where is":
                user = msg.split(' ')[2]
            elif msg[:7] == "whereis":
                user = msg.split(' ')[1]
            data = self.send_whois(user)
            self.send_msg(channel, "querying %s" % (user))
            self.send_msg(channel, "%r" % (data))
