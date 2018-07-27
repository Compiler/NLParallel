
class Topic:

	def __init__(self, name):
		self.name = name;

	def getName(self):
		return self.name

	def setName(self, newName):
		self.name = newName

	def __str__(self):
		return self.name;

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return hash(self.name)
