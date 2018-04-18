from flask import Flask,request,render_template,redirect,url_for
import redis
import datetime
from db import DB

app = Flask(__name__)
r = redis.Redis(host='localhost',port=6379)
d = DB()

@app.route('/')
def index():
    devices= ['xTR-1','MS-BR1','WLC-1','WLC-2','AP-1','AP-2','APIC-EM','ME']
    d.store_devices(devices)
    return render_template('index.html',devices=d.get_device_states())

@app.route('/<name>',methods=['GET'])
def search(name):
    return 'Not Found' if d.is_reserved(name) == False else 'Found'

@app.route('/reserve',methods=['POST'])
def reserve():
    if request.method == "POST":
        user=request.values.get('user')
        minutes=request.values.get('minutes')
        device=request.values.get('device')
        time = datetime.datetime.now().strftime("%d/%m/%y at %H:%M:%S")
        d.store(device,user,minutes,time)
    return redirect(url_for('index'))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
         filename = values.get('filename', None)
         if filename:
              file_path = os.path.join(app.root_path,endpoint, filename)
              values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8800)
