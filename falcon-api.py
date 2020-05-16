import json, falcon

class ObjectRequestClass():
	"""docstring for ClassName"""
	def on_get(self, req, resp):
		contents = {
		"greet":"hi",
		"hello":"welcome"
		"bye":"leaving"
		}

		resp.body = json.dumps(contents)

api = falcon.API()
api.add_route('/test', ObjectRequestClass())