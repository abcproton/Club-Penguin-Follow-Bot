from Penguin.ClubPenguin import ClubPenguin
from Penguin.Penguin import Penguin
from Penguin.ClubPenguin import PenguinFactory

'''
Followbot Script - CPKarth123
Penguin (PCL) - Aurora (Arthur)
'''

class MyPenguin(Penguin):
        
        def __init__(self, player, offset_x, offset_y):
                super(MyPenguin, self).__init__(player)
                
                self.name = 'Breptnb' #Change this to the penguin you wish to follow!
                self.mixTarget = '' 

                self.offset_x = offset_x
                self.offset_y = offset_y
                
                self.addListener("sp", self.handleMove) 
                self.addListener("se", self.handleEmote)
                self.addListener("sm", self.handleMessage)
                self.addListener("ss", self.handleSafeMessage)
                self.addListener("sb", self.handleSnowball)
                self.addListener("sf", self.handleFrame)
                self.addListener("sa", self.handleAction)
                self.addListener("jr", self.handleJoinRoom)
                self.addListener("pbn",self.handlePlayerByName)
                self.addListener("bf", self.handleBf)
                self.addListener("rp", self.handleRp)
                
                
        def handleMove(self, data):
                if data[3] == self.mixTarget:
                        self.sendPosition(int(data[4]) + self.offset_x, int(data[5]) + self.offset_y)
                        
        def handleEmote(self, data):
                if data[3] == self.mixTarget:
                       self.sendEmote(data[4])

        def handleMessage(self, data):
                if data[3] == self.mixTarget:
                        self.sendPhraseMessage(data[4])

        def handleSafeMessage(self, data):
                if data[3] == self.mixTarget:
                        self.sendSafeMessage(data[4])

        def handleSnowball(self, data):
                if data[3] == self.mixTarget:
                        self.sendSnowball(data[4], data[5])

        def handleFrame(self, data):
                if data[3] == self.mixTarget:
                        self.sendFrame(data[4])

        def handleAction(self, data):
                if data[3] == self.mixTarget:
                        self.sendAction(data[4])

        def handleJoinRoom(self, data):
                self.getPlayerInfoByName(self.name)

        
        def handlePlayerByName(self, data):
                self.mixTarget = data[4]
                self.findBuddy(self.mixTarget)

        def handleBf(self, data):
                if data[3] == '-1':
                        self.logger.error("Target is offline!")
                        exit()
                self.joinRoom(data[3])

        def handleRp(self, data):
               if data[3] == self.mixTarget:
                        self.findBuddy(self.mixTarget)

class FollowBotFactory(PenguinFactory):

        def __init__(self, offset_x=0, offset_y=0):
                self.offset_x = offset_x
                self.offset_y = offset_y
                super(FollowBotFactory, self).__init__()

                self.logger.debug("FollowBotFactory constructed")

        def buildProtocol(self, addr):
                player = self.queue.pop()
                
                penguin = MyPenguin(player, self.offset_x, self.offset_y)

                return penguin


cp = ClubPenguin()

accounts = []
for account in open("accounts.txt", "r").read().split("\n"):
        if account!= "":
                accounts.append(dict({"username":account.split(":")[0], "password":account.split(":")[1]}))
        else:
                break

'''
Cube Formation
'''

cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server="Ice Pond", \
        factory=FollowBotFactory(45,0))

cp.connect(username=accounts[1]["username"], password=accounts[1]["password"], server="Ice Pond", \
        factory=FollowBotFactory(-45,0))

cp.connect(username=accounts[2]["username"], password=accounts[2]["password"], server="Ice Pond", \
        factory=FollowBotFactory(45,45))

cp.connect(username=accounts[3]["username"], password=accounts[3]["password"], server="Ice Pond", \
        factory=FollowBotFactory(45,-45))

cp.connect(username=accounts[4]["username"], password=accounts[4]["password"], server="Ice Pond", \
        factory=FollowBotFactory(0,45))

cp.connect(username=accounts[5]["username"], password=accounts[5]["password"], server="Ice Pond", \
        factory=FollowBotFactory(0,-45))

cp.connect(username=accounts[6]["username"], password=accounts[6]["password"], server="Ice Pond", \
        factory=FollowBotFactory(-45,-45))

cp.connect(username=accounts[7]["username"], password=accounts[7]["password"], server="Ice Pond", \
        factory=FollowBotFactory(-45,45))


cp.start()
