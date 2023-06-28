echo
echo 가상환경을 활성화 합니다.
. venv/bin/activate
echo
sleep 2s
echo 웹서버를 시작합니다...
echo
export FLASK_APP=server
export FLASK_DEBUG=True
flask run -h 0.0.0.0 -p 7000 &


echo 블록체인 P2P 네트워크를 시작합니다.
python ./p2p_net/run_p2p.py -p 22901 &
echo
sleep 5s
echo 사설망을 사용하고 있는지 확인합니다.
echo
PUBLIC_IP=`curl https://checkip.amazonaws.com`
PRIVATE_IP=`hostname -I`
echo
echo "사용자님의 공인(public ip) : $PUBLIC_IP"
echo "사용자님의 사설(private ip): $PRIVATE_IP"
echo
sleep 3s
if [[ "$PUBLIC_IP" != "$PRIVATE_IP" ]]
then
    echo
    echo "사설망을 사용하고 있는 것 같습니다."
    echo "다음 주소로 접속해 주세요"
    echo
    echo "http://$PUBLIC_IP:7000"
    echo
else
    echo 
    echo "다음 주소로 접속해 주세요"
    echo
    echo "http://$PUBLIC_IP:7000"
    echo
fi