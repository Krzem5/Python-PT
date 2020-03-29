echo off
echo NUL>_.class
del /s /f /q *.class
cls
javac Main.java
java Main
start /min cmd /c "echo NUL>_.class && del /s /f /q *.class"