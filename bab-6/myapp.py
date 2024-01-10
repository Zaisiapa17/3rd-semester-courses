#import flask
from flask import Flask, render_template

# main app
app = Flask(__name__)

# set route untuk /
@app.route('/')
def index():
    # print text
    return render_template('index.html')

# debut, untuk update server dev otomatis
if __name__ == '__main__':
    app.run(debug=True)

