@REM @echo off
@REM set BATCH_DIR=%~dp0
@REM set JAVA_EXEC="%BATCH_DIR%Resources\jdk-14.0.1\bin\java.exe"
@REM set JVM_OPTIONS=-XX:+ShowCodeDetailsInExceptionMessages
@REM set CLASSPATH="%BATCH_DIR%Resources\Kenan\bin;%BATCH_DIR%Resources\NeticaJ_Win\NeticaJ_504\bin\x64_bin\NeticaJ.jar"
@REM set MAIN_CLASS=App
@REM set NETICA_MODEL="%BATCH_DIR%network\Balule.neta"
@REM set OUTPUT_FILE="%BATCH_DIR%output.cas"

@REM %JAVA_EXEC% %JVM_OPTIONS% -cp %CLASSPATH% %MAIN_CLASS% %NETICA_MODEL% %OUTPUT_FILE%


@echo off
set BATCH_DIR=%~dp0
set JAVA_EXEC="%BATCH_DIR%Resources\jdk-14.0.1\bin\java.exe"
set JAVAC_EXEC="%BATCH_DIR%Resources\jdk-14.0.1\bin\javac.exe"
set JVM_OPTIONS=-XX:+ShowCodeDetailsInExceptionMessages
set CLASSPATH="%BATCH_DIR%Resources\Kenan\bin;%BATCH_DIR%Resources\NeticaJ_Win\NeticaJ_504\bin\x64_bin\NeticaJ.jar"
set SOURCE_DIR="%BATCH_DIR%Resources\Kenan\src"
set MAIN_CLASS=App
set NETICA_MODEL="%BATCH_DIR%network\Balule.neta"
set OUTPUT_FILE="%BATCH_DIR%output.cas"

rem Compile Java source code
%JAVAC_EXEC% -cp %CLASSPATH% -d %BATCH_DIR%Resources\Kenan\bin %SOURCE_DIR%\*.java

rem Execute Java application
%JAVA_EXEC% %JVM_OPTIONS% -cp %CLASSPATH% %MAIN_CLASS% %NETICA_MODEL% %OUTPUT_FILE%


