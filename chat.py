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
            self.getName(line)
        else:
            self.chat(line)

    def getName(self, name): 
        if self.users.has_key(name):
            self.sendLine("Username taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT" 
        
    def chat(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return MainChat(self.users) 


reactor.listenTCP(1025, ChatFactory())
reactor.run()