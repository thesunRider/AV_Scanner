#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
#AutoIt3Wrapper_Icon=icon.ico
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
#include <Security.au3>
#include <File.au3>
#include <Process.au3>

$auth = (@ComputerName&"\" &@UserName)
Local $tSID = _Security__GetAccountSid(@UserName)
$frd = FileRead(@ScriptDir &"\dependencies\launchjvsoft.xml")
$fl = FileOpen(@ScriptDir &"\dependencies\lunch.xml",$FO_OVERWRITE )
FileWrite($fl,StringReplace(StringReplace(StringReplace(StringReplace($frd,"$AUTH$",$auth),"$USERSID$",_Security__SidToStringSid ( $tSID)),"$EXECMD$",@ScriptDir &'\av_scanner.exe'),"$CURDIR$",@ScriptDir))
FileClose($fl)

_RunDos('schtasks.exe /create /xml "'&@ScriptDir&'\dependencies\lunch.xml" /TN "launchjvsoft"'); $STDOUT_CHILD
If @CPUArch == "x86" Then
RunWait(@ScriptDir &"\dependencies\MicrosoftEdgeWebView2RuntimeInstallerX86.exe")
RunWait(@ScriptDir &"\dependencies\VC_redist.x86.exe")
Else
RunWait(@ScriptDir &"\dependencies\MicrosoftEdgeWebView2RuntimeInstallerX64.exe")
RunWait(@ScriptDir &"\dependencies\VC_redist.x64.exe")
EndIf

DirRemove(@ScriptDir&"\dependencies\",1 )
exit