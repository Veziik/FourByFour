#! /usr/bin/env python3
import sys
from classes import *
import random
import time

def apply_preset(arguments):
	preset = arguments['preset']
	numberOfCycles = arguments['numberOfCycles']
	parguments = dict()
	parguments['include'] = set()
	parguments['restrict'] = set()
	parguments['exclude'] = set()
	parguments['cycleThemes'] = list()

	if preset == 'balanced':
		parguments['include'].add('warmup')
		parguments['include'].add('legs')
		parguments['include'].add('arms')
		parguments['include'].add('power')
		parguments['include'].add('speed') 
		parguments['include'].add('abdominals')
		parguments['include'].add('pushup')
		parguments['exclude'].add('hard')


		
		legsOrArms = ['legs', 'arms']
		speedOrPower = ['speed', 'power']
		random.seed(time.time)
		legsOrArmsFirst = random.randint(0,1)
		random.seed(time.time)
		speedOrPowerFirst = random.randint(0,1)


		for i in range(numberOfCycles):
			if i <= numberOfCycles/4:
				parguments['cycleThemes'].append(['warmup'])
			elif i <= 3*(numberOfCycles/8):
				parguments['cycleThemes'].append([speedOrPower[speedOrPowerFirst] , legsOrArms[legsOrArmsFirst] ])
			elif i <= 4*(numberOfCycles/8):
				parguments['cycleThemes'].append([speedOrPower[1-speedOrPowerFirst] , legsOrArms[legsOrArmsFirst] ])
			elif i <= 5*(numberOfCycles/8):
				parguments['cycleThemes'].append([speedOrPower[speedOrPowerFirst] , legsOrArms[1-legsOrArmsFirst] ])
			elif i <= 6*(numberOfCycles/8):
				parguments['cycleThemes'].append([speedOrPower[1-speedOrPowerFirst] , legsOrArms[1-legsOrArmsFirst] ])
			else:
		 		parguments['cycleThemes'].append(['abdominals' , 'pushup'])




	elif preset == 'legspeed':
		parguments['include'].add('speed')
		parguments['include'].add('warmup')
		parguments['restrict'].add('legs')

		for i in range(numberOfCycles):
			if i <= numberOfCycles/4:
				parguments['cycleThemes'].append(['warmup'])

	elif  preset == 'legstrength':
		parguments['include'].add('legs')
		parguments['include'].add('strength')
		parguments['include'].add('warmup')
		parguments['restrict'].add('legs')

		for i in range(numberOfCycles):
			if i <= numberOfCycles/4:
				parguments['cycleThemes'].append(['warmup'])

	elif preset == 'armspeed':
		parguments['include'].add('arms')
		parguments['include'].add('speed')
		parguments['include'].add('warmup')
		parguments['restrict'].add('arms')

		for i in range(numberOfCycles):
			if i <= numberOfCycles/4:
				parguments['cycleThemes'].append(['warmup'])

	elif preset == 'armstrength':
		parguments['include'].add('arms')
		parguments['include'].add('strength')
		parguments['include'].add('warmup')
		parguments['restrict'].add('arms')

		for i in range(numberOfCycles):
			if i <= numberOfCycles/4:
				parguments['cycleThemes'].append(['warmup'])

	elif preset == 'abdominals':
		parguments['include'].add('abdominals')
		parguments['include'].add('back')


	return parguments

def import_exercises(filename, arguments):
	exercises = set()
	include = arguments['include']
	exclude = arguments['exclude']
	restrict = arguments['restrict']
	parguments = apply_preset(arguments)

	for keyword in parguments['include']:
		arguments['include'].add(keyword)

	for keyword in parguments['exclude']:
		arguments['exclude'].add(keyword)

	for keyword in parguments['restrict']:
		arguments['restrict'].add(keyword)

	if parguments['cycleThemes']:
		arguments['cycleThemes'] = parguments['cycleThemes']



	with open(filename, 'r') as file:
		for line in file:
			if len(line) > 2 and not line.startswith('#'):
				replaced = line.replace('\n', '')
				split = replaced.split(',')
				name = split[0].title()
				slots = int(split[1].replace(' ', ''))
				tags = set()
				for i in range(2, len(split)):
					tags.add(split[i].replace(' ', '').lower())

				if (tags & include or 'all' in include) and len(tags & restrict) == len(restrict) and len(tags & exclude)== 0 :
					newexercise = Exercise(name=name,slots=slots, tags=tags)
					#newexercise.toString()
					exercises.add(newexercise)
	return exercises

def parse_preset(preset):
	preset = preset.lower().replace(' ', '').replace('\n', '')
	if preset == 'kb' or preset == 'kickboxing' or preset == 'balanced' or preset == 'default':
		return 'balanced'
	elif preset == 'lsp' or preset == 'legspeed':
		return 'legspeed'
	elif preset == 'lstr' or preset == 'legstrength':
		return 'legstrength'
	elif preset == 'asp' or preset == 'armspeed':
		return 'armspeed'
	elif preset == 'astr' or preset == 'armstrength':
		return 'armstrength'
	elif preset == 'abdominals' or preset == 'abs':
		return 'abdominals'
	else:
		return None	




def print_help():
	print('''\nFourByFour: An exercise routine Generator

USAGE: ./generate.py [routine name] <option1> <option2> ...

Routine Commands: 
4x4: 4 cycles of 4 exercises, each exercise lasts 45sec, 1min rest between cycles
8x4: twice as many cycles as 4x4
list: List exercises, but do not order them into an exercise

Options:
-i/-I <tags>: Include any exercises with one of these tags
-e/-E <tags>: Exclude any exercises with one of these tags
-r/-R <tags>: Restrict all exercises to have all these tags
''')

def parse_commands():
	arguments = dict()
	if len(sys.argv) < 2:
		print('Not enough arguments.')
		exit(0)

	#Parse Routine To Construct
	routine = sys.argv[1].lower() 
	if  routine == '8x4' or routine == '30m hiit':
		arguments['routineName'] = '4x4' 
		arguments['numberOfCycles'] = 4
		arguments['cycleSize'] = 4
		arguments['onTime'] = 45
		arguments['restTime'] = 60
	elif routine == '4x4' or routine == '15m hiit':
		arguments['routineName'] = '8x4'
		arguments['numberOfCycles'] = 8
		arguments['cycleSize'] = 4
		arguments['onTime'] = 45
		arguments['restTime'] = 60
	elif routine == 'help' or routine == '--help':
		print_help()
		exit(0)
	elif routine == 'list':
		arguments['routineName'] = None
		arguments['numberOfCycles'] = 0
	else:
		print('Routine not recognized')
		exit(0)

	#Parse Options
	exclude = set()
	include = set()
	restrict = set()
	preset = None
	

	if(len(sys.argv) > 2):
		i = 2
		while i < len(sys.argv):
			#Parse -i option
			if sys.argv[i] == '-i':
				i+=1

				while i < len(sys.argv) and '-' not in sys.argv[i]:
					include.add(sys.argv[i])
					i+=1
			#parse -e option
			elif sys.argv[i] == '-e':
				i+=1

				while i < len(sys.argv) and '-' not in sys.argv[i]:
					exclude.add(sys.argv[i])
					i+=1
			#parse -r option
			elif sys.argv[i] == '-r':
				i+=1

				while i < len(sys.argv) and '-' not in sys.argv[i]:
					restrict.add(sys.argv[i])
					i+=1
			elif sys.argv[i] == '-p':
				preset = parse_preset(sys.argv[i+1])
				i+=2


			else:
				i+=1

			
			#print(i)

		#Dbug comment for argumemts
		#print('include: ' + str(include))
		#print('exclude: ' + str(exclude))
		#print('restrict: ' + str(restrict))
		#print('preset: ' + str(preset))

	if not include:
		include.add('all')

	arguments['preset'] = preset
	arguments['include'] = include
	arguments['exclude'] = exclude
	arguments['restrict'] = restrict

			

	return arguments



def list_exercises(exercises):
	exerciseList = list()
	for exercise in exercises:
		exerciseList.append(exercise.name)

	exerciseList.sort()
	for name in exerciseList:
		print(name) 


def main():
	arguments = parse_commands()
	exercises = import_exercises('exercises.txt', arguments)
	if not arguments['routineName']:
		list_exercises(exercises)
		arguments['routine'] = None
	elif arguments['routineName'] == '4x4':
		arguments['routine'] = Routine(onTime=arguments['onTime'], restTime=arguments['restTime'], cycleSize=arguments['cycleSize'], numberOfCycles=arguments['numberOfCycles'], cycleThemes=arguments['cycleThemes'])
		
	elif arguments['routineName'] == '8x4':
		#arguments['routine'] = Routine(onTime=arguments.['onTime'], restTime=arguments.['restTime'], cycleSize=arguments['cycleSize'], numberOfCycles=arguments['numberOfCycles'], cycleThemes=arguments['cycleThemes'])
		pass


	if arguments['routine']:
		arguments['routine'].generateRoutineList(exercises)




if __name__ == '__main__':
	main()
else:
	print('no main')
	exit(0)



