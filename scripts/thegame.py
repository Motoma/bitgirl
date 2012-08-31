#! /usr/bin/env python

import pickle
import time

import template

# 20 levels of doom and destruction!
data_file = 'data/thegame.pk'
scores = {}
levels = [15 * 3 ** i for i in range(20)]

def load_database():
    global scores
    data = open(data_file, 'r')
    scores = pickle.load(data)
    data.close()

def save_database():
    global scores
    data = open(data_file, 'w')
    pickle.dump(scores, data)
    data.close()    

try:
    load_database()
except:
    save_database()

class IRCScript(template.IRCScript):
    def privmsg(self, user, channel, msg):
        global scores, levels

        if not scores.has_key(user):
            scores[user] = 0

        if msg.lower() == 'lol' or 'lol ' in msg.lower() or ' lol' in msg.lower():      
            scores[user] -= 5
        elif channel == self.nickname:
            if msg == 'score':
                cur = scores[user]
                for level in range(len(levels)):
                    if levels[level] > cur:
                        break
                if level < len(levels) - 2:
                    next = levels[level]
                else:
                    next = 2**64
                self.send_msg(user, 'You are currently level %i. You are %i/%ixp to level %i.' % (level, cur, next, level + 1))
        elif '[' in msg and ']' in msg:
            for i in range (10):
                scores[user] += 1

                if scores[user] in levels:
                    level = levels.index(scores[user]) + 1
                    self.send_msg(channel, '*** Congratulations to %s, who has acquired level %i!!!***' % (user, level))

            save_database()
        else:
            scores[user] += 1

            if scores[user] in levels:
                level = levels.index(scores[user]) + 1
                self.send_msg(channel, '*** Congratulations to %s, who has acquired level %i!!!***' % (user, level))

            save_database()

    def action(self, user, channel, msg):
        if not scores.has_key(user):
            scores[user] = 0

        scores[user] += 1
        if scores[user] in levels:
            level = levels.index(scores[user]) + 1
            self.send_msg(channel, '*** Congratulations to %s, who has acquired level %i!!!***' % (user, level))

        scores[user] += 1
        if scores[user] in levels:
            level = levels.index(scores[user]) + 1
            self.send_msg(channel, '*** Congratulations to %s, who has acquired level %i!!!***' % (user, level))

        save_database()
        

        
