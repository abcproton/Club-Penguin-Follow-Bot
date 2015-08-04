import logging
from collections import deque
from ConfigParser import ConfigParser

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from Penguin import Chinstrap
from Penguin import Penguin

# Creates client objects for initial handshake
class ClubPenguin(ClientFactory):

	"""
	The address of the login-server the client will connect to.
	"""
	serverAddress = "204.75.167.165:3724"

	def __init__(self):
		self.logger = logging.getLogger("Penguin")

		self.penguinFactory = PenguinFactory()

		self.queue = deque()

	def changeLoginServer(self, ip, port):
		self.serverAddress = "%s:%d" % ip, port

	def connect(self, **player):
		if "factory" not in player:
			player["factory"] = self.penguinFactory

		self.queue.append(player)

		ip, port = self.serverAddress.split(":")

		reactor.connectTCP(ip, int(port), self)

	def buildProtocol(self, address):
		player = self.queue.pop()

		loginInstance = Chinstrap(player)

		# Give the PenguinFactory instance an attribute
		loginInstance.factory = player["factory"]

		return loginInstance

	def clientConnectionLost(self, connector, reason):
		pass

	def clientConnectionFailed(self, connector, reason):
		self.logger.error("Connection failed: " + str(reason))

	def start(self):
		reactor.run()

class PenguinFactory(ClientFactory, object):

	# Used to track the status of current penguins (not currently used?)
	penguins = {}

	def __init__(self):
		self.logger = logging.getLogger("Penguin")

		self.servers = ConfigParser()
		self.servers.read(["Servers.ini"])

		self.queue = deque()

	# TODO: Add penguin to "penguins" dictionary!
	def connect(self, player):
		serverName = player.get("server")

		address = self.servers.get(serverName, "IP")
		port = self.servers.get(serverName, "Port")

		self.queue.append(player)

		reactor.connectTCP(address, int(port), self)

	def buildProtocol(self, address):
		player = self.queue.pop()

		penguin = Penguin(player)

		return penguin

	def clientConnectionFailed(self, connector, reason):
		self.logger.error("Connection failed: " + str(reason))