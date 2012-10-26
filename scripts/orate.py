#! /usr/bin/env python
#
# Orate.py will cause bitgirl to speak everything that others say in
# all channels she is in, including private messages.
# Notes:
#   - THIS IS UNSAFE. The technique used is issuing SmallTalk commands to 
#     the festival interactive environment. I am not a SmallTalk afficianado
#     and cannot claim that all strings are properly escaped. There is a very
#     real potential for remote execution using this plugin.
#   - Requires Festival for TTS: http://www.cstr.ed.ac.uk/projects/festival/
#   - Defaults to cmu_us_awb_arctic_clunits which is not part of the standard
#     Festival distribution.

# Path to the festival binary
FESTIVAL = '/home/cgilbert/code/personal/festival/festival/bin/festival'
# kal_diphone and rab_diphone are typical voices are both available in the
# festival download section, ARCTIC voice databases, including the one below
# can be found at: http://www.speech.cs.cmu.edu/cmu_arctic/packed/
VOICE = 'cmu_us_awb_arctic_clunits'

import subprocess

import template

class IRCScript(template.IRCScript):
    def __init__(self, *args):
        template.IRCScript.__init__(self, *args)

        self.festival = subprocess.Popen([FESTIVAL], stdin=subprocess.PIPE)
        self.festival.stdin.write('(voice_%s)\n' % (VOICE))

    def privmsg(self, user, channel, msg):
        self.say_text(msg)

    def say_text(self, message):
        # Don't think multiline strings are allowed, but just to be safe
        safe = message.replace('"', '\"').replace('\n', ' ').replace('\r', ' ')
        self.festival.stdin.write('(SayText "%s")\n' % (safe))

    def quit(self):
        self.festival.communicate('(quit)\n')

    def __del__(self, *args):
        self.quit()
