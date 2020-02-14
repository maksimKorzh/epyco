from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from io import StringIO
from subprocess import Popen, PIPE
import sys


###################################################################
#
# APP
#
###################################################################

app = Flask(__name__)


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
