import random #random.randint(startint,endint)

class Exercise(object):
	"""Object for storing exercises"""
	def __init__(self, name='', slots=0, tags=set()):
		self.name = name
		self.slots = slots
		self.tags = tags

	def toString(self):
		print('Name: ' + self.name)
		print('Slots: ' + str(self.slots))
		print('Tags: ' + str(self.tags))

class Routine(object):
	"""Object for storing and generating routines """


	def __init__(self, onTime=0, offTime=0, restTime=0, cycleSize=0, cycleThemes=list(), numberOfCycles=0):
		self.onTime = onTime
		self.offTime = offTime
		self.restTime = restTime
		self.cycleSize = cycleSize
		self.cycleThemes = cycleThemes
		self.numberOfCycles = numberOfCycles
		self.routineList = list()


	def filterSet(self, exercises, theme):
		returnSet = set()

		if theme:
			for exercise in exercises:
				if theme in exercise.tags:
					returnSet.add(exercise)
		else:
			returnSet = exercises

		return returnSet


	def generateRoutineList(self, exercises):
		for i in range(self.numberOfCycles):
			theme = None
			if i < len(self.cycleThemes) and self.cycleThemes[i]:
				theme  = self.cycleThemes[i]
			
			for j in range(cycleSize):
				filteredSet = self.filterSet(exercises, theme)
				exercise = random.choice(tuple(filterSet))
				self.routineList.append(str(self.onTime) + 's ' + exercise.name)

				if self.offTime :
					self.routineList.append(str(self.offTime) + 's off time')

			if self.restTime > 0 and not (j + 1 == self.numberOfCycles):
				self.routineList.append(str(self.restTime) + 's Rest')

			print(str(routineList))
