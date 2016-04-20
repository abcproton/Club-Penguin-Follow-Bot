from string import join
from random import choice, randrange
from urllib import urlencode
from urllib2 import urlopen, Request, HTTPError
from bs4 import BeautifulSoup
from threading import Thread
import requests


class AccountGenerator(Thread):
  header = {
    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
  }

  def __init__(self):
    super(AccountGenerator, self).__init__()
      
    self.email = "random"
    self.name = "random"
    self.pw = "penguin88"
    self.color = randrange(1, 12)

  def run(self):
    self.loadCaptchas()
    self.registerPenguin()

  def loadCaptchas(self):
    self.captchas = {}
    self.captchas["watermelon"] = "ARRB8J8KQ9t7AAAAAElFTkSuQmCC"
    self.captchas["balloon"] = "wuWB85cW2c5NQAAAABJRU5ErkJggg=="
    self.captchas["pizza"] = "XMAAAAASUVORK5CYII="
    self.captchas["popcorn"] = "yat7sdCF61QAAAABJRU5ErkJggg=="
    self.captchas["igloo"] = "b+T94dZQb+IAAAAASUVORK5CYII="
    self.captchas["cheese"] = "B0eBprJbn4wXAAAAAElFTkSuQmCC"

  def registerPenguin(self):
    self.getRegisterData()

    if self.name == "random":
      self.name = self.genRandomString(8)

    if self.email == "random":
      self.email = self.genRandomString(8) + "@gmail.com"

    print "[{0}] Registering... ".format(self.name)

    try:
      data = {
        "anon_token": self.anonToken,
        "color": str(self.color),
        "name": self.name,
        "pass": self.pw,
        "pass_show": "1",
        "email": self.email,
        "terms": "1",
        "captcha": str(self.captchaN),
        "op":"Create Your Penguin",
        "form_build_id": self.formBuildId,
        "form_id": "penguin_create_form"
      }

      request = Request("https://secured.clubpenguin.com/penguin/create", urlencode(data), self.header)
      response = urlopen(request)

      htmlData = response.read()
      soup = BeautifulSoup(htmlData, "html.parser")
      
      setCookieResponse = response.info().getheader("Set-Cookie")
      response.close()

      if setCookieResponse != None:
        print "[{0}] Registration successful".format(self.name)
        with open("accounts.txt", "a") as file:
          file.write("{0}:{1}\n".format(self.name, self.pw))

    except HTTPError, err:
      if err.code == 403:
        print "[{0}] Registration successful".format(self.name)
        with open("accounts.txt", "a") as file:
          file.write("{0}:{1}\n".format(self.name, self.pw))
      else:
        raise

   
  def getRegisterData(self):
    request = Request("https://secured.clubpenguin.com/penguin/create", headers=self.header)
    response = urlopen(request)

    cookie = response.info().getheader("Set-Cookie")
    htmlData = response.read()

    response.close()

    soup = BeautifulSoup(htmlData, "html.parser")

    itemName = self.findBetween(htmlData, "item_name\":\"", "\",");
    image1 = self.findBetween(htmlData, "\"images\":{\"1\":\"", "\",");
    image1 = image1.rsplit('/',1)[-1]

    image2 = self.findBetween(htmlData, image1 + "\",\"2\":\"", "\",");
    image2 = image2.rsplit('/',1)[-1]

    image3 = self.findBetween(htmlData, image2 + "\",\"3\":\"", "\"");
    image3 = image3.rsplit('/',1)[-1]

    itemImage = self.captchas[itemName]
    if(image1 == itemImage):
      self.captchaN = 0
    elif(image2 == itemImage):
      self.captchaN = 1
    elif(image3 == itemImage):
      self.captchaN = 2

    self.anonToken = soup.find("input", {"name": "anon_token"})["value"]
    self.formBuildId = soup.find("input", {"name": "form_build_id"})["value"]

    randomString = self.genRandomString()
    
    self.header["Cookie"] = "{0} playspanTRANSID=arthur-{1}; cpBROWSERID=vortexal-{1};".format(cookie, randomString)
    self.header["Origin"] = "https://secured.clubpenguin.com"
    self.header["Referer"] = "https://secured.clubpenguin.com/penguin/create"

  def findBetween(self, s, first, last):
    try:
      start = s.index(first) + len(first)
      end = s.index(last, start)
      return s[start:end]
    except ValueError:
      return ""

  def safeFind(self, str, value):
    try:
      jsonObj = json.loads(str)
      return jsonObj[value]
    except ValueError, e:
      return False
    return False

  def genRandomString(self, length=8):
    return join((choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(length)), "")

print """
    =+= Account Generator =+=
    Stores generated accounts in 'accounts.txt' file

\n
"""

amt = input("Enter the amount of penguins you wish to generate: ")

for i in range(int(amt)):
    a = AccountGenerator()
    a.start()
