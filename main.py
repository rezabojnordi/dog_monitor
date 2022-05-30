from api.master_dog_monitor import DogMonitor
#!flask/bin/python
from flask import Flask
from utils.openstack.authonticate import Authonticate
from utils.openstack.info_host import InfoHost
from flask import jsonify,json,request



app = Flask(__name__)


##*****************************************swagger*****************************************

from flasgger import Swagger
from flasgger.utils import swag_from
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs" : [
        {
            "endpoint" : "apispec_1",
            "route" : "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag:True,  
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger = Swagger(app, config= swagger_config)
##*******************************************************************************************************

'''

This function get Metrics from prometheus to customer or client
'''

@app.route("/get_metrics", methods=['GET'])
@swag_from("doc/api_doc.yml")
def get_metrics():
    if request.method == 'GET':
        res = request.get_json()["server"]
        date = request.get_json()["date"]
        instance_id = res["instance_id"]

        print("##############",date["start_date"])

        #Authonticate()
        info_host = InfoHost(instance_id)
        details = info_host.detailHost()
        if(details):
            dog_monitor = DogMonitor(details["instance_name"],details["compute"],date["start_date"],date["start_time"],date["end_date"],date["end_time"])
            r = dog_monitor.request_metrics()
            return success_result("success",r)
        else:
            return error_result("error","The instance is not found"),404
    else:
        pass






# create error result structure
def error_result(status,message):
    results={}
    results["error"]={}
    results["error"]["status"]=status
    results["error"]['message']=message
    return jsonify(results)

# create success result structure
def success_result(status,message,types=""):
    results={}
    results["data"]={}
    results["data"]["status"]=status
    if types !="":
        results["data"]["type"]=types
    results["data"]['message']=message
    return jsonify(results)


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True,port=8686)

