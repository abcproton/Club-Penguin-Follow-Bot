import json
import logging
from time import sleep
from urllib2 import Request, urlopen

from lxml import etree
from twisted.internet import defer, reactor
from twisted.protocols.basic import LineReceiver

from Crypto import Crypto
from Parser import Parser

class Spheniscidae(object, LineReceiver):

	delimiter = "\x00"

	# Used for caching phrase ids
	phrases = {}

	def __init__(self, player):
		self.logger = logging.getLogger("Penguin")

		for attribute in player:
			setattr(self, attribute, player[attribute])

		self.listeners = {
			"l": [self._handleLogin]
		}

	def connectionMade(self):
		# self.send("<policy-file-request/>")
		self.send("<msg t='sys'><body action='verChk' r='0'><ver v='153' /></body></msg>")
		self.send("<msg t='sys'><body action='rndK' r='-1'></body></msg>")

	"""
	Parses XML and world-server data and calls functions to handle the data.
	"""
	def lineReceived(self, data):
		#self.logger.info("Received data: " + data)

		if data.startswith("<"):
			data = etree.fromstring(data)[0]

			if data.get("action") == "rndK":
				self.randomKey = data.findtext("k")
				
				self.sendLogin()

		# World-server data is handled separately
		elif data.startswith("%"):
			if Parser.isValid(data):
				data = Parser.parseRaw(data)
				handler = data[1]

				if handler in self.listeners:
					for handlerCallback in self.listeners[handler]:
						handlerCallback(data)
	"""
	Adds a "listener" to the listeners' dictionary.

	A listener is basically a function that's called whenever is specific-type of packet is received.
	By default, the dictionary contains listeners for essential functionality such as logging in,
	joining a server, and joining a room.

	(As of now, it only contains one for logging in - "l")

	Here's an example of how you'd invoke this method:
	self.addListener("gi", self.handleGetInventory)

	The first parameter is the "id" of the packet -in this case, it's "gi". The "gi" packet contains
	the ids of the items the player owns.

	The second is simply the function that will handle that packet when it's received.

	Each packet can have an unlimited amount of listeners.
	"""
	def addListener(self, handler, callback):
		if handler not in self.listeners:
			self.listeners[handler] = [callback]
		else:
			self.listeners[handler].append(callback)

		return self # For chaining

	"""
	Just 'cause it's shorter and everyone in the community is probably more used to it.
	It automatically appends the null-byte to the end of the outgoing data.
	"""
	def send(self, data):
		#elf.logger.debug("Sending %s", data)
		self.sendLine(data)

class Chinstrap(Spheniscidae):

	def __init__(self, player):
		super(Chinstrap, self).__init__(player)

		self.player = player

	def sendLogin(self):
		loginHash = Crypto.getLoginHash(self.password, self.randomKey)

		self.send(
			"<msg t='sys'><body action='login' r='0'><login z='w1'>"
			"<nick><![CDATA[" + self.username + "]]></nick>"
			"<pword><![CDATA[" + loginHash + "]]></pword>"
			"</login></body></msg>"
		);

	def _handleLogin(self, data):
		rawPlayerString = data[3]
		rawPlayer = Parser.parseVertical(rawPlayerString)

		self.player["rawPlayerString"] = rawPlayerString
		self.player["rawPlayer"] = rawPlayer

		self.player["playerId"] = rawPlayer[0]
		self.player["loginKey"] = rawPlayer[3]
		self.player["confirmationHash"] = data[4]

		self.factory.connect(self.player)

		self.transport.loseConnection()

class Penguin(Spheniscidae):

	internalRoomId = "-1"

	def __init__(self, player):
		super(Penguin, self).__init__(player)

		self.addListener("jr", self._handleJoinRoom)

	def sendLogin(self):
		passwordHash = Crypto.encryptPassword(self.loginKey + self.randomKey) + self.loginKey

		self.send(
			"<msg t='sys'><body action='login' r='0'><login z='w1'>"
			"<nick><![CDATA[" + self.rawPlayerString + "]]></nick>" 
			"<pword><![CDATA[" + passwordHash + "#" + self.confirmationHash + "]]></pword>"
			"</login></body></msg>"
		)

	def _handleLogin(self, data):
		self.logger.info("A bot logged on")

		self.sendXt("s", "j#js", self.playerId, self.loginKey, "en")
		self.sendXt("s", "g#gi")

	# For now, this is literally all it does
	def _handleJoinRoom(self, data):
		self.internalRoomId = data[2]

	"""
	Usage example
		self.sendXt("s", "i#ai", 413) = %xt%s%i#ai%2%413%

	This method can probably be improved.
	"""
	def sendXt(self, category, id, *args):
		# Makes sure that all of the values in *args are strings
		parameters = "%".join(str(x) for x in args)
		parameters = self.internalRoomId + "%" + parameters

		data = "%xt%" + category + "%" + id + "%" + parameters + "%"
		self.send(data)

	# Tasks

	def buyInventory(self, id):
		self.sendXt("s", "i#ai", id)

	def sendPosition(self, x, y):
		self.sendXt("s", "u#sp", x, y)

	def joinRoom(self, id, x=0, y=0):
		self.sendXt("s", "j#jr", id, x, y)

	def findBuddy(self, id):
                self.sendXt("s", "u#bf", id)

        def sendFrame(self, id):
                self.sendXt("s", "u#sf", id)

        def sendEmote(self, id):
                self.sendXt("s", "u#se", id)

        def sendSnowball(self, x, y):
                self.sendXt("s", "u#sb", x, y)

        def sendAction(self, id):
                self.sendXt("s", "u#sa", id)

        def sendSafeMessage(self, id):
                self.sendXt("s", "u#ss", id)

        def sendJoke(self, id):
                self.sendXt("s", "u#sj", id)
                
	# Doesn't (always?) work
	def sendMessage(self, msg):
		self.sendXt("s", "m#sm", msg)

        # To be used in conjunction with getPhraseId
	def sendPhrase(self, id):
		self.sendXt("s", "m#pcam", id)

	def getPlayerInfoByName(self, name):
		self.sendXt("s", "u#pbn", name)

	"""
	Retrieves phrase chat id of msg for use with the pcam packet.
	Do NOT call this method directly; use getPhraseId instead.
	"""
	def retrievePhraseId(self, d, msg):
		data = {
			"language": "en", 
			"original_text": msg, 
			"product": "pen"
		}

		headers = {
			"Authorization": "FD 08306ECE-C36C-4939-B65F-4225F37BD296:905664F40E29B95CF5810B2ACA85497C7430BB1498E74B52",
			"Referer": "http://media1.clubpenguin.com/play/v2/client/phrase_autocomplete.swf?clientVersion=19313"
		}

		req = Request("https://api.disney.com/social/autocomplete/v2/search/messages", json.dumps(data), headers)

		try:
			handler = urlopen(req)
			response = handler.read()
			id = json.loads(response)["id"]

			d.callback((id, msg))
		except Exception as ex:
			d.errback(ex)

	"""
	Creates a deferred thread then calls retrievePhraseId.
	The thread's object is returned so that the end-user may 
	attach callbacks to it.
	"""
	def getPhraseId(self, msg):
		d = defer.Deferred()
		reactor.callWhenRunning(self.retrievePhraseId, d, msg)

		return d

	# Caches the result and sends the phrase
	def receivedPhraseId(self, result):
		id, msg = result

		if msg not in self.phrases:
			self.phrases[msg] = id

		self.sendPhrase(id)

	# Just in case something goes wrong while fetching the id
	def failedPhraseId(self, ex):
		errorMessage = str(ex)

		self.logger.error("Failed to retrieve phrase id: {0}".format(errorMessage))

	"""
	Sends the phrase if it's cached. If it isn't, we retrieve it, then
	send it. It also gets cached so that we don't have to do it again.
	"""
	def sendPhraseMessage(self, msg):
		if msg not in self.phrases:
			d = self.getPhraseId(msg)
			d.addCallback(self.receivedPhraseId)
			d.addErrback(self.failedPhraseId)
		else:
			id = self.phrases[msg]
			self.sendPhrase(id)
