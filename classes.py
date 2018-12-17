class Exercise(object):
	"""docstring for Exercise"""
	def __init__(self, name='', slots=0, tags=set()):
		self.name = name
		self.slots = slots
		self.tags = tags

	def toString(self):
		print('Name: ' + self.name)
		print('Slots: ' + str(self.slots))
		print('Tags: ' + str(self.tags))

		