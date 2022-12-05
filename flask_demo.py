#coding: utf-8
from flask import Flask, request
import great_contribution as gc
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/')
def hello_world():
	return gc.getWuYunLiuQi('1993-1-7')
	# return 'Hello World'

#@app.route('/date/<datetime>')
#def output(datetime):
#    return gc.getWuYunLiuQi(datetime)

@app.route('/date', methods=['get'])
def output():
        return gc.getWuYunLiuQi(request.args.get('date'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
