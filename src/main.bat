@echo off

javac Main.java
if %ERRORLEVEL% EQU 0 java Main %1 %2
