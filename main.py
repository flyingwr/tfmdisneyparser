from aiohttp import ClientSession, web

from typing import Optional

import api
import asyncio
import os
import stat
import subprocess

class API:
	def __init__(self):
		self.is_local: bool = "C:" in os.getcwd() or "D:" in os.getcwd()

	@staticmethod
	def authentication(auth: str) -> Optional[str]:
		if len((credentials := auth.split())) > 1:
			scheme, token = credentials
			if scheme == "Bearer":
				return token
		return None

	async def update(self):
		async with ClientSession() as session:
			async with session.get("https://pastebin.com/raw/26nGu1x2") as response:
				if response.ok:
					data = await response.json(content_type="text/plain")
					api.tokens = data.get("tfmdisney", [])
				else:
					print("Failed to read Pastebin")

	async def fetch(self):
		while True:
			await api.parser.start()
			await asyncio.sleep(8.0)

endpoint = API()
	
async def main():
	app = web.Application()
	await endpoint.update()

	app.router.add_get("/api/tfm_keys", api.TfmKeys)
	app.router.add_get("/transformice", api.Transformice)

	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, "0.0.0.0", os.getenv("PORT", 8090))
	await site.start()

	await endpoint.fetch()

if __name__ ==  "__main__":
	asyncio.run(main())
