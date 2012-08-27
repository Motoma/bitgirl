Introducing bitgirl
===================

BitGirl is a fully pluggable IRC bot which allows dynamic command and module loading, unloading, and reloading on the fly, without rebooting. This allows for highly dynamic behavior with seamless updates, granting the plugin developer an extremely high turn around rate for the code-compile-test cycle.

BitGirl was written as an entry to the Dream.In.Code IRC Competition (http://www.dreamincode.net/forums/topic/238097-irc-competition/).

When started, she connects to irc.efnet.org and joins #MotomaBot. She then waits for commands to be sent to her via direct message.

The commands she allows by default are:

    load <script>: loads a script from the plugin directory. (ex. /msg BitGirl load bucket)
    unload <script>: unloads a script and clears any saved state from memory (ex. /msg BitGirl unload bucket)
    reload <script>: reloads a script and clears any saved state from memory (ex. /msg BitGirl reload bucket)
    list: lists loaded and available scripts (ex. /msg BitGirl list)
    join <channel>: causes BitGirl to join a channel (ex. /msg BitGirl join #DreamInCode)
    leave <channel>: causes BitGirl to leave a channel (ex. /msg BitGirl leave#DreamInCode)

Everything else about BitGirl is modular, and controlled through various included plugins.

    bucket: Emulates some of #XKCD's Bucket's behavior.
    cakefart: You may have seen this one in the chat...
    logger: logs all activity to the command line.
    thegame: Awards players XP based on behavior in the chat. Scores are stored in the data directory.
    trivia: Abruptly subverts people trying to play SuperCore's bot's trivia (which never was completed, btw).

Bucket
------

bucket is a program in and of itself. Essentially, it falls into two parts: personality, fact memory, and responsiveness.

Personality and responsiveness are hard coded. BitGirl will go out of her way to cheer up people and harass bots. Additionally, she responds directly to emotes that involve her.

Fact memory on the other hand is much more in-depth. bucket allows BitGirl to learn and forget pieces of information about topics. These are entirely controlled by users in the channels she is in, and are stored between reboots and rejoins in an SQLite database (in the data directory). When BitGirl hears something she knows about, there is a chance that she will respond with a factoid.

You can teach BitGirl a fact by using the [] to highlight a keyword. For instance:

    <Motoma> BitGirl: [Java] is the reason I have [nightmare]s.
    ...
    <Dogstoppe> I had this mad nightmare last night.
    <BitGirl> Java is the reason I have nightmares.

You can have multiple factoids per word, and multiple words per factoid.

Additionally, BitGirl can substitute words:

    <Motoma> BitGirl: <verbing> punching
    <Motoma> BitGirl: <nouns> trees
    <Motoma> BitGirl: [I love] $verbing $nouns.
    ...
    <Dogstoppe> I love DreamInCode.
    <BitGirl> I love punching trees.

There is a significant number of factoids stored in data/bucket.pk. 

The Way Bot Programming Should Be
---------------------------------

The pluggable architecture allows even the python novice to begin developing a bot in my framework. You may simply create a script in the scripts folder, and in it, inherit from template.IRCScript. From there, you build callbacks for each of the IRC events. For instance, the logger script, in its entirety:

~~~~~ python
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
~~~~~

The list of inherited and overridable supported callbacks are:

    privmsg: Called any time the bot receives a private message
    joined: Called any time the bot joins a channel.
    left: Called any time the bot leaves a channel.
    signedOn: Called any time the bot connects to a server.
    action: Called any time the someone performs an emote in a channel the bot is in (/me dances wildly)
    userJoined: Called when a user joins a channel the bot is in.
    userLeft: Called when a user leaves a channel the bot is in.
    userQuit: Called when a user quits from a channel the bot is in.
    userKicked: Called when a user is kicked from a channel the bot is in.
    msg: Called whenever a user talks in a channel the bot is in.
    describe: Called whenever the bot performs an emote.

Additionally, any child for the IRCScript can use the send_msg and send_describe to talk and emote in a channel.
