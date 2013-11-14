#!/usr/bin/env python

import argparse
import os
import sys
from subprocess import Popen, PIPE, STDOUT, call


"""
Color codes:
"""
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
GREY = '\033[90m'
BLACK = '\033[90m'
DEFAULT = '\033[99m'

BOLD = '\033[1m'

WARNING = RED
MODULE = BLUE+BOLD
FUNCTION = GREY+BOLD
ENDC = '\033[0m'

def check_input(inputString):
	"""
	Arguments: String of arguments from Terminal
	Purpose:
		Split string into a list for easier iteration
	Return: List of arguments as string
	"""
	if inputString == '':
		inputList = []
		
	elif inputString.find(',') != -1:
		inputList = inputString.split(',')
	else:
		inputList = inputString.split(' ')

	return inputList

def create_functions(fileName, function, delimiter='', classMethod=False):
	"""
	Arguments: file to write to, function to write, add extra delimeter if class method, boolean for class method or not
	Purpose:
		writes the functions/method to the file
		will add arguments and return values to functions/methods
	Return: N/A
	"""

	argumentString = raw_input("Enter argument(s) for "+FUNCTION+function+ENDC+': ')

	argumentList = check_input(argumentString)

	argumentString = ','.join(argumentList)
	
	if classMethod == True:
		if argumentList == []:
			argumentString = 'self'
		else:
			argumentString = 'self,'+argumentString

	fileName.write('def '+function+'('+argumentString+')'+':')

	returnString = raw_input("Enter return value(s) for "+FUNCTION+function+ENDC+': ')
	
	returnValueList = check_input(returnString)

	if returnValueList == []:
		fileName.write('\n\t'+delimiter+'pass # remove this and replace with the function body')
	else:
		
		if not classMethod:
			returnString = ','.join(returnValueList)
			fileName.write('\n\t'+delimiter+'return '+returnString)
		else:
			classReturnValueList = []
			
			for value in returnValueList:
				value = 'self.'+value.replace(' ','')
				classReturnValueList.append(value)
			
			returnString = ','.join(classReturnValueList)
			fileName.write('\n\t'+delimiter+'return '+returnString)

	fileName.write('\n\n')

def check_package(package):
	"""
	Argument: Package to import
	Purpose:
		check if package can be Imported
	Return: True or False depending on if module could be imported or not
	"""
	try:
		__import__(package)
		return True
	except ImportError:
		return False

def install_package(package):
	"""
	Argument: Package to install
	Purpose:
		Installs packages/modules if User doesn't have it installed already
	Return: True or False depending on if package installed or not
	"""

	if os.getuid() == 0:
		command = 'sudo pip install '+package
	else:
		command = 'pip install '+package
	
	command = command.split(' ')
	event = Popen(command, shell=True, stdin=PIPE, stdout=PIPE)
	output = event.communicate()

	messageString = output[0]
	beginMessage = messageString.find('Could')
	# print beginMessage
	endMessage = messageString[beginMessage:].find(package)+len(package)+beginMessage
	# print endMessage
	

	# print output

	if output[0].find("Could not find") != -1:
		print WARNING+'Download/Install Error: '+ENDC+messageString[beginMessage:endMessage]
		return False
	else:
		return True

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', default='pygenFile',help='name of the file you want to create')
	parser.add_argument('-i', '--imports', nargs='+', help='modules you want to import')
	parser.add_argument('-c', '--classes', nargs='+', help='names of classes you want to create')
	parser.add_argument('-f', '--functions', nargs='+', help='names of functions you want to create')
	
	parser.add_argument('-fw', '--framework', nargs='?', help='name of python framework')

	args = parser.parse_args()

	fileName = ""

	# begin implementing Framework app files generation
	if args.framework:

		if os.getuid() != 0: # check for root user
			print WARNING+BOLD+'Warning: Not root user!'+ENDC+' Some dependencies may not install.'
			response = raw_input(CYAN+'Continue?'+ENDC+'[y/n]: ')
					
			if response.lower() == 'n':
				sys.exit()

		if not check_package('pip'):
			from subprocess import Popen, PIPE, STDOUT
			command = 'easy_install pip'
			event = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
			output = event.communicate()
			print output[0]

		print "About to install modules"
		install_package(args.framework)

		# if check_package(args.framework):
		# 	execfile(args.framework+'Generate.py')
		# else:
		# 	install_package(args.framework)
		# 	execfile(args.framework+'Generate.py')

	else:
		if args.file:
			
			# if os.path.exists('./'+args.file+'.py'):

			# 	# Allow User to overwrite file that already exists
			# 	# -----------------------------------------------------
			# 	print WARNING+BOLD+'Warning!'+ENDC+' About to overwrite '+BLUE+args.file+ENDC
			# 	response = raw_input(CYAN+'Would you like to continue?'+ENDC+'[y/n] ')
			# 	if response.lower() == 'n':
			# 		sys.exit()
			# 	else:
			# 		# os.remove(args.file+'.py')
			# 		fileName = open(args.file+'.py', 'w')
			# 	# -----------------------------------------------------
			# else:
			# 	print 'Creating new file, '+BLUE+BOLD+fileName
			# 	fileName = open(args.file+'.py', 'w')

			fileName = open(args.file+'.py', 'w')

			if args.imports:
				
				# check for modules and install dependencies if necessary

				if os.getuid() != 0: # check for root user
					print WARNING+BOLD+'Warning: Not root user!'+ENDC+' Some dependencies may not install.'
					response = raw_input(CYAN+'Continue?'+ENDC+'[y/n]: ')
					
					if response.lower() == 'n':
						sys.exit()


				for module in args.imports:

					moduleExists = check_package(module)
					

					if moduleExists:
						print 'Imported '+MODULE+module+ENDC
						fileName.write('import '+module+'\n')

					else:
						pipExists = check_package('pip')
						
						if pipExists:
							couldInstall = install_package(module)
							
							if couldInstall:
								fileName.write('import '+module+'\n')
							else:
								print WARNING+'ERROR:'+ENDC+' Module, '+MODULE+module+ENDC+', does not exist or could not be downloaded/installed. Did not write to file'
						
						else:
							# install pip first
							from subprocess import Popen, PIPE, STDOUT
							command = 'easy_install pip'
							event = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
							output = event.communicate()
							print output[0]

							install_package(module)

							fileName.write('import '+module+'\n')


				fileName.write('\n')

			if args.classes:

				for className in args.classes:
					fileName.write('class '+className+':')

					dataString = raw_input('Enter data to be stored in the class, '+BLUE+BOLD+className+ENDC+': ')

					dataList = check_input(dataString)

					argumentDataList = ['self']

					for arg in dataList:
						newArg = arg+'=None'
						argumentDataList.append(newArg)
						

					dataString = ','.join(argumentDataList)
					fileName.write('\n\tdef __init__('+dataString+'):')

					for arg in argumentDataList[1:]:
						
						fileName.write('\n\t\tself.'+arg.replace(' ', '').replace('=None', '')+' = '+arg.replace('=None', '').replace(' ', ''))

					fileName.write('\n\n')

					methodString = raw_input('Enter the methods of class, '+BLUE+BOLD+className+ENDC+': ')

					methodList = check_input(methodString)

					for method in methodList:
						fileName.write('\t')
						create_functions(fileName, method, '\t', True)


			if args.functions:

				for function in args.functions:

					create_functions(fileName, function)

				fileName.write("def main():\n\tpass")
				fileName.write("\n\nif __name__ == '__main__':\n\tmain()")
			
			else:
				fileName.write("def main():\n\tpass")
				fileName.write("\n\nif __name__ == '__main__':\n\tmain()")
		
		fileName.close()
		print 'Successfully created the file, '+CYAN+args.file+'.py'+ENDC

	# open file generated in default editor
	try:
		returnCode = subprocess.call('open '+args.file+'.py', shell=True)
		if returnCode < 0:
			print >>sys.stderr, "Child was terminated by signal", -returnCode
		else:
			print >>sys,stderr, "Child returned", returnCode
	except OSError, e:
		print >>sys.stderr, "Execution failed", e

if __name__ == '__main__':
	main()
	