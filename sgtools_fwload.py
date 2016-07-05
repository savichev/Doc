#!/usr/bin/env python
import os,sys,commands,time

# ------------------------ Functions ------------------------ #
def convertHEX(number): # Converts decimal to HEX. Also, makes it 6 digits with leading zeros.
        x=hex(number)[2:]
        while(True):
                if(len(x)<6):
                        x='0'+x
                        continue
                else:

                        break
        return x

def codeloadmode5(filename,devices):
	global filepath
	if (os.path.exists(filepath + filename)==False):
		print "Error: File does not exist"
	else:
		for drive in devices:
			print "Drive %s" % drive
			size=os.path.getsize(filepath + filename)
			hexsize=convertHEX(size)
			output=commands.getoutput("sg_raw --send=%s --in=%s%s %s 3b 05 00 00 00 00 %s%s %s%s %s%s 00 00 00" % (size,filepath,filename,drive,hexsize[0],hexsize[1],hexsize[2],hexsize[3],hexsize[4],hexsize[5])).rstrip().split('\n')
			# Try again if failure				
			if (len(output)>1):output=commands.getoutput("sg_raw --send=%s --in=%s%s %s 3b 05 00 00 00 00 %s%s %s%s %s%s" % (size,filepath,filename,drive,hexsize[0],hexsize[1],hexsize[2],hexsize[3],hexsize[4],hexsize[5])).rstrip().split('\n')			
			# Print status				
			if (len(output)==1):print "Code Load Successful!"
			else:print "Error: Code Load Failed. => \n" + '\n'.join(output)
def codeloadmode7(filename,chunk,devices):
	global filepath
	if (chunk=='undefined'):
		print "Command cancelled."
		sys.exit()
	if chunk is None: chunk=input("Enter chunk size: ")
	if (os.path.exists(filepath+filename)==False):
		print "Error: File does not exist"	
	else:
		for drive in devices:
			chunk=int(chunk)
			print "Drive %s" % drive
			size=os.path.getsize(filepath+filename)
			hexchunk=convertHEX(chunk)
			iterations=size/chunk
			skip=0 # initialize skip value
			send=chunk # send value is equal to chunk except for last step
			i=0 # counter
			steps=0 # number of successful steps
			while(i<=iterations):
				# Get Hex for CDB
				if(i==iterations):
					send=size
					hexchunk=convertHEX(send)
				else:
					size=size-chunk
				# Get skip value
				if(i==0):skip=0
				else:skip=skip+chunk
				offset=convertHEX(skip)
				# Load file chunk
				output=commands.getoutput("sg_raw --skip=%s --send=%s --infile=%s%s %s 3B 07 00 %s%s %s%s %s%s %s%s %s%s %s%s 00 00 00" % (skip,send,filepath,filename,drive,offset[0],offset[1],offset[2],offset[3],offset[4],offset[5],hexchunk[0],hexchunk[1],hexchunk[2],hexchunk[3],hexchunk[4],hexchunk[5])).rstrip().split('\n')
				# Try again if failure		
				#if(len(output)>1): output=commands.getoutput("sg_raw --skip=%s --send=%s --infile=%s%s %s 3B 07 00 %s%s %s%s %s%s %s%s %s%s %s%s" % (skip,send,filepath,filename,drive,offset[0],offset[1],offset[2],offset[3],offset[4],offset[5],hexchunk[0],hexchunk[1],hexchunk[2],hexchunk[3],hexchunk[4],hexchunk[5])).rstrip().split('\n')
				# Successful steps counter
				#if (len(output)==1): steps+=1
				i+=1
			print "Code Load Successful!"
			#if (i==steps): print "Code Load Successful!"
			#else: print "Error: Code Load Failed. => " + ('\n' .join(output))
			
#-----------------------Help Functions---------------------#
def helpconfig(cmd,msg):
		print cmd + "\n--" + msg + '\n'
def help(): # Python GUI Help Page
	print "HELP PAGE\n"

	helpconfig("mode5","loads entered code file to drive(s) with mode 5\nExample: #./sgtools_fwload.py mode5 /root/firmware.lod /dev/sda")
	helpconfig("mode7","loads entered code file to drive(s) with mode 7 using entered chunk size\nExample: #./sgtools_fwload.py mode7 /root/firmware.lod /dev/sda 2048")

	helpconfig("exit","exits the program")
# ------------------------ Execute Commands ------------------------ #
def execute(inp):
	# Get drive to perform action on
	x=(len(inp)-1)
	drives=inp[x].split(' ')
	
	if(inp[1]=="help"):help()
	elif(inp[1]=="mode7"):codeloadmode7(inp[2],inp[3],drives)
	elif(inp[1]=="mode5"):codeloadmode5(inp[2],drives)
	else:print "Command does not exist. To see a list of commands and for help, type \"help\""
# ------------------------ Main Function ------------------------ #
def main():
	global filepath
	global logpath
	filepath = '/'
	logpath= '/'
	# Kills process in case hangs up
	commands.getoutput("killall sg_inq")
	commands.getoutput("killall sg_map")
	commands.getoutput("killall grep")
	execute(sys.argv)

main()

