echo
echo
echo "CJU-coin"
echo
echo "*** Welcome to CJU-coin Mining System ***"
echo "*** 씨쥬코인(CJU-coin) 채굴 시스템에 오신것을 환영합니다. ***"
echo
echo
echo "채굴 네트워크 설치 및 설정을 위해서는 관리자 권한이 필요합니다."
echo "사용자로부터 관리자 권한 사용을 허락받아야 합니다.."
echo
echo "파이썬 패키비 관리자 pip를 업그레이드합니다..."
echo "Start upgrade python package manager (pip)..."
echo
echo 가상환경 관리자 virtualenv 설치합니다
echo Start installing virtualenv...
pip3 install virtualenv
echo done!
echo
echo "가상환경을 생성하겠습니다..."
echo "가상환경이 설치되면 현재 위치에 venv 폴더가 생성됩니다."
echo "Set up virtual environment......"
echo "After setting up "venv" folder will be appeared in your target directory"
virtualenv venv
echo done!
echo 가상환경 설치 성공!
echo
echo
echo "설치된 가상환경을 활성화 합니다."
echo "Activate virtual environment......"
. venv/bin/activate
ls
echo
echo
echo "필요한 파이썬 패키지들을 설치하겠습니다..."
echo 'Install required python package using ...'
pip install -r ./p2p_net/requirements.txt

echo

echo "모든 설치 및 필요한 환경 설정을 마쳤습니다."
echo "터미널에서 다음 명령을 실행하여 서버를 실행해 주세요."
echo
echo ". run_blockchain.sh"
echo 

