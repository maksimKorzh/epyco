from subprocess import Popen, PIPE
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import g
from io import StringIO
import threading
import sys


###################################################################
#
# APP
#
###################################################################

app = Flask(__name__)

proc = None
process = None


###################################################################
#
# Routes
#
###################################################################

@app.route('/')
def root():
    return render_template('code.html')

@app.route('/execute', methods=['POST'])
def execute():
    # write code to file
    with open('run.py', 'w') as code:
        code.write(request.form.get('source'))
    
    with Capturing() as output:
        execute = Popen('python3 run.py', shell=True, stdout=PIPE, stderr=PIPE)
        out = execute.stdout.read().decode('utf-8')
        err = execute.stderr.read().decode('utf-8')
        print(out, err)
    
    return jsonify({'output': '\n'.join(output)})

@app.route('/background', methods=['POST'])
def backgroud():
    global process
    
    # write code to file
    with open('background.py', 'w') as code:
        code.write(request.form.get('source'))
    
    # clear background output
    with open('background.txt', 'w') as out:
        out.write('')
    
    # clear background log
    with open('background.log', 'w') as out:
        out.write('')
        
    def run():
        global proc

        proc = Popen('exec python3 background.py', shell=True, stdout=PIPE, stderr=PIPE)
        out = proc.stdout.read().decode('utf-8')
        err = proc.stderr.read().decode('utf-8')
        
        with open('background.txt', 'a') as output:
            output.write(out + err)
    
    process = threading.Timer(0, run)
    process.start()
    
    return '''Executing code in background thread...

# paste this code before spider class definition to enable logging
import logging
logging.basicConfig(filename='background.log',level=logging.DEBUG)

# usage
def parse(self, response):
    self.log(response.text) # will log response.text to background.log

# track your code's output in new EPYCO tab:
from hack import *
cat('background.log')
'''  

@app.route('/kill', methods=['POST'])
def kill():
    if proc.poll() is None:
        proc.kill()
        process.cancel()
        
        # clear user file output
        with open('background.txt', 'w') as output:
            output.write('process was killed!\n')
        
        # clear user log file
        with open('background.log', 'w') as output:
            output.write('process was killed!\n')

        return 'background process %s was successfully killed!' % str(proc)
    else:
        return 'no process running!'
    

###################################################################
#
# Misc
#
###################################################################

# Capture console output
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


###################################################################
#
# Driver
#
###################################################################

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
