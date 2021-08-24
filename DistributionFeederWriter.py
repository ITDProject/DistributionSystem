import sys
import random
import numpy as np
import yaml
import math
import os

FeederFolder= "IEEE123"
DistFeederPath = './DistributionFeeder/' + FeederFolder + "/"

InputFilesFolder = "./InputFiles/"
if not os.path.exists(InputFilesFolder):
    os.makedirs(InputFilesFolder)

YAMLFilesFolder = "YAMLFiles"
YAMLPath = os.path.join(InputFilesFolder,YAMLFilesFolder)
if not os.path.exists(YAMLPath):
    os.makedirs(YAMLPath)

JsonFolder = "JsonFiles"
JsonPath = os.path.join(InputFilesFolder,JsonFolder)
if not os.path.exists(JsonPath):
    os.makedirs(JsonPath)

HousePath = './House/'

if len(sys.argv) == 8:
	DistFeederFileName = (sys.argv[1])
	FeederLoadFileName = (sys.argv[2])
	NDistSys = int(sys.argv[3])
	Mix = int(sys.argv[4])
	Type = int(sys.argv[5])
	Bus = int(sys.argv[6])
	AvgValue = int(sys.argv[7])
elif len(sys.argv) == 7:
	DistFeederFileName = (sys.argv[1])
	FeederLoadFileName = (sys.argv[2])
	NDistSys = int(sys.argv[3])
	Mix = int(sys.argv[4])
	Type = int(sys.argv[5])
	Bus = int(sys.argv[6])
	AvgValue = 5000
elif len(sys.argv) == 6:
	DistFeederFileName = (sys.argv[1])
	FeederLoadFileName = (sys.argv[2])
	NDistSys = int(sys.argv[3])
	Mix = int(sys.argv[4])
	Type = int(sys.argv[5])
	Bus = 1
	AvgValue = 5000
elif len(sys.argv) == 5:
	DistFeederFileName = (sys.argv[1])
	FeederLoadFileName = (sys.argv[2])
	NDistSys = int(sys.argv[3])
	Mix = int(sys.argv[4])
	Type = 2
	Bus = 1
	AvgValue = 5000
elif len(sys.argv) == 4:
	DistFeederFileName = (sys.argv[1])
	FeederLoadFileName = (sys.argv[2])
	NDistSys = int(sys.argv[3])
	Mix = 0
	Type = 2
	Bus = 1
	AvgValue = 5000
elif len(sys.argv) == 3:
	DistFeederFileName = (sys.argv[1])
	FeederLoadFileName = (sys.argv[2])
	NDistSys = 1
	Mix = 0
	Type = 2
	Bus = 1
	AvgValue = 5000
elif len(sys.argv) == 1:
	DistFeederFileName = 'IEEE123Feeder.glm'
	FeederLoadFileName = 'IEEE123Nodes.txt'
	NDistSys = 1
	Mix = 0
	Type = 2
	Bus = 1
	AvgValue = 5000

f1 = open(DistFeederPath + DistFeederFileName, 'r')
linesFeeder = f1.readlines()

f2 = open(DistFeederPath + FeederLoadFileName, 'r')
linesLoads = f2.readlines()

objects = {}
objname = ''
NumNodes = 0
TotalHouses = 0
HouseController = 'HouseController'

# attributes related to HVAC 
cooling_COP = [3.5, 3.8, 4.1]
over_sizing_factor = [0.0, 0.1, 0.2]

# attributes related to size [Small Normal Large]
ceiling_height = [8, 8, 8]
number_of_stories = [1, 1, 2]
aspect_ratio = [1.5, 1.5, 1.5]
floor_area = [864, 1350, 2352]; 

# attributes related to thermal integrity [Poor Normal Good]
mass_internal_gain_fraction = [0.5, 0.5, 0.5]
mass_solar_gain_fraction = [0.5, 0.5, 0.5]
glass_type = ['GLASS', 'GLASS', 'LOW_E_GLASS'] 
glazing_layers = ['TWO', 'TWO', 'THREE']
airchange_per_hour = [1.5, 1, 0.5] 
Rroof = [19, 30, 48] 
Rdoors = [3, 3, 11] 
Rfloor = [4, 19, 30] 
Rwall = [11, 11, 22] 
window_frame = ['ALUMINIUM', 'THERMAL_BREAK', 'INSULATED']
#Rwindows = [0.79, 1.23, 3.26] #[Poor Normal Good]

# attributes related to interior-exterior types [Poor Normal Good]
exterior_ceiling_fraction = [1, 1, 1]
exterior_floor_fraction = [1, 1, 1]
exterior_wall_fraction = [1, 1, 1]
glazing_treatment = ['REFL', 'REFL', 'HIGH_S']
interior_surface_heat_transfer_coeff = [1.46, 1.46, 1.46]
interior_exterior_wall_ratio = [1.5, 1.5, 1.5]
total_thermal_mass_per_floor_area = [4.5, 4.0, 3.5]
number_of_doors = [1, 2, 4]
window_exterior_transmission_coefficient = [1.0, 0.6, 0.6]
window_wall_ratio = [0.15, 0.15, 0.15]

def genphaseslist(ph):
	res_list = []
	ph = ph.replace("\"","")
	ph = ph.replace(";","")
	for i in ph:
		if i == 'A' or i == 'B' or i == 'C':
			res_list.append(i)
	return res_list

for i in linesLoads:
	t = i.split()
	if len(t) != 0:
		if t[0] == 'object':
			objname = t[1]
			objects[objname] = {}
		if t[0] == 'name':
			objects[objname]['name'] = t[1].replace(";","")
		if t[0] == 'phases':
			objects[objname]['phases'] = t[1].replace(";","")
			objects[objname]['phases_list'] = genphaseslist(objects[objname]['phases'])
			objects[objname]['no_houses'] = {k: 0 for k in objects[objname]['phases_list']}
			objects[objname]['house_mix'] = [[0,0] for k in objects[objname]['no_houses']]
		if t[0] == 'voltage_A':
			objects[objname][ 'voltage_A'] = t[1].replace(";","")
		if t[0] == 'voltage_B':
			objects[objname][ 'voltage_B'] = t[1].replace(";","")
		if t[0] == 'voltage_C':
			objects[objname][ 'voltage_C'] = t[1].replace(";","")
		if t[0] == 'constant_power_A':
			objects[objname][ 'constant_power_A'] = t[1].replace(";","")
		if t[0] == 'constant_power_B':
			objects[objname][ 'constant_power_B'] = t[1].replace(";","")
		if t[0] == 'constant_power_C':
			objects[objname][ 'constant_power_C'] = t[1].replace(";","")
		if t[0] == 'constant_current_A':
			objects[objname][ 'constant_current_A'] = t[1].replace(";","")
		if t[0] == 'constant_current_B':
			objects[objname][ 'constant_current_B'] = t[1].replace(";","")
		if t[0] == 'constant_current_C':
			objects[objname][ 'constant_current_C'] = t[1].replace(";","")
		if t[0] == 'constant_impedance_A':
			objects[objname][ 'constant_impedance_A'] = t[1].replace(";","")
		if t[0] == 'constant_impedance_B':
			objects[objname][ 'constant_impedance_B'] = t[1].replace(";","")
		if t[0] == 'constant_impedance_C':
			objects[objname][ 'constant_impedance_C'] = t[1].replace(";","")
		if t[0] == 'nominal_voltage':
			objects[objname][ 'nominal_voltage'] = t[1].replace(";","")
		if t[0] == '}':
			objname = ''

for objname,objdata in objects.items():
	NumNodes = NumNodes + len(objects[objname]['phases_list'])
	for ph in objdata['phases_list']:
		no_houses = 0
		for k, v in objdata.items():
			nom_volt = float(objdata['nominal_voltage'])
			if k == 'constant_power_' + ph:
				no_houses = no_houses + math.ceil(math.sqrt(complex(v).real* complex(v).real+ complex(v).imag*complex(v).imag)/AvgValue)
				#print('no_houses:', no_houses, flush = True)
			if k == 'constant_current_' + ph:
				no_houses = no_houses + math.ceil(abs((nom_volt)*complex(v))/AvgValue)
				#print('no_houses:', no_houses, flush = True)
			if k == 'constant_impedance_' + ph:
				no_houses = no_houses + math.ceil(abs((nom_volt*nom_volt)/complex(v))/AvgValue)
				#print('no_houses:', no_houses, flush = True)
		objects[objname]['no_houses'][ph] = no_houses
		TotalHouses = TotalHouses + no_houses

for objname,objdata in objects.items():
	objects[objname]['house_mix'] = {j : [Type-1 for i in range(v)] for j,v in objects[objname]['no_houses'].items()}

print('TotalHouses:', TotalHouses)
print('Nodes:', NumNodes, flush = True)

HouseBatchFile = 'runHouseholds' + str(TotalHouses) + '.bat'
f3 = open(HouseBatchFile,'w')

#print('DistFeederFileName: ', DistFeederFileName)
if DistFeederFileName.startswith('.'):
	DistFeederFileName = DistFeederFileName.replace('.', '', 1)
	DistFeederFileName = DistFeederFileName.replace(chr(92), '')
#print('DistFeederFileName: ', DistFeederFileName)

feederName = DistFeederFileName.split('.')[0]
glm = '.glm'
#print('feederName: ', feederName)

# scedulesFolder= "schedules"
# scedulesPath = './DistributionFeeder/' + scedulesFolder + "/"

for i in range(NDistSys):
	feederHouse = feederName + 'Modified' + str(NDistSys) + glm
	f4 = open(InputFilesFolder + feederHouse,'w')
    
	# print('#set minimum_timestep=300', file=f4)
	# print('#set profiler=1', file=f4)
	# print('#set randomseed=10', file=f4)
    
	# print('clock {', file=f4)
	# print('     timezone CST+6CDT;', file=f4)
	# print("     starttime '2016-07-26 00:00:00';", file=f4)
	# print("     stoptime '2016-07-29 06:00:00';", file=f4)
	# print('}', file=f4)
    
	# print('module tape;', file=f4)
	# print('module connection;', file=f4)
	# print('module climate;', file=f4)
    
	# print('module powerflow {', file=f4)
	# print('     solver_method FBS;', file=f4)
	# print('     warning_undervoltage 0.95 pu;', file=f4)
	# print('     warning_overvoltage 1.05 pu;', file=f4)
	# print('     line_limits TRUE;', file=f4)
	# print('}', file=f4)

	# print('module residential {', file=f4)
	# print('     implicit_enduses NONE;', file=f4)
	# print('     ANSI_voltage_check TRUE;', file=f4)
	# print('}', file=f4)

	# print('#include "'+ scedulesPath + 'appliance_schedules.glm";', file=f4)
	# print('#include "'+ scedulesPath + 'water_schedule.glm";', file=f4)
 
	# print('object climate {', file=f4)
	# print('     name weather;', file=f4)
	# print('     tmyfile "./Weather/TX_Midland_International_Ap.tmy3";', file=f4)
	# print('     interpolate QUADRATIC;', file=f4)
	# print('}', file=f4)
    
	for l in linesFeeder:
		print(l, file=f4, end="")
    
	print('', file=f4)
	print('object fncs_msg {', file=f4)
	print('     name gridlabdSimulator' + str(i+1) + ';', file=f4)
	print('     parent network_node;', file=f4)
	print('     configure '+ InputFilesFolder + feederName + 'Modified' + str(NDistSys)+'_FNCS_Config.txt;', file=f4)
	print('    option "transport:hostname localhost, port 5570";', file=f4)
	print('}', file=f4)
    
	for objname,objdata in objects.items():
		data = {'node': {'name' : '', 'phases': '', 'voltage_A': '', 'voltage_B': '', 'voltage_C': '', 'nominal_voltage': 0.0},
		'transformer':{'name' : '', 'phases': '', 'from': '', 'to' : '', 'configuration':''},
		'triplex_node_1' : {'name' : '', 'phases' : '', 'nominal_voltage': 0.0},
		'triplex_line' : {'name' : '', 'phases':'', 'from' : '', 'to':'', 'length': '', 'configuration': ''},
		'triplex_node_2' : {'name' : '', 'phases' : '', 'nominal_voltage': 0.0},
		'triplex_meter' : {'name' : '', 'parent' : '', 'groupid': '', 'phases':'', 'nominal_voltage':0.0},
		'house' : {'name' : '', 'parent' : ''}
		}
		for key,val in objdata.items():
			if key == 'name' or key == 'phases' or key == 'voltage_A' or key == 'voltage_B' or key == 'voltage_C' or key == 'nominal_voltage':
				data['node'][key] = val
		
		print('object node:'+data['node']['name']+ ' {', file=f4)
		for k,v in data['node'].items():
			if k == 'name':
				print(k, 'n'+str(v) + ';', file=f4)
			else:
				print(k, str(v) + ';', file=f4)
		print("}", file=f4)
		
		val = objdata['phases_list']
		for ph in val:
			data['transformer']['name'] = 'center_tap_' + str(data['node']['name']) + str(ph)
			data['triplex_node_1']['name'] = 'triplex_node_' + str(data['node']['name']) + str(ph)
			data['transformer']['phases'] = str(ph) + 'S'
			data['transformer']['from'] = 'n'+ str(data['node']['name'])
			data['transformer']['to'] = data['triplex_node_1']['name']
			data['transformer']['configuration'] = str(ph) + 'S_config'
			data['triplex_node_1']['phases'] = str(ph) + 'S'
			data['triplex_node_1']['nominal_voltage'] = 120
			
			for key, val in data.items():
				if key == 'triplex_node_1':
					print('object triplex_node {', file=f4)
					for k,v in val.items():
						print(k, str(v) + ';', file=f4)
					print("}", file=f4)
				if key == 'transformer':
					print('object ' + key + ' {', file=f4)
					for k,v in val.items():
						print(k, str(v) + ';', file=f4)
					print("}", file=f4)

			HouseNo = objects[objname]['no_houses'][ph]
			for j in range(HouseNo):
				data['triplex_line']['name'] = 'triplex_line_' + str(data['node']['name']) + str(ph) + '_' + str(j+1)
				data['triplex_node_2']['name'] = 'triplex_node_' + str(data['node']['name']) + str(ph)+ '_' + str(j+1)
				data['triplex_meter']['name'] = 'triplex_meter_' + str(data['node']['name'])+ str(ph) + '_' + str(j+1)
				house_index = str(data['node']['name'])+ str(ph) + '_' + str(j+1)
				data['house']['name'] = 'house_'+ house_index
				if i ==0:
					print('start /b cmd /c python ' + HousePath + HouseController + '.py '+ JsonPath +'/controller_registration_'+data['house']['name']+'_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/'+data['house']['name']+'.log 2^>^&1', file = f3)
				
				data['triplex_line']['phases'] = str(ph) + 'S'
				data['triplex_line']['from'] = data['triplex_node_1']['name']
				data['triplex_line']['to'] = data['triplex_node_2']['name']
				data['triplex_line']['length'] = '100 ft'
				data['triplex_line']['configuration'] = 'triplex_line_configuration_1'
				
				data['triplex_node_2']['phases'] = str(ph) + 'S'
				data['triplex_node_2']['nominal_voltage'] = 120
				
				
				data['triplex_meter']['parent'] = data['triplex_node_2']['name']
				data['triplex_meter']['groupid'] = 'triplex_node_meter'+ str(data['node']['name']) + str(ph)
				data['triplex_meter']['phases'] = str(ph) + 'S'
				data['triplex_meter']['nominal_voltage'] = 120
				
				data['house']['parent'] = data['triplex_meter']['name']
				for key, val in data.items():
					if key == 'triplex_node_2':
						print('object triplex_node {', file=f4)
						for k,v in val.items():
							print(k, str(v) + ';', file=f4)
						print("}", file=f4)
					if key == 'triplex_line' or key == 'triplex_meter':
						print('object ' + key + ' {', file=f4)
						for k,v in val.items():
							print(k, str(v) + ';', file=f4)
						print("}", file=f4)
					if key == 'house':
						print('object ' + key + ' {', file=f4)
						for k,v in val.items():
							print(k, str(v) + ';', file=f4)
						
						rand_param = round(random.uniform(68,76),2)
						rand_param = 72
						print('air_temperature ' + str(rand_param) + ';', file=f4)
						print('mass_temperature ' + str(rand_param) + ';', file=f4)
						print('heating_system_type ', end='', file=f4)
						x=np.random.random_sample()
						if x<=1:
							print('GAS;',file=f4)
						elif x>=0.7112 and x<0.8722:
							print('HEAT_PUMP;',file=f4)
						else:
							print('RESISTANCE;',file=f4)
							
						print('cooling_system_type ', end='',file=f4)
						if x<=1:
							if x <= 1:
								print('ELECTRIC;',file=f4)
							else:
								print('NONE;',file=f4)
						
						print('fan_type ONE_SPEED;',file=f4)						
						print('thermostat_control NONE;', file=f4)
						
						RN = random.uniform(0,1)
						print('system_mode COOL;', file=f4)

						house_mix = objects[objname]['house_mix'][ph]
						if Mix == 1:
							rand_house = int(random.uniform(0,3))
						else:
							rand_house = house_mix[j]
						#print('rand_house: '+str(rand_house))
						
						# attributes related to HVAC [L M H]
						print('cooling_COP ' + str(cooling_COP[rand_house]) +';', file=f4)
						print('over_sizing_factor ' + str(over_sizing_factor[rand_house]) +';', file=f4)
						
						
						# attributes related to size [Small Normal Large]
						print('ceiling_height ' + str(ceiling_height[rand_house]) +';', file=f4)
						print('number_of_stories ' + str(number_of_stories[rand_house]) +';', file=f4)
						print('aspect_ratio ' + str(aspect_ratio[rand_house]) +';', file=f4)
						print('floor_area ' + str(floor_area[rand_house])+';', file=f4)
						
						# attributes related to thermal integrity [Poor Normal Good]
						print('mass_internal_gain_fraction ' + str(mass_internal_gain_fraction[rand_house]) +';', file=f4)
						print('mass_solar_gain_fraction ' + str(mass_solar_gain_fraction[rand_house]) +';', file=f4)
						print('glass_type ' + str(glass_type[rand_house]) +';', file=f4)
						print('glazing_layers ' + str(glazing_layers[rand_house]) +';', file=f4)
						print('airchange_per_hour ' + str(airchange_per_hour[rand_house]) +';', file=f4)
						print('Rroof ' + str(Rroof[rand_house]) +';', file=f4)
						print('Rdoors ' + str(Rdoors[rand_house]) +';', file=f4)
						print('Rfloor ' + str(Rfloor[rand_house]) +';', file=f4)
						print('Rwall ' + str(Rwall[rand_house]) +';', file=f4)
						#print('Rwindows ' + str(Rwindows[rand_house]) +';', file=f4)
						print('window_frame ' + str(window_frame[rand_house]) +';', file=f4)

						# attributes related to interior-exterior types [Poor Normal Good]
						print('exterior_ceiling_fraction ' + str(exterior_ceiling_fraction[rand_house]) +';', file=f4)
						print('exterior_floor_fraction ' + str(exterior_floor_fraction[rand_house]) +';', file=f4)
						print('exterior_wall_fraction ' + str(exterior_wall_fraction[rand_house]) +';', file=f4)
						print('glazing_treatment ' + str(glazing_treatment[rand_house]) +';', file=f4)
						print('interior_surface_heat_transfer_coeff ' + str(interior_surface_heat_transfer_coeff[rand_house]) +';', file=f4)
						print('interior_exterior_wall_ratio ' + str(interior_exterior_wall_ratio[rand_house]) +';', file=f4)
						print('total_thermal_mass_per_floor_area ' + str(total_thermal_mass_per_floor_area[rand_house]) +';', file=f4)
						print('number_of_doors ' + str(number_of_doors[rand_house]) +';', file=f4)
						print('window_exterior_transmission_coefficient ' + str(window_exterior_transmission_coefficient[rand_house]) +';', file=f4)
						print('window_wall_ratio ' + str(window_wall_ratio[rand_house]) +';', file=f4)
						
						rand_param = int(random.uniform(-1000,1000))
						
						
						print('object occupantload {', file=f4)
						print('number_of_occupants 1;' , file=f4)
						print('occupancy_fraction 1.0;' , file=f4)
						print('};', file=f4)
						
						print('object ZIPload {', file=f4)
						print('name lights_' + house_index + ";", file=f4)
						print('schedule_skew ' + str(rand_param) + ";", file=f4)
						print('base_power LIGHTS*2;', file=f4)
						print('current_fraction 0;', file=f4)
						print('impedance_fraction 1;', file=f4)
						print('power_fraction 0;', file=f4)
						print('current_pf 0;', file=f4)
						print('impedance_pf 1;', file=f4)
						print('power_pf 0;', file=f4)
						print('heat_fraction 0.8;', file=f4)
						print('};', file=f4)
						
						x2=np.random.random_sample()
						if x2<=1:
							print('object ZIPload {', file=f4)
							print('name clotheswasher_' + house_index + ";", file=f4)
							print('schedule_skew ' + str(rand_param) + ";", file=f4)
							print('base_power CLOTHESWASHER*1;', file=f4)
							print('current_fraction 0;', file=f4)
							print('impedance_fraction 0;', file=f4)
							print('power_fraction 1;', file=f4)
							print('current_pf 0.97;', file=f4)
							print('impedance_pf 0.97;', file=f4)
							print('power_pf 0.97;', file=f4)
							print('heat_fraction 0.8;', file=f4)
							print('};', file=f4)
						
						x3=np.random.random_sample()
						if x3<=1:
							print('object ZIPload {', file=f4)
							print('name refrigerator_' + house_index + ";", file=f4)
							print('schedule_skew ' + str(rand_param) + ";", file=f4)
							print('base_power REFRIGERATOR*1;', file=f4)
							print('current_fraction 0;', file=f4)
							print('impedance_fraction 0;', file=f4)
							print('power_fraction 1;', file=f4)
							print('current_pf 0.97;', file=f4)
							print('impedance_pf 0.97;', file=f4)
							print('power_pf 0.97;', file=f4)
							print('heat_fraction 0.8;', file=f4)
							print('};', file=f4)
						
						x4=np.random.random_sample()
						
						if x4<=1:
							print('object ZIPload {', file=f4)
							print('name dryer_' + house_index + ";", file=f4)
							print('schedule_skew ' + str(rand_param) + ";", file=f4)
							print('base_power DRYER*1;', file=f4)
							print('current_fraction 0.1;', file=f4)
							print('impedance_fraction 0.8;', file=f4)
							print('power_fraction 0.1;', file=f4)
							print('current_pf 0.9;', file=f4)
							print('impedance_pf 1.0;', file=f4)
							print('power_pf 0.9;', file=f4)
							print('heat_fraction 0.8;', file=f4)
							print('};', file=f4)
						
						x5=np.random.random_sample()
						
						if x5<=1:
							print('object ZIPload {', file=f4)
							print('name freezer_' + house_index + ";", file=f4)
							print('schedule_skew ' + str(rand_param) + ";", file=f4)
							print('base_power FREEZER*1;', file=f4)
							print('current_fraction 0;', file=f4)
							print('impedance_fraction 0;', file=f4)
							print('power_fraction 1;', file=f4)
							print('current_pf 0.97;', file=f4)
							print('impedance_pf 0.97;', file=f4)
							print('power_pf 0.97;', file=f4)
							print('heat_fraction 0.8;', file=f4)
							print('};', file=f4)

						x6=np.random.random_sample()
						if x6<=1:
							print('object ZIPload {', file=f4)
							print('name range_' + house_index + ";", file=f4)
							print('schedule_skew ' + str(rand_param) + ";", file=f4)
							print('base_power RANGE*1;', file=f4)
							print('current_fraction 0;', file=f4)
							print('impedance_fraction 1;', file=f4)
							print('power_fraction 0;', file=f4)
							print('current_pf 0;', file=f4)
							print('impedance_pf 1;', file=f4)
							print('power_pf 0;', file=f4)
							print('heat_fraction 0.8;', file=f4)
							print('};', file=f4)

						print('object ZIPload {', file=f4)
						print('name microwave_' + house_index + ";", file=f4)
						print('schedule_skew ' + str(rand_param) + ";", file=f4)
						print('base_power MICROWAVE*1;', file=f4)
						print('current_fraction 0;', file=f4)
						print('impedance_fraction 0;', file=f4)
						print('power_fraction 1;', file=f4)
						print('current_pf 0.97;', file=f4)
						print('impedance_pf 0.97;', file=f4)
						print('power_pf 0.97;', file=f4)
						print('heat_fraction 0.8;', file=f4)
						print('};', file=f4)
						
						print('}', file=f4)

AgentType = 'IDSO'

auction_datayaml = {}
auction_datayaml['name'] = AgentType + '_' + str(Bus) 
auction_datayaml['time_delta'] = '1s'
auction_datayaml['broker'] = 'tcp://localhost:5570'
auction_datayaml['values'] = {}
auction_datayaml['values']['DALMP'] = {'topic': 'ames/DALMPAtBus' + str(Bus), 'default': 1}
auction_datayaml['values']['RTLMP'] = {'topic': 'ames/RTLMPAtBus' + str(Bus), 'default': 1}

for k in range(NDistSys):
	auction_datayaml['values']['distribution_load#'+'gridlabdSimulator'+str(k+1)] = {'topic': 'gridlabdSimulator'+str(k+1)+'/distribution_load', 'default': 0.0}
	auction_datayaml['values']['distribution_energy#'+'gridlabdSimulator'+str(k+1)] = {'topic': 'gridlabdSimulator'+str(k+1)+'/distribution_energy', 'default': 0.0}

for i in range(NDistSys):
	for objname,objdata in objects.items():
		datayaml = {'node': {'name' : ''},
		'house' : {'name' : '', 'parent' : ''}
		}
		for key,val in objdata.items():
			if key == 'name':
				datayaml['node'][key] = val
		
		val = objdata['phases_list']
		for ph in val:
			HouseNo = objects[objname]['no_houses'][ph]
			for j in range(HouseNo):
				house_index = str(datayaml['node']['name'])+ str(ph) + '_' + str(j+1)
				datayaml['house']['name'] = 'house_'+ house_index
				
				for k in range(NDistSys):
					auction_datayaml['values']['hvac_load#' + 'gridlabdSimulator' + str(k+1) + '#' + datayaml['house']['name']] = {'topic' :'gridlabdSimulator' + str(k+1) + '/' + datayaml['house']['name']+'/hvac_load', 'default' : 0.0}
				
				details = {'topic':'controller_'+datayaml['house']['name']+'_thermostat_controller/TransactiveAgentOutput', 'default': {"controller":{datayaml['house']['name']:{"pistar":{"propertyType":"double","propertyUnit":"none","propertyValue":0.0},"P":{"propertyType":"double","propertyUnit":"none","propertyValue":0.0},"P_ON":{"propertyType":"double", "propertyUnit": "none", "propertyValue": 0.0},"state":{"propertyType":"string","propertyUnit":"none","propertyValue":"ON"}}}}}
				auction_datayaml['values'][datayaml['house']['name']] = details

with open( YAMLPath + '/' + AgentType + '.yaml', 'w') as outfile: 
    yaml.dump(auction_datayaml, outfile, default_flow_style=False)