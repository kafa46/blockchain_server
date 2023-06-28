@echo off
title CJU-coin
echo.
echo.
echo *** Welcome to CJU-coin Mining System ***
echo *** 씨쥬코인(CJU-coin) 채굴 시스템에 오신것을 환영합니다. ***

echo.
echo.

echo 채굴 네트워크 설치 및 설정을 위해서는 관리자 권한이 필요합니다.
echo 사용자로부터 관리자 권한 사용을 허락받아야 합니다..
echo To continue setting up and cofiguring, we need "Adminstrator" permission.
echo Please allow the administrator's previlliage.
echo.
echo.
if not "%1"=="am_admin" (
	echo.
	echo We will move you to allow screen Press Enter.
	set /p=관리자 권한을 허락하기 위해 이동하겠습니다. 엔터를 치세요.  
)
echo.
echo.

:: Ref -> https://stackoverflow.com/questions/18755553/automatically-running-a-batch-file-as-an-administrator
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
echo.
echo.

echo 파이썬 패키비 관리자 pip를 설치합니다...
echo Start upgrade python package manager (pip)...
python -m pip install --upgrade pip
echo.
echo done!
echo 설치 성공!
echo.
echo.

echo Start installing virtualenv...
pip install virtualenv
echo done!
echo.
echo.

echo 프로그램 파일 위치로 이동해야 합니다...
echo We need to move into your directory (or folder).
set /p targetPath=씨쥬코인(CJU-coin) 마이닝 프로그램 압축 푼 폴더 경로를 복사, 붙여넣기 해 주세요: 
echo your target directory: %targetPath%
echo.
echo.

echo 입력하신 경로로 이동하겠습니다.
echo Move to your target directory
cd %targetPath%
dir
echo.
echo 작업경로를 확인했습니다.
echo.
echo.

echo 가상환경을 설치하겠습니다...
echo Set up virtual environment......
echo After setting up "venv" folder will be appeared in your target directory
virtualenv venv
echo.
echo done!
echo 가상환경 설치 성공!
echo.
echo.

echo 설치된 가상환경을 활성화 합니다.
echo Activate virtual environment......
call .\venv\Scripts\activate.bat
cd
echo.
echo done!
echo.
echo 가상환경 활성화 성공!
echo.
echo.


echo 블록체인 데이터베이스를 초기화 합니다.
set FLASK_APP=server
set FLASK_DEBUG=True
flask db init
flask db migrate
flask db upgrade


echo 모든 설치 및 필요한 환경 설정을 마쳤습니다.
echo 씨쥬코인(CJU-coin) 설치 및 채굴 안내 튜토리얼 페이지를 실행하고 마치겠습니다.
echo Open the tutorial page using default browser
echo.
pause
start "" ".\p2p_net/tutorial.html"
echo.
echo.
