from flask import Flask,render_template
import json
#d = json.load(open('elements.json'),strict=False)
'''
app = Flask(__file__)

@app.route('/')
def test():
    d = json.loads(open('elements.json'),strict=False)
    return render_template('test.html',e = d)

if __name__ =='__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
'''

d = json.load(open('elements.json'),strict=False)
print(d['MS - BR1']['IP Address'])


    
    

    

