@echo off
title CJU-coin
echo.
echo.
echo *** Welcome to CJU-coin Mining System ***
echo *** ��������(CJU-coin) ä�� �ý��ۿ� ���Ű��� ȯ���մϴ�. ***

echo.
echo.

echo ä�� ��Ʈ��ũ ��ġ �� ������ ���ؼ��� ������ ������ �ʿ��մϴ�.
echo ����ڷκ��� ������ ���� ����� ����޾ƾ� �մϴ�..
echo To continue setting up and cofiguring, we need "Adminstrator" permission.
echo Please allow the administrator's previlliage.
echo.
echo.
if not "%1"=="am_admin" (
	echo.
	echo We will move you to allow screen Press Enter.
	set /p=������ ������ ����ϱ� ���� �̵��ϰڽ��ϴ�. ���͸� ġ����.  
)
echo.
echo.

:: Ref -> https://stackoverflow.com/questions/18755553/automatically-running-a-batch-file-as-an-administrator
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
echo.
echo.

echo ���̽� ��Ű�� ������ pip�� ��ġ�մϴ�...
echo Start upgrade python package manager (pip)...
python -m pip install --upgrade pip
echo.
echo done!
echo ��ġ ����!
echo.
echo.

echo Start installing virtualenv...
pip install virtualenv
echo done!
echo.
echo.

echo ���α׷� ���� ��ġ�� �̵��ؾ� �մϴ�...
echo We need to move into your directory (or folder).
set /p targetPath=��������(CJU-coin) ���̴� ���α׷� ���� Ǭ ���� ��θ� ����, �ٿ��ֱ� �� �ּ���: 
echo your target directory: %targetPath%
echo.
echo.

echo �Է��Ͻ� ��η� �̵��ϰڽ��ϴ�.
echo Move to your target directory
cd %targetPath%
dir
echo.
echo �۾���θ� Ȯ���߽��ϴ�.
echo.
echo.

echo ����ȯ���� ��ġ�ϰڽ��ϴ�...
echo Set up virtual environment......
echo After setting up "venv" folder will be appeared in your target directory
virtualenv venv
echo.
echo done!
echo ����ȯ�� ��ġ ����!
echo.
echo.

echo ��ġ�� ����ȯ���� Ȱ��ȭ �մϴ�.
echo Activate virtual environment......
call .\venv\Scripts\activate.bat
cd
echo.
echo done!
echo.
echo ����ȯ�� Ȱ��ȭ ����!
echo.
echo.


echo ��� ��ġ �� �ʿ��� ȯ�� ������ ���ƽ��ϴ�.
echo ��������(CJU-coin) ��ġ �� ä�� �ȳ� Ʃ�丮�� �������� �����ϰ� ��ġ�ڽ��ϴ�.
echo Open the tutorial page using default browser
echo.
pause
start "" ".\p2p_net/tutorial.html"
echo.
echo.
