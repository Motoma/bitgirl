#! /usr/bin/env python

import pickle
import time

from random import choice, random

import template

# Base statistics
EMOTIVENESS = 0.5
RESPONSIVENESS = 0.1
SHIFTINESS = 0.3
HOSTILITY = 0.05
LOVE = 0.01

# Taking queues from XKCD's Bucket
data_file = 'data/bucket.pk'
factoids = {}
substitutions = {}

# Dishing out hugs
love_verbs = ['hugs', 'snuggles up to', 'high-fives', 'tackles', 'dances with', 'gives a backrub to', 'gives an ice cream cone to', 'holds hands with', 'caresses', 'smothers', 'tickles', 'pinches', 'spanks', 'pushes', 'nudges', 'nuzzles', 'pokes']
love_acts = ['briming with joy', 'smiling from ear to ear', 'giggling with delight', 'hopping around playfully', 'showing her warmer side', 'very delicately', 'overflowing with kindness', 'warmly', 'blushing', 'shyly', 'bashfully', 'batting her eyelashes', 'grinning broadly', 'whistling happily']

# Bot rage
known_bots = ['CoreBot', 'DICBotV2', 'cbot_', 'ShaneKBot', 'DICtrivia', 'IshBot', 'N1tr0Bot', 'BetasBot']
br_verbs = ['headbutts', 'slaps', 'donkey-punches', 'kung-fu kicks', 'karate chops', 'stabs', 'shivs', 'bites', 'orangutan kicks', 'grumbles at', 'snarls at']
br_acts = ['wildly', 'vehemently', 'with great vigour', 'surreptitiously', 'without mercy', 'angrily', 'and eats a hot dog', 'and Jesus, then kicks a puppy', 'visciously, thoroughly unimpressed']

# Entrances
ent_verbs = ['bows', 'smirks', 'twirls', 'giggles', 'winks', 'screams joyously']
ent_acts = ['dances into the room', 'walks through the door', 'enters the chat', 'waves at you', 'gives you a high-five', 'flashes a smile']

# Emote reactions
reactions = ['blushes furiously at %s.', 'winks seductively at %s.', 'nods at %s in agreement.', 'give %s a thumbs up.', 'smiles at %s approvingly.', 'becomes shy around %s.', 'steps slowly away from %s.', 'thinks about %s and shudders.', 'stares at %s in utter disbelief.', 'gags at %s\'s antics.', 'thrusts suggestively in %s\'s direction.', 'slaps %s with all her might.']

def load_database():
    global factoids, substitutions
    data = open(data_file, 'r')
    factoids, substitutions = pickle.load(data)
    data.close()

def save_database():
    global factoids, substitutions
    data = open(data_file, 'w')
    pickle.dump((factoids, substitutions), data)
    data.close()    

try:
    load_database()
except:
    save_database()

def substitute(fact):
    global factoids, substitutions
    tokens = get_tokens(fact)
    for token in tokens:
        while substitutions.has_key(token) and token in fact:
            fact = fact.replace('$%s' %(token,), choice(substitutions[token]), 1)
    return fact

def get_tokens(fact):
    tokens = [] 
    spos = fact.find('$')
    while spos > -1:
        epos = len(fact)
        for end in [' ', ',', '.', ';', '?', '!', '$']:
            npos = fact.find(end, spos + 1, epos)
            if npos > -1:
                epos = npos
        tokens.append(fact[spos + 1:epos])
        spos = fact.find('$', epos)
    return tokens

def get_keywords(msg):
    keywords = []
    spos = msg.find('[')
    while spos > -1:
        epos = msg.find(']', spos + 4)
        if epos > -1:
            keywords.append(msg[spos + 1:epos])
        spos = msg.find('[', epos + 1)
    return keywords

class IRCScript(template.IRCScript):
    def joined(self, channel):
        if random() < EMOTIVENESS:
            self.send_describe(channel, '%s and %s.' % (choice(ent_verbs), choice(ent_acts)))

    def privmsg(self, user, channel, msg):
        if channel == self.nickname:
            self.direct_message(user, msg)
            self.learn(user, msg)
        else:
            # Someone is talking to me
            if self.nickname.lower() == msg[:len(self.nickname)].lower():
                msg = msg[len(self.nickname) + 1:].strip()
                self.react(user, channel, msg)
                self.learn(user, msg)
                
            elif ' hell ' in msg:
                self.send_msg(channel, msg.replace(' hell ', ' hello '))
            # WORDPLAY!
            elif channel != self.nickname and random() < SHIFTINESS:
                if self.nickname.lower() == msg[:len(self.nickname)].lower():
                    msg = msg[len(self.nickname) + 1:].strip()
                if 'the fucking ' in msg:
                    self.send_msg(channel, msg.replace('the fucking', 'fucking the'))
                elif ' exp' in msg:
                    self.send_msg(channel, msg.replace(' exp', ' assp'))
                elif ' ex' in msg:
                    self.send_msg(channel, msg.replace(' ex', ' sex'))
                elif ' variable' in msg:
                    self.send_msg(channel, msg.replace(' variable', ' constant'))
                elif 'do you know' == msg[:11].lower():
                    time.sleep(3 + random() * 6)
                    self.send_msg(channel, '%s: No, but if you hum a few bars I can fake it.' % (user,))
                elif 'pun' in msg.lower() and 'intended' in msg.lower():
                    time.sleep(3 + random() * 6)
                    self.send_msg(channel, '%s: Nobody cares if your puns were intended.' % (user,))

            # PEACE!
            elif random() < LOVE and user not in known_bots:
                time.sleep(3 + random() * 8)
                self.send_describe(channel, '%s %s, %s.' % (choice(love_verbs), user, choice(love_acts)))

            # RAGE!
            elif user in known_bots and random() < HOSTILITY:
                time.sleep(2 + random() * 5)
                self.send_describe(channel, '%s %s %s.' % (choice(br_verbs), user, choice(br_acts)))

            # I feel like responding
            elif random() < RESPONSIVENESS:
                self.react(user, channel, msg)
    
    def action(self, user, channel, data):
        if self.nickname.lower() in data.lower() and random() < RESPONSIVENESS:
            self.send_describe(channel, choice(reactions) % (user,))

    def learn(self, user, msg):
        global factoids, substitutions
        msg = msg.strip()
        keys = get_keywords(msg)
        msg = msg.replace('[', '').replace(']', '')
        if len(keys) > 0:
            for key in keys:
                key = key.lower()
                if not factoids.has_key(key):
                    factoids[key] = []
                factoids[key].append(msg)
            save_database()
        if msg[0] == '<' and '>' in msg[3:]:
            epos = msg.find('>')
            token = msg[1:epos]
            body = msg[epos + 1:].strip()
            if not substitutions.has_key(token):
                substitutions[token] = []
            substitutions[token].append(body.strip())
            save_database()

    def react(self, user, channel, msg):
        global factoids, substitutions
        msg = msg.lower()
        facts = []
        for x in factoids:
            if ' %s ' % (x,) in msg or msg[:len(x)] == x or msg[-len(x):] == x or msg[-len(x) - 1:-1] == x:
                for fact in factoids[x]:
                    facts.append(fact)
        if len(facts) > 0:
            time.sleep(3 + random() * 8)
            self.send_msg(channel, substitute(choice(facts)))

    def direct_message(self, user, msg):
        if msg[:11] == 'deletefact ':
            token = msg[11:].strip()
            if factoids.has_key(token):
                factoids.pop(token)
                save_database()
            else:
                self.send_msg(user, 'No factoid found: "%s"' % (token,))
        elif msg[:9] == 'showfact ':
            token = msg[9:].strip()
            if factoids.has_key(token):
                self.send_msg(user, '%s: %r' % (token, factoids[token]))
            else:
                self.send_msg(user, 'No factoid found: "%s"' % (token,))
        if msg[:11] == 'deletesubs ':
            token = msg[11:].strip()
            if substitutions.has_key(token):
                substitutions.pop(token)
                save_database()
            else:
                self.send_msg(user, 'No substitution found: "%s"' % (token,))
        elif msg[:9] == 'showsubs ':
            token = msg[9:].strip()
            if substitutions.has_key(token):
                self.send_msg(user, '%s: %r' % (token, substitutions[token]))
            else:
                self.send_msg(user, 'No substitution found: "%s"' % (token,))
        elif msg == 'ss':
            self.send_msg(user, '%r' % (substitutions.keys(),))
        elif msg == 'sf':
            self.send_msg(user, '%r' % (factoids.keys(),))
