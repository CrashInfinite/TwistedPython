from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class MainChat(LineReceiver):

    def __init__(self, users):
        self.conns = conns
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("Please choose a username")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):http://en.wikipedia.org/wiki/John_Malkovich
        if self.users.has_key(name):
            self.sendLine("Username taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return MainChat(self.users) 


reactor.listenTCP(1025, ChatFactory())
reactor.run()