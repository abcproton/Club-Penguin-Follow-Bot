from Penguin.ClubPenguin import ClubPenguin
from Penguin.Penguin import Penguin
from Penguin.ClubPenguin import PenguinFactory

'''
FollowBot Script - CPKarth123 
Penguin (PCL) - Aurora (Arthur)
Version: 5.0 - http://rile5.com/topic/38164-cp-follow-bot-python-penguin/
'''

penguin = raw_input("TARGET PENGUIN -> ") 
server = raw_input("SERVER OF TARGET PENGUIN -> ")
print '''
Formations:
    -Star
    -Swastika
    -Cube
    -Circle
    -GAY
    -Raid
    -No Offset
'''
formation = raw_input("FORMATION -> ")

class MyPenguin(Penguin):
        
        def __init__(self, player):
                super(MyPenguin, self).__init__(player)

                self.player = player

                self.name = ''
                self.mixTarget = ''

                self.offset_x = 0
                self.offset_y = 0
                
                self.isHoldingNewspaper = False
                self.isHoldingBlueprint = False

                self.addListener("sp", self.handleMove) 
                self.addListener("se", self.handleEmote)
                self.addListener("sm", self.handleMessage)
                self.addListener("ss", self.handleSafeMessage)
                self.addListener("sj", self.handleJoke)
                self.addListener("sb", self.handleSnowball)
                self.addListener("sf", self.handleFrame)
                self.addListener("sa", self.handleAction)
                self.addListener("jr", self.handleJoinRoom)
                self.addListener("pbn",self.handlePlayerByName)
                self.addListener("bf", self.handleBf)
                self.addListener("rp", self.handleRp)
                self.addListener("e", self.handleError)
                
        def handleMove(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> MOVED: " + data[4] + " " + data[5] 
                        self.sendPosition(int(data[4]) + self.offset_x, int(data[5]) + self.offset_y)
                        
        def handleEmote(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT EMOTE: " + data[4]
                        self.sendEmote(data[4])

        def handleMessage(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT MESSAGE: " + data[4]
                        self.sendPhraseMessage(data[4]) # Doesn't work if penguin is not activated!
                        
                        if data[4] == "blueprint" and self.isHoldingBlueprint == False:
                                self.sendBlueprint()
                                print "BOT >> SENT BLUEPRINT" 
                                self.isHoldingBlueprint = True
                                self.isHoldingNewspaper = False
                                
                        elif data[4] == "blueprint" and self.isHoldingBlueprint == True:
                                self.joinRoom(912)
                                self.joinRoom(self.currentRoomID)
                                print "BOT >> RESTARTED" 
                                self.isHoldingBlueprint = False

                        if data[4] == "newspaper" and self.isHoldingNewspaper == False:
                                self.sendNewspaper()
                                print "BOT >> SENT NEWSPAPER" 
                                self.isHoldingNewspaper = True
                                self.isHoldingBlueprint = False

                        elif data[4] == "newspaper" and self.isHoldingNewspaper == True:
                                self.joinRoom(912)
                                self.joinRoom(self.currentRoomID)
                                print "BOT >> RESTARTED" 
                                self.isHoldingNewspaper = False
                                
        def handleSafeMessage(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT SAFE MESSAGE: " + data[4]
                        self.sendSafeMessage(data[4])

        def handleJoke(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT JOKE: "  + data[4]
                        self.sendJoke(data[4])

        def handleSnowball(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT SNOWBALL: " + data[4] + " " + data[5] 
                        self.sendSnowball(data[4], data[5])

        def handleFrame(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT FRAME: " + data[4]
                        self.sendFrame(data[4])

        def handleAction(self, data):
                if data[3] == self.mixTarget:
                        print self.name + ">> SENT ACTION: " + data[4]
                        self.sendAction(data[4])

        def handleJoinRoom(self, data):
                self.getPlayerInfoByName(self.name)
        
        def handlePlayerByName(self, data):
                self.mixTarget = data[4]
                self.findBuddy(self.mixTarget)

        def handleBf(self, data):
                if data[3] == '-1':
                        print "[INFO] " +self.name + " is not on the server you choose."
                        self.transport.loseConnection()
                        exit()
                        
                print self.name + ">> JOINED ROOM: " + data[3]
                self.joinRoom(data[3])
                self.currentRoomID = data[3]
                
                self.isHoldingBlueprint = False
                self.isHoldingNewspaper = False

        def handleRp(self, data):
               if data[3] == self.mixTarget:
                        self.findBuddy(self.mixTarget)
                        
        def handleError(self, data):
                if data[3] == "210" or data[3] == "212":
                        print "BOT >> FAILED TO JOIN ROOM"
                        self.findBuddy(self.mixTarget)
    
                else:
                        print "BOT >> ERROR: " + data[3]

        '''Chat Commands'''
        
        def sendBlueprint(self):
                self.send("%xt%s%t#rt%21%1%%")
                self.send("%xt%s%t#at%48952%2%1%")
                
        def sendNewspaper(self):
                self.send("%xt%s%t#rt%26408%1%%")
                self.send("%xt%s%t#at%26408%1%1%")

class FollowBotFactory(PenguinFactory):

        def __init__(self, target_penguin, offset_x=0, offset_y=0):
                self.offset_x = offset_x
                self.offset_y = offset_y
                self.target_penguin = target_penguin
                super(FollowBotFactory, self).__init__()
                # self.logger.debug("FollowBotFactory constructed")

        def buildProtocol(self, addr):
                player = self.queue.pop()
                
                penguin = MyPenguin(player)
                
                penguin.target_penguin = self.target_penguin
                penguin.offset_x = self.offset_x
                penguin.offset_y = self.offset_y

                return penguin


cp = ClubPenguin()

accounts = []
for account in open("accounts.txt", "r").read().split("\n"):
        if account!= "":
                accounts.append(dict({"username":account.split(":")[0], "password":account.split(":")[1]}))
        else:
                break
        
        
'''_____________'''

'''  FORMATIONS  '''
'''_____________'''

def starFormation():
        
        '''
        Star Formation
        '''

        cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin, 45,0))

        cp.connect(username=accounts[1]["username"], password=accounts[1]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,0))

        cp.connect(username=accounts[2]["username"], password=accounts[2]["password"], server=server, \
                factory=FollowBotFactory(penguin, 45,45))

        cp.connect(username=accounts[3]["username"], password=accounts[3]["password"], server=server, \
                factory=FollowBotFactory(penguin, 45,-45))

        cp.connect(username=accounts[4]["username"], password=accounts[4]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,45))

        cp.connect(username=accounts[5]["username"], password=accounts[5]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,-45))

        cp.connect(username=accounts[6]["username"], password=accounts[6]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,-45))

        cp.connect(username=accounts[7]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,45))

        cp.connect(username=accounts[8]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin, 65,0))

        cp.connect(username=accounts[9]["username"], password=accounts[1]["password"], server=server, \
                factory=FollowBotFactory(penguin, -65,0))

        cp.connect(username=accounts[10]["username"], password=accounts[2]["password"], server=server, \
                factory=FollowBotFactory(penguin, 65,65))

        cp.connect(username=accounts[11]["username"], password=accounts[3]["password"], server=server, \
                factory=FollowBotFactory(penguin, 65,-65))

        cp.connect(username=accounts[12]["username"], password=accounts[4]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,65))

        cp.connect(username=accounts[13]["username"], password=accounts[5]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,-65))

        cp.connect(username=accounts[14]["username"], password=accounts[6]["password"], server=server, \
                factory=FollowBotFactory(penguin, -65,-65))

        cp.connect(username=accounts[15]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,45))

        cp.connect(username=accounts[16]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin, 90,0))

        cp.connect(username=accounts[17]["username"], password=accounts[1]["password"], server=server, \
                factory=FollowBotFactory(penguin, -90,0))

        cp.connect(username=accounts[18]["username"], password=accounts[2]["password"], server=server, \
                factory=FollowBotFactory(penguin, 90,90))

        cp.connect(username=accounts[19]["username"], password=accounts[3]["password"], server=server, \
                factory=FollowBotFactory(penguin, 90,-90))

        cp.connect(username=accounts[20]["username"], password=accounts[4]["password"], server=server, \
                factory=FollowBotFactory(penguin, 90,90))

        cp.connect(username=accounts[21]["username"], password=accounts[5]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,-90))
 
        cp.connect(username=accounts[22]["username"], password=accounts[6]["password"], server=server, \
                factory=FollowBotFactory(penguin, -90,-90))

        cp.connect(username=accounts[23]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -90,90))
 
        cp.start()

def swastikaFormation():

        '''
        Swastika Formation
        '''
        
        cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,30))

        cp.connect(username=accounts[1]["username"], password=accounts[1]["password"], server=server, \
                factory=FollowBotFactory(penguin, -0,-30))

        cp.connect(username=accounts[2]["username"], password=accounts[2]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,60))

        cp.connect(username=accounts[3]["username"], password=accounts[3]["password"], server=server, \
                factory=FollowBotFactory(penguin, -0,-60))

        cp.connect(username=accounts[4]["username"], password=accounts[4]["password"], server=server, \
                factory=FollowBotFactory(penguin, 25,-60))

        cp.connect(username=accounts[5]["username"], password=accounts[5]["password"], server=server, \
                factory=FollowBotFactory(penguin, -25,60))

        cp.connect(username=accounts[6]["username"], password=accounts[6]["password"], server=server, \
                factory=FollowBotFactory(penguin, 50,-60))

        cp.connect(username=accounts[7]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -50,60))

        cp.connect(username=accounts[8]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, 30,0))

        cp.connect(username=accounts[9]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -30,-0))

        cp.connect(username=accounts[10]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, 60,0))

        cp.connect(username=accounts[11]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -60,-0))

        cp.connect(username=accounts[12]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, 60,25))

        cp.connect(username=accounts[13]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -60,-25))

        cp.connect(username=accounts[14]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, 60,50))

        cp.connect(username=accounts[15]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -60,-50))

        cp.start()

def cubeFormation():
        
        '''
        Cube Formation
        '''

        cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin, 45,0))

        cp.connect(username=accounts[1]["username"], password=accounts[1]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,0))

        cp.connect(username=accounts[2]["username"], password=accounts[2]["password"], server=server, \
                factory=FollowBotFactory(penguin, 45,45))

        cp.connect(username=accounts[3]["username"], password=accounts[3]["password"], server=server, \
                factory=FollowBotFactory(penguin, 45,-45))

        cp.connect(username=accounts[4]["username"], password=accounts[4]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,45))

        cp.connect(username=accounts[5]["username"], password=accounts[5]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,-45))

        cp.connect(username=accounts[6]["username"], password=accounts[6]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,-45))

        cp.connect(username=accounts[7]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, -45,45))

        cp.start()

def circleFormation():

        '''
        Circle Formation
        '''

        cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin, -0,-60))

        cp.connect(username=accounts[1]["username"], password=accounts[1]["password"], server=server, \
                factory=FollowBotFactory(penguin, 0,60))

        cp.connect(username=accounts[2]["username"], password=accounts[2]["password"], server=server, \
                factory=FollowBotFactory(penguin, 60,0))

        cp.connect(username=accounts[3]["username"], password=accounts[3]["password"], server=server, \
                factory=FollowBotFactory(penguin, -60,-0))

        cp.connect(username=accounts[4]["username"], password=accounts[4]["password"], server=server, \
                factory=FollowBotFactory(penguin, -40,40))

        cp.connect(username=accounts[5]["username"], password=accounts[5]["password"], server=server, \
                factory=FollowBotFactory(penguin, 40,40))

        cp.connect(username=accounts[6]["username"], password=accounts[6]["password"], server=server, \
                factory=FollowBotFactory(penguin, -40,-40))

        cp.connect(username=accounts[7]["username"], password=accounts[7]["password"], server=server, \
                factory=FollowBotFactory(penguin, 40,-40))

        cp.start()
        

def gayFormation():
        '''
        GAY Formation
        '''
        
        cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -60,-80))
 
        cp.connect(username=accounts[1]["username"], password=accounts[1]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -80,-80))
         
        cp.connect(username=accounts[2]["username"], password=accounts[2]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -100,-80))
         
        cp.connect(username=accounts[3]["username"], password=accounts[3]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -100,-60))
         
        cp.connect(username=accounts[4]["username"], password=accounts[4]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -100,-40))
         
        cp.connect(username=accounts[5]["username"], password=accounts[5]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -100,-20))
         
        cp.connect(username=accounts[6]["username"], password=accounts[6]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -100,0))
         
        cp.connect(username=accounts[7]["username"], password=accounts[7]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -80,0))
                   
        cp.connect(username=accounts[8]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -60,0))
                                   
        cp.connect(username=accounts[9]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -40,0))
                                   
        cp.connect(username=accounts[10]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -40,-20))
                                   
        cp.connect(username=accounts[11]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -40,-40))
                                   
        cp.connect(username=accounts[12]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, -70,-40))
                                   
        cp.connect(username=accounts[13]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 0,-20))
         
        cp.connect(username=accounts[14]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 0,-40))
                                   
        cp.connect(username=accounts[15]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 0,-60))
                                   
        cp.connect(username=accounts[16]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 0,-80))
                                   
        cp.connect(username=accounts[17]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 40,-80))
                                   
        cp.connect(username=accounts[18]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 60,-80))
                                   
        cp.connect(username=accounts[19]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 60,-60))
                                   
        cp.connect(username=accounts[20]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 60,-40))
                                   
        cp.connect(username=accounts[21]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 60,-20))
                                   
        cp.connect(username=accounts[22]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 60,0))
         
        cp.connect(username=accounts[23]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 30,-50))
                                   
        cp.connect(username=accounts[24]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 100,-80))
                   
        cp.connect(username=accounts[25]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 110,-60))
                                   
        cp.connect(username=accounts[26]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 120,-40))
                                   
        cp.connect(username=accounts[27]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 140,-60))
                                   
        cp.connect(username=accounts[28]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 160,-80))
                                   
        cp.connect(username=accounts[29]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 120,-20))
                                   
        cp.connect(username=accounts[30]["username"], password=accounts[8]["password"], server=server, \
                        factory=FollowBotFactory(penguin, 120,0))

        cp.start()


def raidFormation():
        '''
        Raid Formation
        '''
        
        for account in accounts:
                cp.connect(username=account["username"], password=account["password"], server= server, \
                        factory=FollowBotFactory(penguin))
        cp.start()

def noOffset():
        '''
        No Offset
        '''
        
        cp.connect(username=accounts[0]["username"], password=accounts[0]["password"], server=server, \
                factory=FollowBotFactory(penguin))

        cp.start()


'''_____________'''

'''END FOMRATIONS'''
'''_____________'''


### TO ADD FORMATIONS MAKE ANOTHER FUNCTION AND ADD ANOTHER ELIF CONDITION ###

        
if formation.lower() == "star":
        if len(accounts) < 24:
                print "You do not have enough penguins in the accounts.txt file to use this formation, you will need 24 penguins; you have " + str(len(accounts))
        else:
                starFormation()
        
elif formation.lower() == "swastika":
        if len(accounts) < 16:
                print "You do not have enough penguins in the accounts.txt file to use this formation, you will need 16 penguins; you have " + str(len(accounts))
        else:
                swastikaFormation()
        
elif formation.lower() == "cube":
        if len(accounts) < 8:
                print "You do not have enough penguins in the accounts.txt file to use this formation, you will need 8 penguins; you have " + str(len(accounts))
        else:
                cubeFormation()

elif formation.lower() == "circle":
        if len(accounts) < 8:
                print "You do not have enough penguins in the accounts.txt file to use this formation, you will need 8 penguins; you have " + str(len(accounts))
        else:
                circleFormation()

elif formation.lower() == "gay":
        if len(accounts) < 31:
                print "You do not have enough penguins in the accounts.txt file to use this formation, you will need 31 penguins; you have " + str(len(accounts))
        else:
                gayFormation()

elif formation.lower() == "raid":
        raidFormation()

elif formation.lower() == "no offset":
        if len(accounts) < 2:
                print "You do not have enough penguins in the accounts.txt file to use this formation, you will need 1 penguins; you have " + str(len(accounts))
        else:
                noOffset()

else:
        print "Formation not found. Try again!"
        
