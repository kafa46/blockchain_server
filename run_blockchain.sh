export FLASK_APP=server
export FLASK_DEBUG=True

python ./p2p_net/run_p2p.py &
flask run -h 0.0.0.0 -p 7000