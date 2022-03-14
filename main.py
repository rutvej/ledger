from builtins import print
from flask import Flask,Request,json, request,jsonify
import hashlib


app = Flask("__main__")

@app.route("/")
def home():
    return "hello world!" 

@app.route("/legder")
def ledger():
    ledgerdata = open("ledger.json","r+")
    ledgerdata = json.load(ledgerdata)
    return jsonify((ledgerdata)) if ledgerdata else "no ledger"

@app.route("/mine",methods=["POST"])
def mining():
    try:
        data = request.json
        jsonfile = open("ledger.json","r+")
        ledgerdata = json.load(jsonfile)
        prevhash = ledgerdata[-1]["hash"]
        id = ledgerdata[-1]["id"]+1
        data["prevhash"] = prevhash
        data["id"] = id
        hashdata = json.dumps(data)
        hash = hashlib.sha256(hashdata.encode()).hexdigest()
        data["hash"] = hash
        ledgerdata.append(data)
        print(ledgerdata)
        jsonfile.seek(0)
        jsonfile.truncate()
        json.dump(ledgerdata,jsonfile)
        return "success"
    except Exception as e :
        print(e)
        return str("")

@app.route("/verify")
def verify():
    ledfile = request.files["file"].stream.read().decode()
    myled = open("ledger.json","r").read()
    # print(ledfile.decode(),"dadsad\n",myled,ledfile==myled)
    print(ledfile==myled)

    jsonfile = json.loads(ledfile)
    for i in jsonfile:
        hash = i.pop("hash")
        data = json.dumps(i)
        cal = hashlib.sha256(data.encode()).hexdigest()
        print(cal,hash)
        if hash != cal:
            return jsonify({"Error":"fraud ledger","fraud person":i["data"]["invester_name"]})
        

    return {}



    





    


# if __name__ == "__main__":
#     app.run(port=4040,debug=True)