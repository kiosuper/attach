import subprocess
import gdb
import re

def normalize_argv(args, size=0):
	"""
	Normalize argv to list with predefined length
	from https://github.com/longld/peda
	"""
	args = list(args)
	for (idx, val) in enumerate(args):
		if to_int(val) is not None:
			args[idx] = to_int(val)
		if size and idx == size:
			return args[:idx]

	if size == 0:
		return args
	for i in range(len(args), size):
		args += [None]
	return args
def getprocname(relative=False):
	procname = None
	try:
		data = gdb.execute("info proc exe",to_string=True)
		procname = re.search("exe.*",data).group().split("=")[1][2:-1]
	except:
		data = gdb.execute("info files",to_string=True)
		if data:
			procname = re.search('Symbols from "(.*)"',data).group(1)
	if procname and relative :
		return procname.split("/")[-1]
	return procname

class at(gdb.Command):
	def __init__ (self):
		super (at, self).__init__ ("at", gdb.COMMAND_USER)

	def invoke (self, arg, from_tty):
		(processname,) = normalize_argv(arg,1)
		if not processname :
			processname = getprocname(relative=True)
			if not processname :
				print("Attaching program: ")
				print("No executable file specified.")
				print("Use the \"file\" or \"exec-file\" command.")
				return
		try :
			print("Attaching to %s ..." % processname)
			pidlist = subprocess.check_output("pidof " + processname,shell=True).decode('utf8').split()
			gdb.execute("attach " + pidlist[0])
		except :
			print( "No such process" )
			return
at()