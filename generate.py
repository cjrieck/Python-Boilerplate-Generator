#!/usr/bin/env python

import argparse
import os
import sys
import glob
from subprocess import Popen, PIPE, STDOUT, call

from functions import create_functions
from inputs import check_input
from packages import check_package, install_package

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

# def check_input(inputString): # in classes as well

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', default='pygenFile',help='name of the file you want to create')
	parser.add_argument('-p', '--path', nargs='?', default='./', help='destination path of the file')
	parser.add_argument('-i', '--imports', nargs='+', help='modules you want to import')
	parser.add_argument('-c', '--classes', nargs='+', help='names of classes you want to create')
	parser.add_argument('-f', '--functions', nargs='+', help='names of functions you want to create')
	
	parser.add_argument('-fw', '--framework', nargs='?', help='name of python framework')

	args = parser.parse_args()

	fileName = ""
	os.chdir(args.path)

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
			
			filelist = glob.glob("./*.py")
			newfile = args.file+".py"
			if any(newfile in s for s in filelist): 	#checks to see if file exists in a list of files in current directory
				print WARNING+BOLD+'Warning!'+ENDC+' About to overwrite '+BLUE+args.file+ENDC
			 	response = raw_input(CYAN+'Would you like to continue?'+ENDC+'[y/n] ')
			 	if response.lower() == 'n':
			 		sys.exit()
				else:
					os.remove(newfile)
	
			else:
			 	print 'Creating new file, '+BLUE+BOLD+newfile

			fileName = open(newfile, 'w')
			fileName.write("#!/usr/bin/env python\n\n")

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
								print 'Imported '+MODULE+module+ENDC
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
					className = className[0].upper()+className[1:] # uppercase class name
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
	stderr = ""
	try:
		returnCode = call('open '+args.file+'.py', shell=True)
		if returnCode < 0:
			print >>sys.stderr, "Child was terminated by signal", -returnCode
		else:
			print >>sys.stderr, "Child returned", returnCode
	except OSError, e:
		print >>sys.stderr, "Execution failed", e

if __name__ == '__main__':
	main()
	