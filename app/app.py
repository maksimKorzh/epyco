from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from io import StringIO 
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
    with Capturing() as output:
        try:
            exec(request.form.get('source'), globals())
            
            with open('.codelog', 'a') as codelog:
                codelog.write(request.form.get('source'))
                
        except Exception as e:
            return jsonify({'output': e.args[0]})
    
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
