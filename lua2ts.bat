@echo off
for %%a in (%*) do (
   echo convert to ts: "%%~na"
   python E:\WorkRoot\LuaToTypeScript\lua2ts.py "%%~na"
)
pause