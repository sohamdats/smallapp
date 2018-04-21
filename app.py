from flask import Flask,request,render_template,redirect,url_for
import redis
import datetime
from db import DB
import json

app = Flask(__name__)
d = DB(host='redis')


@app.route('/')
def index():
    
    e_data = json.load(open('elements.json'),strict=False)
    for element,ele_p in e_data.items():
        d.store_element(element)
        d.store_eprop(element,'Role',ele_p['Role'])
        d.store_eprop(element,'IP',ele_p['IP'])
        d.store_eprop(element,'IP Address',ele_p['IP Address'])
        d.store_eprop(element,'Credentials',ele_p['Credentials'])
        d.store_eprop(element,'Device',ele_p['Device'])
    
    return render_template('index.html',elements=d.get_element_states())

@app.route('/<name>',methods=['GET'])
def search(name):
    return 'Not Found' if d.is_reserved(name) == False else d.is_reserved(name)

@app.route('/reserve',methods=['POST'])
def reserve():
    if request.method == "POST":
        user=request.values.get('user')
        minutes=request.values.get('minutes')
        element=request.values.get('element')
        d.store(element,user,minutes)
        #print(element,user,minutes)
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
