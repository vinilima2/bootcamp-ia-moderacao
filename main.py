from flask import Flask, render_template, request  

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')
   
if __name__ == "__main__": 
    app.run(host = "0.0.0.0", port = 8080)

@app.route('/analyse', methods = ["POST"]) 
def analyse():
    id_msg, msg = request.get_json().values()
    return id_msg + ' ' + msg
