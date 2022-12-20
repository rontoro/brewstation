import time
import re
import sys
from flask import Flask, render_template
import threading
from turbo_flask import Turbo
import os

app = Flask(__name__)
turbo = Turbo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.context_processor
def inject_load():
    if sys.platform.startswith('linux'):
        with open('/proc/loadavg', 'rt') as f:
#            load = os.popen('vcgencmd measure_temp').readline()
            load = os.popen('vcgencmd measure_temp').readline().split("=",1)[1].split("'",1)[0]
    return {'load1': load}

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))