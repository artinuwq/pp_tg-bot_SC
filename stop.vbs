Set WshShell = CreateObject("WScript.Shell")
strComputer = "."
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")
Set colProcessList = objWMIService.ExecQuery("Select * from Win32_Process Where CommandLine Like '%bot_main.py%'")

For Each objProcess in colProcessList
    objProcess.Terminate()
Next

Set colProcessList = Nothing
Set objWMIService = Nothing
Set WshShell = Nothing