=====
Usage
=====
**Steps involved in execution:**

#. Generate distribution grid populated with households with the choice of 'Household Type' by executing the following:

   python generateModifiedGrid.py FileName LoadFileName NDistSys Mix Type TxBus
   
   The above commands depend on the following user-specified parameters: 
   
   * FileName - The name of the input distribution grid model file, e.g. IEEE123.glm, IEEE13.glm, etc
   
   * LoadFileName - The name of the file that has original load details of the grid
   
   * NDistSys - The number of distribution systems that are handled by the IDSO
   
   * Mix - Represents if the chosen households are a mix of different structure types or single structure type;
     
     * Mix is set to 0: A single structure type, set by input parameter 'Type' described below, is chosen to populate the distribution grid;
     
     * Mix is set to 1: A mix of structure types Low, Medium, High are used to populate the distribution grid;
	 
   * Type - Represents household's structure quality type; 
     
     * Set Type to 1 for Low Structure Quality Type;
     
     * Set Type to 2 for Medium Structure Quality Type;
     
     * Set Type to 3 for High Structure Quality Type;
	   
   * TxBus - The transmission bus to which the distribution system is considered to be connected. (Note: This input is needed if this model is used within an ITD system, else it defaults to 1)
   
   Example usage: python generateModifiedGrid.py IEEE123Grid.glm IEEE123LoadObjects.txt 1 0 2 1;
   
   Outcomes:
   
   * A '.glm' file for the distribution system: It is the required distribution grid populated by households
   
   * A '.yaml' file for the IDSO: IDSO yaml file would contain all necessary details required to communicate with distribution agents (and transmission agents if this model is used within an ITD)
   
   * A '.bat' file for the households: It would contain the required code to run household processes, used in Step 4.
    
   Sample outcomes: IEEE123GridModified1.glm, IDSO.yaml, runHouseholds.bat
    
#. Generate required additional files by executing the following command:
   
   python agentPreparation.py FileName NDistSys TxBus
   
   The above commands depend on the following user-specified parameters: 
   
   * FileName - The name of the distribution grid generated in the above step
   
   * NDistSys - The number of distribution systems that are handled by the IDSO
   
   * TxBus - The transmission bus to which the distribution system is considered to be connected. (Note: This input is needed if this model is used within an ITD system, else it defaults to 1)
   
   Example usage: python agentPreparation.py IEEE123GridModified1 1 1
    		
   Outcomes: 
   
   * FNCS configuration txt file: It contains needed input information for configuring GridLAB-D subscriptions and publications
   
   * '.json' registration file for the IDSO: It contains the input information required to initialize the IDSO
   
   * '.json' registration files for the households: Each file contains input information (household attributes) specific to each household
   
   Sample outcomes: IEEE123GridModified1_FNCS_Config.txt, IDSO_registration.json, etc
   
   Note: 'agentPreparation.py' imports 'agentRegistration' class from 'agentRegistration.py'.
   
#. Set the following parameters in the runIDSO.bat
   
   * DSDirectory - Set the path of this repository folder to DSDirectory
   
   * NDay - Number of days the simulation needs to be carried out
   
   * NHour - Number of additional hours the simulation needs to be carried out after the simulation is run for NDay
   
   * deltaT - Length (seconds) of each control-step of the Five-Step TES design
   
   * NoOfHouseholds - Number of households connected to the distribution grid
   
   * NDistSys - Number of distribution systems monitored by the IDSO
   
   * FileName - The name of the input distribution grid model file given in Step 1 (without '.glm' extension), e.g. IEEE123, IEEE13, etc
   
   * C - Choose an appropriate case; 
     
     * Set C to 0 for generating test case outcomes with a flat retail price. Also set FRP(cents/kWh) to user specified retail price 
     
     * Set C to 1 for generating test case outcomes for 'Test Case 2: IDSO Peak Load Reduction Capabilities'. Also set PL(kW) and TPLR(kW) to user specified values
     
     * Set C to 2 for generating test case outcomes for 'Test Case 3: IDSO Load Matching Capabilities'. Also set RefLoad
   
	
#. Run all the distribution system processes by executing the following command:

   runIDSO.bat
   
   Note: All the files generated in the above steps are needed to run the distribution system processes.
   
**Miscellaneous Notes:** 

* Users can end a simulation run in the middle of the run by executing 'kill5570.bat'. Executing 'list5570.bat' lists all currently running processes. If you perform 'kill5570.bat', you should next run 'list5570.bat' to make sure it shows no process is running before you execute another 'runIDSO.bat' operation. 
* Note for developers: For 'import fncs' to work, the environmental variable $PATH needs to be appended to add the location of 'fncs.py'.
