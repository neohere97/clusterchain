import hashlib
from flask import Flask,request
import httplib2
import json
import threading
import socket

app=Flask(__name__)

hostname = socket.gethostname()
max_nonce = 30000000
difficulty_bits = 8
target = 2 ** (256-difficulty_bits)
found_nonce_elsewhere = False
peers = ['192.168.2.104']
transactions = {}
chain = []

@app.route('/found',methods=['POST'])
def found():
    
    global found_nonce_elsewhere
    found_nonce_elsewhere = True
    data_received = json.loads(request.data.decode('utf-8'))
    validate(data_received['nonce'], data_received['host'])
    return 'OK', 200


@app.route('/job',methods=['POST'])
def job():
    data_received = json.loads(request.data.decode('utf-8'))
    t= threading.Thread(target=find_nonce,args=(data_received,))
    t.start()     
    global transactions 
    transactions = data_received 

    return 'OK',200



def find_nonce(transactions):
    found_nonce = False
    for nonce in range(max_nonce):
        hash_result = hashlib.sha256(str.encode(str(transactions) + str(nonce))).hexdigest()
        if(found_nonce_elsewhere):
            print('***************Shit*************IIIII')
            break
        if int(hash_result, 16) < target:
            calc_hash = hash_result
            calc_nonce = nonce
            found_nonce = True
            break

    if found_nonce:
        print(calc_nonce)
        validate(calc_nonce,hostname)
        send_to_peers(calc_nonce)
        # return calc_hash, calc_nonce


def send_to_peers(nonce):
    http = httplib2.Http()
    result = {
        "nonce":nonce,
        "host":hostname
    }
    for i in peers:
        http.request('http://{}:5000/found'.format(i),'POST',json.dumps(result))
        

def validate(nonce, host):    
    hash_result = hashlib.sha256(str.encode(str(transactions) + str(nonce))).hexdigest()
    if int(hash_result, 16) < target:
        block = {
            "transactions":transactions,
            "host":host,
            "hash":hash_result
        }
        chain.append(block)
        print(chain)
    else:
        return False
    #  If all nodes return True, then add the block to the chain

if __name__ == '__main__':
    app.run(host='0.0.0.0')