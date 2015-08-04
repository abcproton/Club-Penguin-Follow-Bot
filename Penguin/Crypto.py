import hashlib

class Crypto:

	@staticmethod
	def encryptPassword(password):
		hash = hashlib.md5(password.encode('utf-8')).hexdigest()
		swappedHash = hash[16:32] + hash[0:16]
		
		return swappedHash

	@staticmethod
	def getLoginHash(password, rndK):
		key = Crypto.encryptPassword(password).upper()
		key += rndK
		key += "a1ebe00441f5aecb185d0ec178ca2305Y(02.>'H}t\":E1_root"

		hash = Crypto.encryptPassword(key)

		return hash