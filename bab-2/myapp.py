#import flask
from flask import Flask

# main app
app = Flask(__name__)

# set route untuk /
@app.route('/')
def index():
    # print text
    return 'Hello World!'

# debut, untuk update server dev otomatis
if __name__ == '__main__':
    app.run(debug=True)
    
