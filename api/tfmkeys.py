from aiohttp import web
from main import endpoint

import api

class TfmKeys(web.View):
	async def get(self):
		response = {}
		status = 401

		if (auth := self.request.headers.get("Authorization")) is not None:
			if (token := endpoint.authentication(auth)) is not None:
				if token in api.tokens:
					response.update(api.parser.fetched)
					status = 200
				else:
					response["error"] = "unauthorized token"
			else:
				response["error"] = "invalid credentials"
				status = 400
		else:
			response["error"] = "invalid credentials"
			status = 400

		return web.json_response(response, status=status)