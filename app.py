from flask import Flask
from time import sleep
import time
app = Flask(__name__)

@app.route("/")
def index():
    print('RUNNING')
    return "ALPHA\t"+str(time.time())+"\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
