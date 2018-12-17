#! /usr/bin/env python3
import sys
from classes import Exercise
import random #random.randint(startint,endint)


def apply_preset(arguments):
	preset = arguments['preset']
	parguments = dict()
	parguments['include'] = set()
	parguments['restrict'] = set()
	parguments['exclude'] = set()

	if preset == 'balanced':
		 parguments['include'].add('warmup')
		 parguments['include'].add('legs')
		 parguments['include'].add('arms')
		 parguments['include'].add('power')
		 parguments['include'].add('speed')
		 parguments['include'].add('abdominals')
		 parguments['include'].add('pushup')
		 parguments['exclude'].add('hard')
	elif preset == 'legspeed':
		 parguments['include'].add('speed')
		 parguments['include'].add('warmup')
		 parguments['restrict'].add('legs')
	elif  preset == 'legstrength':
		 parguments['include'].add('legs')
		 parguments['include'].add('strength')
		 parguments['include'].add('warmup')
		 parguments['restrict'].add('legs')
	elif preset == 'armspeed':
		 parguments['include'].add('arms')
		 parguments['include'].add('speed')
		 parguments['include'].add('warmup')
		 parguments['restrict'].add('arms')
	elif preset == 'armstrength':
		 parguments['include'].add('arms')
		 parguments['include'].add('strength')
		 parguments['include'].add('warmup')
		 parguments['restrict'].add('arms')
	elif preset == 'abdominals':
		 parguments['include'].add('arms')
		 parguments['include'].add('strength')
		 parguments['include'].add('warmup')
		 parguments['restrict'].add('arms')

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

				if tags & include and len(tags & restrict) == len(restrict) and len(tags & exclude)== 0:
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

Options:
-i/-I <tags>: include any exercises with one of these tags
-e/-E <tags>: exclude any exercises with one of these tags
-r/-R <tags>: restrict all exercises to have all these tags
''')

def parse_commands():
	arguments = dict()
	if len(sys.argv) < 2:
		print('Not enough arguments.')
		exit(0)

	#Parse Routine To Construct
	routine = sys.argv[1].lower() 
	if  routine == '8x4' or routine == '30m hiit':
		arguments['routine'] = '4x4' 
	elif routine == '4x4' or routine == '15m hiit':
		arguments['routine'] = '8x4'
	elif routine == 'help' or routine == '--help':
		print_help()
		exit(0)
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
		arguments['preset'] = preset
		arguments['include'] = include
		arguments['exclude'] = exclude
		arguments['restrict'] = restrict
			

	return arguments







def main():
	arguments = parse_commands()
	exercises = import_exercises('exercises.txt', arguments)




if __name__ == '__main__':
	main()
else:
	print('no main')
	exit(0)