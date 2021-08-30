# DistributionSystem

This site gathers together ITD Project work on the modeling of distribution systems relevant for the modeling of Integrated Transmission and Distribution (ITD) systems.

The code/data in this repository are provided in support of ITD TES Platform that is developed as part of our ITD project. The details of this project can be found at http://www2.econ.iastate.edu/tesfatsi/ITDProjectHome.htm

Currently, this repository is only supported on a Windows operating system.

Installation Instructions:

#. Install Python
    
   Python can be installed using any of the following choices:
    
   Choice 1: Install Python using the Anaconda Distribution, available for downloading from https://www.anaconda.com/distribution/
   Check https://docs.anaconda.com/anaconda/install/windows/ for installation instructions. 

   Choice 2: Install Python using the Miniconda installer following the instructions given at https://conda.io/miniconda.html 
   Note: Pay particular attention to how the conda package manager is used to install various required modules such as numpy. 

   Choice 3: Install standard Python from https://www.python.org/ . The optional ‘pip’ is needed to install modules such as numpy.
	
   Note: The current study used the Miniconda installer from https://docs.conda.io/en/latest/miniconda.html to install Python (V3) at the location 	
   C:\Miniconda3

   Add C:/Miniconda3 to path (python.exe is located at C:\Miniconda3) to recognize Python from cmd (or powershell) else only conda prompt knows Python.
	
   Add C:/Miniconda3/Scripts and C:Miniconda3/Library/bin to use conda to install packages.

   Verify installation using "Python --version" command prompt.  
	
   Verify access to pip and conda (by typing pip/conda).
	
   To install modules, use 'pip install ModuleName' or 'conda install ModuleName'.
	
   To uninstall modules, use 'pip uninstall ModuleName' or 'conda uninstall ModuleName'.

   Note: For “version” command line prompts, Python requires the use of a double hyphen “- -version”.

#. Install GridLAB-D with FNCS as prerequisite by following the instructions at
   http://gridlab-d.shoutwiki.com/wiki/Building_GridLAB-D_on_Windows_with_MSYS2#Building_GridLAB-D_from_Source


Steps involved in execution:

#. Generate distribution system feeder populated with households with the choice of 'Household Type' by executing the following:

   python DistributionFeederWriter.py DistFeederFileName FeederLoadFileName NDistSys Mix Type TxBus
   
   The above commands depend on the following user-specified parameters: 
   
   * DistFeederFileName - The name of the distribution feeder file, e.g. IEEE123.glm, IEEE13.glm, etc
   
   * FeederLoadFileName - The name of the file that has original feeder load details
   
   * NDistSys - The number of distribution systems that are handled by the IDSO
   
   * Mix - Represents if the chosen households are a mix of different structure types or single structure type;
     
     * Mix is set to 0: A single structure type, set by input parameter 'Type' described below, is chosen to populate the distribution system feeder;
     
     * Mix is set to 1: A mix of structure types Low, Medium, High are used to populate the distribution system feeder;
	 
   * Type - Represents household's structure quality type; 
     
     * Set Type to 1 for Low Structure Quality Type;
     
     * Set Type to 2 for Medium Structure Quality Type;
     
     * Set Type to 3 for High Structure Quality Type;
	   
   * TxBus - The transmission bus to which the distribution system is considered to be connected to (Note: This input is needed if this model is used within an ITD system, else it defaults to 1)
   
   (Example usage: python DistributionFeederWriter.py IEEE123Feeder.glm IEEE123LoadObjects.txt 1 0 2 1)
   
   Outcomes: Distribution feeder populated by houses and a 'Yaml' file for IDSO. IDSO yaml file would contain all necessary details required to communicate with distribution agents (and transmission agents if this model is used within an ITD). 
    
#. Generate required additional files by executing the following command:
   
   python AgentPrep.py FileName NDistSys TxBus
   
   The above commands depend on the following user-specified parameters: 
   
   * FileName - The name of the distribution feeder generated in the above step
   
   * NDistSys - The number of distribution systems that are handled by the IDSO
   
   * TxBus - The transmission bus to which the distribution system is considered to be connected to (Note: This input is needed if this model is used within an ITD system, else it defaults to 1)
   
   (Example usage: python AgentPrep.py IEEEModified1 1 1)  
    		
   Outcomes: FNCS configuration txt file and json registration files for IDSO and households.
   FNCS configuration txt file contains needed input information for configuring GridLAB-D subscriptions and publications. IDSO json file contains needed input information for the IDSO and Household json file contains household specific information (household attributes).
	
#. Set the following parameters in the runIDSO.bat
   
   * NDay - Number of days the simulation needs to be carried out
   
   * NHour - Number of additional hours the simulation needs to be carried out after the simulation is run for NDay
   
   * deltaT - Length (seconds) of each control-step of the Five-Step TES design
   
   * NoOfHouses - Number of households connected to the distribution system feeder
   
   * NDistSys - Number of distribution systems monitored by the IDSO
   
   * DistFeederFileName - The name of the distribution feeder file given in Step 1 (without '.glm' extension), e.g. IEEE123, IEEE13, etc
   
   * C - Choose an appropriate case; 
     
     * Set C to 0 for generating test case outcomes with a flat retail price. Also set FRP(cents/kWh) to user specified retail price 
     
     * Set C to 1 for generating test case outcomes for 'Test Case 2: IDSO Peak Load Reduction Capabilities'. Also set PL(kW) and TPLR(kW) to user specified values
     
     * Set C to 2 for generating test case outcomes for 'Test Case 3: IDSO Load Matching Capabilities'. Also set RefLoad
   
   * DSDirectory - Set the path of this repository folder to DSDirectory
	
#. Run all the distribution system processes by executing the following command:

   runIDSO.bat
   
   (Additional Notes: User can end the simulation run in the middle of the run by executing 'kill5570.bat'. Executing 'list5570.bat' lists all the processes. If you perform 'kill5570.bat', make sure 'list5570.bat'shows no process before executing another 'runIDSO.bat' operation. 
