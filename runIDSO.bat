set DSDirectory=C:\Users\swathi\Dropbox\ITDTESPlatform\DistributionSystem
set DistFeederDir=%DSDirectory%\DistributionFeeder\IEEE123
set InputFilesDir=%DSDirectory%\InputFiles
set YAMLFilesDir=%InputFilesDir%\YAMLFiles
set JsonFilesDir=%InputFilesDir%\JsonFiles
set OutputFilesDir=%DSDirectory%\OutputFiles
set LogFilesDir=%OutputFilesDir%\LogFiles
set PlotFilesDir=%OutputFilesDir%\PlotFiles
set GLDOutcomesDir=%OutputFilesDir%\GLDOutcomes


set "NDay=2"
set "NHour=4"
set "deltaT=300"
set "NoOfHouses=927"
set "NDistSys=1"
set "DistFeederFileName=IEEE123Feeder"
set /a "tmax=%NDay%*86400+%NHour%*3600"
set /a "NoOfProcesses=%NoOfHouses%+%NDistSys%+1"

set "C=2"
rem choose 0 for FRP, 1 for PR, 2 for LF 

set "FRP=12"
set "PL=5000"
set "TPLR=500"
set "RefLoad=1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500"

md %OutputFilesDir% 2> nul
md %LogFilesDir% 2> nul
md %PlotFilesDir% 2> nul
md %GLDOutcomesDir% 2> nul

set FNCS_FATAL=no
set FNCS_LOG_STDOUT=yes
cd %DSDirectory%

set FNCS_LOG_LEVEL=DEBUG2
set FNCS_TRACE=NO
start /b cmd /c fncs_broker %NoOfProcesses% ^>%LogFilesDir%/broker.log 2^>^&1

set FNCS_LOG_LEVEL=
set FNCS_CONFIG_FILE=%YAMLFilesDir%/IDSO.yaml
start /b cmd /c python ./IDSO/IDSO.py %JsonFilesDir%/IDSO_registration.json %tmax% %deltaT% %NDistSys% %C% %FRP% %PL% %TPLR% %RefLoad% ^>%LogFilesDir%/IDSO.log 2^>^&1

set FNCS_LOG_LEVEL=DEBUG2
FOR /L %%i IN (1,1,%NDistSys%) DO start /b cmd /c gridlabd %InputFilesDir%/%DistFeederFileName%Modified%%i.glm ^>%LogFilesDir%/gridlabd%%i.log 2^>^&1

set FNCS_LOG_LEVEL=
runHouseholds927.bat
REM start /b cmd /c python ./House/HouseController.py ./InputFiles/JsonFiles/controller_registration_house_1A_1_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/house_1A_1.log 2^>^&1
REM start /b cmd /c python ./House/HouseController.py ./InputFiles/JsonFiles/controller_registration_house_1A_2_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/house_1A_2.log 2^>^&1
REM start /b cmd /c python ./House/HouseController.py ./InputFiles/JsonFiles/controller_registration_house_1A_3_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/house_1A_3.log 2^>^&1
REM start /b cmd /c python ./House/HouseController.py ./InputFiles/JsonFiles/controller_registration_house_1A_4_thermostat_controller.json %tmax% %deltaT% ^>%logfilesdir%/house_1A_4.log 2^>^&1
