#	Copyright (C) 2017 Battelle Memorial Institute
import sys
import os
from agentRegistration import agentRegistration

InputFilesFolder = "./inputFiles/"
if not os.path.exists(InputFilesFolder):
    os.makedirs(InputFilesFolder)
    
jsonFolderName = "jsonFiles"

if len(sys.argv) == 4:
	FeederFileName = (sys.argv[1])
	NDistSys = int(sys.argv[2])
	Bus = int(sys.argv[3])
elif len(sys.argv) == 3:
	FeederFileName = (sys.argv[1])
	NDistSys = int(sys.argv[2])
	Bus = 1
elif len(sys.argv) == 2:
	FeederFileName = (sys.argv[1])
	NDistSys = 1
	Bus = 1

if FeederFileName.startswith('.'):
	FeederFileName = FeederFileName.replace('.', '', 1)
	FeederFileName = FeederFileName.replace(chr(92), '')

fileName = FeederFileName.split('.')[0]

auctions, controllers = agentRegistration(fileName, NDistSys, Bus, InputFilesFolder, jsonFolderName)

print ("launch_agents.sh executes", 2 + len (controllers), "processes")

want_logs = False

if want_logs:
	prefix = "(export FNCS_FATAL=NO && export FNCS_LOG_STDOUT=yes && exec"
else:
	prefix = "(export FNCS_FATAL=NO && exec"
suffix_auc = "&> auction.log &)"
suffix_gld = "&> gridlabd.log &)"

metrics = sys.argv[1]

for i in range(NDistSys):
	op = open(InputFilesFolder + fileName +"_FNCS_Config.txt", "w")
	print ("publish \"commit:network_node.distribution_load -> distribution_load\";", file=op)
	print ("publish \"commit:network_node.distribution_real_energy -> distribution_energy\";", file=op)
	for key, value in controllers.items():
		arg = value['controller_information']['houseName']
		MeterArg = 'triplex_meter' + arg.split('house')[1]
		TriplexNodeArg = 'triplex_node' + arg.split('house')[1]
		
		print ("publish \"commit:" + arg + ".system_mode -> " + arg + "/system_mode\";", file=op)
		
		print ("publish \"commit:" + arg + ".Qi -> " + arg + "/Qi\";", file=op)
		print ("publish \"commit:" + arg + ".solar_gain -> " + arg + "/solar_gain\";", file=op)
		print ("publish \"commit:" + arg + ".outdoor_temperature -> " + arg + "/outdoor_temperature\";", file=op)
		print ("publish \"commit:" + arg + ".outdoor_rh -> " + arg + "/outdoor_rh\";", file=op)
		print ("publish \"commit:" + MeterArg + ".voltage_12 -> " + MeterArg + "/voltage_12\";", file=op)
		
		print ("publish \"commit:" + arg + ".hvac_load -> " + arg + "/hvac_load\";", file=op)
		
		print ("subscribe \"precommit:" + arg + ".system_mode <- controller_" + key + "/gridlabdSimulator"+str(i+1)+"_system_mode\";", file=op)
		houseNumber = arg.split("_")
	op.close()