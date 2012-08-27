#! /usr/bin/env python

import random
import time

import template

TRIVIA_BOT = 'DICtrivia'
ANSWER = ':trivia answer'
NEXT = ':trivia next'
Q_A = {
    '___________ is commonly referred to as politically motivated hacking.' : 'Hacktivism',
    'In m-commerce, the hyped evolution of e-commerce, what does the M stand for?' : 'Mobile',
    'What does ASP mean to online auctions using it to determine fees?' : 'Average Sales Price',
}

class IRCScript(template.IRCScript):
    def privmsg(self, user, channel, msg):
        if user == TRIVIA_BOT:
            question = msg.strip()
            if question in Q_A:
                self.send_msg('%s %s' % (ANSWER, Q_A[question]))
                time.sleep(random.randint(15, 60))
                self.send_msg(NEXT)

                              
