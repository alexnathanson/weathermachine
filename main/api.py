from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import threading
from _thread import interrupt_main
import json
import webbrowser
import os
import serial.tools.list_ports

app = Flask(__name__)
CORS(app)

#these should be queues and/or events for the main thread, not globals
runSettings = {}
runIt = False

stats = {"percent":0,"elapsedTime":0,"estimateRemainingTime":0,"light":[]}
rData = {}

print("Starting Flask server...")

#wait a second for the script to start then open a browser
threading.Timer(1.25, lambda: openBrowser() ).start()

#open the interface in the default browser
def openBrowser():
      webbrowser.open_new("http://127.0.0.1:5000")

#this serves the html page
@app.route('/')
def main():
   return render_template('index.html')

#this gets the available the options for the simulation
@app.route('/options', methods=['GET'])
def options():
    if "files" in request.args.get('options'):
        print("GET FILES")
        response = os.listdir('data/cleaned')
        return response
    elif "ports" in request.args.get('options'):
        print("GET ARDUINO PORTS")
        ports = list(serial.tools.list_ports.comports())
        response = []
        for p in ports:
            #print(p.description)
            if "Arduino" in p.description:
                response.append(p.name + " - " + p.description) 
        return response

#this receives the users settings - should probably be a post...
@app.route('/weather', methods=['GET'])
def weather():
    global runIt
    global runSettings

    if "stop" in request.args:
        runIt = False
        print("STOP!")
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    else:
        runSettings = request.args.to_dict()
        runIt = True
        print(runSettings)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

#this shuts down the entire program
@app.route('/shutdown', methods=['GET'])
def shutdown():
    print("Shutdown")
    interrupt_main()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


#post live stats
@app.route('/data', methods=['POST','GET'])
def data():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            global rData
            rData = request.json
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        else:
            return 'Content-Type not supported!'
    else:
        return rData


#post live stats
@app.route('/runStats', methods=['POST','GET'])
def runStats():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            runStats = request.json

            global stats
            stats['percent'] = runStats['percent']
            stats['elapsedTime'] = runStats['elapsedTime']
            stats['estimatedRemainingTime'] = runStats['estimatedRemainingTime']
            stats['light'].append(runStats['light'])

            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        else:
            return 'Content-Type not supported!'
    else:
        return stats

if __name__ == '__main__':
 	
    app.run()
