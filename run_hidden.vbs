Set WshShell = CreateObject("WScript.Shell")
strPath = WshShell.CurrentDirectory & "\src\bot_main.py"
pythonCmd = "pythonw " & Chr(34) & strPath & Chr(34)
WshShell.Run pythonCmd, 0, False
Set WshShell = Nothing