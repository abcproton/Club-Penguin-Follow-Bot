from string import join
from random import choice, randrange
from urllib import urlencode
from operator import xor
from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
import threading

class AccountMaker(object, threading.Thread):

  header = {
    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
  }

  def __init__(self, username, password, email, color="random", amount=1):
    if len(username) > 12:
      print "Username is too long!"
    elif len(username) < 3:
      print "Username is too short."
    elif amount != 1 and len(username) > 9:
      print "Username is too long!"
    elif xor(type(amount) != int, amount < 1):
      print "Invalid amount specified."
    else:
      self.username = username
      self.password = password
      self.email = email
      self.color = color if color != "random" else randrange(1, 13)
      self.amount = amount

      self.create()

  def generateRandomString(self, length=8):
    return join((choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(length)), "")

  def retrieveCookies(self):
    initialRequest = Request("https://secured.clubpenguin.com/penguin/create", headers=self.header)

    initialResponse = urlopen(initialRequest)

    cookie = initialResponse.info().getheader("Set-Cookie")

    initialMarkup = initialResponse.read()
    initialResponse.close()

    soup = BeautifulSoup(initialMarkup)

    self.anonToken = soup.find("input", {"name": "anon_token"})["value"]
    self.formBuildId = soup.find("input", {"name": "form_build_id"})["value"]

    randomString = self.generateRandomString()
    self.header["Cookie"] = "{0} playspanTRANSID=arthur-{1}; cpBROWSERID=vortexal-{1};".format(cookie, randomString)
    self.header["Content-Type"] = "application/x-www-form-urlencoded"
    self.header["Origin"] = "https://secured.clubpenguin.com"
    self.header["Referer"] = "https://secured.clubpenguin.com/penguin/create"

  def register(self, username, email):
    self.retrieveCookies()

    if username == "random":
      username = self.generateRandomString(randrange(5, 11))

    if email == "random":
      randomLocal = self.generateRandomString()
      email = "{0}@gmail.com".format(randomLocal)

    print "Registering with {0} and {1}".format(username, email)

    data = {
      "anon_token": self.anonToken,
      "color": self.color,
      "name": username,
      "pass": self.password,
      "pass_show": randrange(0, 1),
      "email": email,
      "email_confirm": email,
      "terms": 1,
      "op":"Next",
      "form_build_id": self.formBuildId,
      "form_id": "penguin_create_form"
    }

    finalRequest = Request("https://secured.clubpenguin.com/penguin/create", urlencode(data), self.header)
    finalResponse = urlopen(finalRequest)

    setCookieResponse = finalResponse.info().getheader("Set-Cookie")
    finalResponse.close()

    if setCookieResponse != None:
      print "Registration Success"
      with open("accounts.txt", "a") as file:
          file.write(username + ":" + self.password + "\n")
    else:
      print "Registration failed"

    del self.header["Cookie"], self.header["Content-Type"], \
        self.header["Origin"], self.header["Referer"]

  def run(self):
    if self.amount > 1:
      for account in range(self.amount):
        if self.username == "random":
          self.register(self.username, self.email)
        else:
          self.register(self.username + str(account), self.email)
    else:
      self.register(self.username, self.email)

try:
  while True:
    t = AccountMaker(username="random", password="ComplexPassword1", email="random", amount=100)
    t.start()
except KeyboardInterrupt:
  print "Stopping.." 
