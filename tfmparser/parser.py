from .bypasscode import BypassCode
from .chatcontainer import ChatContainer
from .chatclass import Chat
from .chatmessage import ChatMessage
from .checker import Checker
from .domainmanager import DomainManager
from .frameloop import FrameLoop
from .mapclass import Map
from .move import Move
from .player import Player
from .shaman import Shaman
from .socket import Socket
from .swf import Swf
from .timer import Timer
from .ui import UI

from typing import Dict, List

import aiohttp
import asyncio
import datetime
import subprocess
import sys

tfm_swf_url = "http://transformice.com/Transformice.swf"

class Parser:
	def __init__(self, is_local: bool = False):
		self._session = None

		self.dumpscript: List = []
		self.fetched: Dict = {}

		self.is_local: bool = is_local

		self.last_swf_len: int = 0

		self.downloaded_swf: str = "Transformice.swf"
		self.output_swf: str = "tfm.swf"

	async def run_console(self, target: str):
		self.dumpscript *= 0

		_exec = "swfdump" if sys.platform == "linux" else "./tools/swfdump"
		console = subprocess.Popen([_exec, "-a", target], shell=False,
			stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		self.dumpscript = [line.decode().rstrip() for line in console.stdout]

	async def download_swf(self):
		if self._session is None:
			self._session = aiohttp.ClientSession()

		update = False

		try:
			url = f"{tfm_swf_url}?d={datetime.datetime.now().timestamp()}"

			async with self._session.head(url) as response:
				length = response.content_length
				if length != self.last_swf_len:
					async with self._session.get(url) as response:
						if response.ok:
							print("Downloading Transformice.swf")

							with open(self.downloaded_swf, "w+b") as f:
								f.write(await response.read())
								
							self.last_swf_len = length

							update = True
						else:
							self.last_swf_len = 0
		except Exception as e:
			print(f"Failed to download Transformice SWF: {e}")

		return update

	async def start(self):
		if await self.download_swf():
			try:
				await self.run_console(self.downloaded_swf)
				swf = Swf(self.downloaded_swf, self.output_swf)
				await swf.parse_content(self.dumpscript)
				await self.run_console(self.output_swf)
			except Exception as e:
				print(f"Failed to parse Transformice SWF: {e}")
			else:
				self.bypass = BypassCode()
				self.chat = Chat()
				self.chat_container  = ChatContainer()
				self.chat_message = ChatMessage()
				self.checker = Checker()
				self.domain_manager = DomainManager()
				self.frame_loop = FrameLoop()
				self.map = Map()
				self.move = Move()
				self.player = Player()
				self.shaman = Shaman()
				self.socket = Socket()
				self.timer = Timer()
				self.ui = UI()

				names = (
					"chat", "chat_container", "chat_message", "checker", "domain_manager",
					"frame_loop", "map", "move", "player", "shaman", "socket", "timer", "ui",
					"bypass"
				)
				for result in await asyncio.gather(*[(getattr(self, name)).fetch(self.dumpscript) for name in names]):
					self.fetched.update(result)
				
				for key, value in self.fetched.items():
					self.fetched[key] = value.replace("\\", "")

				print("Parser data has been updated")
