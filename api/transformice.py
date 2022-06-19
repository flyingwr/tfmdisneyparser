from aiohttp import web

import api

class Transformice(web.View):
	async def get(self):
		if self.request.query.get("swf") is not None:
			return web.FileResponse("./tfm.swf")
		raise web.HTTPNoContent()