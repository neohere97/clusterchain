from flask import Flask, request
import httplib2
import threading
import json
import docker

app=Flask(__name__)
chain = []
transactions = []
queue = []
txn = {}
lock = threading.Lock()

@app.route('/txion', methods=['POST'])
def txion():
    global txn
    trans = request.data.decode('utf-8')
    if(len(txn) == 5):
        queue.append(txn)
        txn = {}
        monitorJobQueue()
    txn[trans] = "Success"
    print(txn)
    return "OK", 200

def monitorJobQueue():
    http = httplib2.Http()       
    global queue
    if(len(queue)>0):
        print(queue[0])
        http.request(f'http://192.168.2.104:5000/job','POST',json.dumps(queue[0]))
        http.request(f'http://192.168.2.103:5000/job','POST',json.dumps(queue[0]))
        
        del queue[0]
    # lock_a.release()
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')
   