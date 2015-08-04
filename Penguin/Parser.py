from collections import deque

class Parser:

	@staticmethod
	def isValid(data):
		parsed = Parser.parseRaw(data)

		if data.startswith("%xt%") and len(parsed) >= 3:
			return True
		else:
			return False

	@staticmethod
	def parseRaw(data):
		parsed = deque(data.split("%"))
		parsed.popleft()
		parsed.pop()

		return parsed

	@staticmethod
	def parseVertical(data):
		parsed = data.split("|")

		return parsed