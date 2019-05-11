from flask import Flask,request  
import random
import threading
import json
import time
import httplib2

app=Flask(__name__)
first_names = ['Carletta', 'Rachelle', 'Renata', 'Ann', 'Karlyn', 'Nydia', 'Keva', 'Willis', 'Allan', 'Akiko', 'Suellen', 'Nickole', 'Ashanti', 'Alisha', 'Ami', 'Bea', 'Jeannine', 'Krystina', 'Carita', 'Lina', 'Rosario', 'Bobbye', 'Senaida', 'Georgann', 'Georgiann', 'Eula', 'Edward', 'Trevor', 'Yetta', 'Carri', 'Hoyt', 'Linh', 'Kristian', 'Carlie', 'Raina', 'Enoch', 'Lindsy', 'Jacqualine', 'Edison', 'Dalene', 'Eva', 'Latosha', 'Wei', 'Leanna', 'Elinore', 'Frederic', 'Pattie', 'Flavia', 'Lynetta', 'Kaylene']
last_names = ['Wm', 'Roscoe', 'Chauncey', 'Graig', 'Malcolm', 'Morgan', 'Dennis', 'Mary', 'Ezekiel', 'Harold', 'Giuseppe', 'Darnell', 'Brant', 'Alejandro', 'Mark', 'Lemuel', 'Herschel', 'Granville', 'Noble', 'Cesar', 'Dewayne', 'Mike', 'Efrain', 'Jeramy', 'Merle', 'Hassan', 'Roberto', 'Jules', 'Rashad', 'Basil', 'Hugh', 'Lane', 'Quentin', 'Hollis', 'Tomas', 'Ferdinand', 'Wendell', 'Roy', 'Stuart', 'Andre', 'Jame', 'Rhett', 'Kelly', 'Darwin', 'Diego', 'Milton', 'Lynn', 'Markus', 'Fermin', 'Rich']
alphabets = [' A ', ' B ' , ' C ', ' D ', ' E ' , ' F ', ' G ', ' H ', ' I ' , ' J ', ' K ', ' L ', ' M ', ' N ', ' O ', ' P ', ' Q ', ' R ', ' S ', ' T ', ' U ', ' V ', ' W ', ' X ', ' Y ', ' Z ']

state = False
no_of_transactions_permin = 2

@app.route('/setState',methods =["POST"])
def setState():
    global state
    state_s = json.loads(request.data.decode('utf-8'))['setState']
    if(state_s == "Start"):
        state = True
        t= threading.Thread(target=generate_trans)
        t.start() 
        print("Started")
    elif(state_s == "Stop"):
        state = False


    return "OK", 200
   
        

@app.route('/numTrans',methods =["POST"])
def numTrans():
    global no_of_transactions_permin
    no_of_transactions_permin = json.loads(request.data.decode('utf-8'))['numTrans']
    print("no of transactions set to {}".format(no_of_transactions_permin))

    return "OK",200

def generate_trans():
    global state
    while True:
        if(not state):
            break
        transaction = "{} paid {} {} PIKA coins".format(random.choice(first_names) + random.choice(alphabets) + random.choice(last_names),random.choice(first_names) + random.choice(alphabets) + random.choice(last_names),random.randint(1,500))
        
        send_transaction(transaction)        
        time.sleep(60/no_of_transactions_permin)


def send_transaction(transaction):
    http = httplib2.Http()
    print(transaction)
    http.request('http://0.0.0.0:5000/txion','POST',transaction)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5003')
     
    