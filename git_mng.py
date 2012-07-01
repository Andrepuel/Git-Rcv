import os
import sys
import subprocess

try:
	import git_rcv_assets
	hostname = git_rcv_assets.hostname
except:
	hostname = "localhost"

def returnPermission(dirpath,username):
	usersFile = open(os.path.join(os.path.expanduser(dirpath),"users"),"r")
	#TODO db-it
	permissions = {"READ":set(),"WRITE":set()}
	state = None
	for eachLine in usersFile:
		if eachLine[0] == "#":
			continue
		assert eachLine[-1] == "\n"
		if eachLine == "READ:\n":
			state = "READ"
			continue
		if eachLine == "WRITE:\n":
			state = "WRITE"
			continue
		assert state is not None
		permissions[state].add(eachLine[:-1])
	usersFile.close()	
	if username in permissions["WRITE"] or "*" in permissions["WRITE"]:
		return "WRITE"
	if username in permissions["READ"] or "*" in permissions["READ"]:
		return "READ"
	return "NULL"

def checkPermission(dirpath,username,access):
	gotAccess = returnPermission(dirpath,username)
	if gotAccess == "WRITE":
		return True
	return gotAccess == access

def checkowner(user,dir):
	owner = open(os.path.join(dir,"owner"),"r").readline()[:-1]
	return user == owner

def assertowner(user,dir):
	if not checkowner(user,dir):
		sys.stderr.writelines("Access denied 2-11\n")
		sys.exit(1)

def listRepos(dir,user,results):
	if os.path.exists(os.path.join(dir,"users")):
		result = ""
		result += dir
		gotPermission = returnPermission(dir,user)
		if gotPermission == "NULL":
			return
		result += " ("+returnPermission(dir,user)+")"
		if checkowner(user,dir):
			result += " (OWNER)"
		results.append(result)
		return
	for each in os.listdir(dir):
		if os.path.isdir(os.path.join(dir,each)):
			listRepos(os.path.join(dir,each),user,results)

def manage(user,*argv):
	command = argv[0]
	if len(argv) > 1:
		dir = argv[1]
	if command == "create-repo":
		try:
			os.makedirs(dir)
		except:
			sys.stderr.writelines("Access denied\n")
			sys.exit(1)
		os.chdir(dir)
		try:
			subprocess.check_call(["git","init","--bare"])
			owner = open("owner","w")
			owner.writelines(user+"\n")
			permissions = open("users","w")
			permissions.write("READ:\n*\nWRITE:\n"+user+"\n")
		except:
			sys.stderr.writelines("Error on repo creation\n")
			sys.exit(1)
		return
	if command == "receive-permissions":
		assertowner(user,dir)
		permissions = open(os.path.join(dir,"users"),"w")
		for i in sys.stdin:
			permissions.write(i)
		permissions.close()
		if( checkPermission(dir,"*","READ") ):
			subprocess.check_call(["chmod","-R","o+rx",dir])
		else:
			subprocess.check_call(["chmod","-R","o-rx",dir])
		return
	if command == "upload-permissions":
		assertowner(user,dir)
		permissions = open(os.path.join(dir,"users"),"r")
		for i in permissions:
			sys.stdout.write(i)
		return
	if command == "list-repos":
		result = []
		listRepos(".",user,result)
		for i in result:
			print os.environ["USER"]+"@"+hostname+":"+i[2:]
		return
