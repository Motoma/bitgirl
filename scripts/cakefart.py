#! /usr/bin/env python

import time
import random

import template

class IRCScript(template.IRCScript):
    def privmsg(self, user, channel, msg):
        if random.random() < 0.001:
            self.send_describe(channel, 'grabs a delicious looking chocolate cake out of the refridgerator.')
            time.sleep(2)
            self.send_describe(channel, 'cuts up the cake, counting out one piece for each person in the room.')
            time.sleep(0.5)
            self.send_describe(channel, 'turns around and loudly FARTS on your piece of cake!')
            
        

        
