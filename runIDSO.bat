set DSDir=C:\Users\swathi\Dropbox\ITDTESPlatform\DistributionSystem

set DSInputFilesDir=%DSDir%\inputFiles
set DSJsonFilesDir=%DSInputFilesDir%\jsonFiles
set DSYAMLFilesDir=%DSInputFilesDir%\yamlFiles

set OutputFilesDir=%DSDir%\outputFiles
set LogFilesDir=%OutputFilesDir%\logFiles
set PlotFilesDir=%OutputFilesDir%\plotFiles

set "NDay=2"
set "NHour=4"
set "deltaT=300"
set "NoOfHouseholds=4"
set "NDistSys=1"
set "DistFeederFileName=IEEE123Feeder"
set /a "tmax=%NDay%*86400+%NHour%*3600"
set /a "NoOfProcesses=%NoOfHouseholds%+%NDistSys%+1"

set "C=2"
REM choose 0 for FRP, 1 for PR, 2 for LF 

set "FRP=12"
set "PL=5000"
set "TPLR=500"
set "RefLoad=1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500 1500"

md %OutputFilesDir% 2> nul
md %LogFilesDir% 2> nul
md %PlotFilesDir% 2> nul

set FNCS_FATAL=no
set FNCS_LOG_STDOUT=yes
set FNCS_TRACE=no
set FNCS_LOG_LEVEL=DEBUG2

start /b cmd /c fncs_broker %NoOfProcesses% ^>%LogFilesDir%/broker.log 2^>^&1

cd %DSDir%

set FNCS_LOG_LEVEL=
set FNCS_CONFIG_FILE=%DSYAMLFilesDir%/IDSO.yaml
start /b cmd /c python ./IDSO/IDSO.py %DSJsonFilesDir%/IDSO_registration.json %tmax% %deltaT% %NDistSys% %C% %FRP% %PL% %TPLR% %RefLoad% ^>%LogFilesDir%/IDSO.log 2^>^&1

set FNCS_LOG_LEVEL=DEBUG2
FOR /L %%i IN (1,1,%NDistSys%) DO start /b cmd /c gridlabd %DSInputFilesDir%/%DistFeederFileName%Modified%%i.glm ^>%LogFilesDir%/gridlabd%%i.log 2^>^&1

set FNCS_LOG_LEVEL=
runHouseholds927.bat