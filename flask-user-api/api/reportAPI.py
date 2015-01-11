from flask import request, abort
from flask.ext.restful import Resource, reqparse
import json

class LolReportAPI(Resource):
	def post(self):
		f = open('test.txt','w')
		json.dump(request.json,f)
		f.close()
		return 'success'