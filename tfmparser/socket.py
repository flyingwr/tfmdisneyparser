from .regex import GET_LEX, GET_PROPERTY, FIND_PROPERTY, INIT_PROPERTY, PUBLIC_METHOD, find_one

from typing import Dict, List

class Socket(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::String = null, <q>[public]::Boolean = false)(2 params, 2 optional)"):
				for x in range(line, line + 10):
					if "getproperty <q>[public]::connected" in dumpscript[x] and (getproperty := await find_one(GET_PROPERTY, dumpscript[x - 1])) is not None:
						self["socket_name"] = getproperty.group(2)
					
						i = 0
						for y in range(x, x + 50):
							if "callpropvoid <q>[public]::removeEventListener, 2 params" in dumpscript[y] and (getproperty := await find_one(GET_PROPERTY, dumpscript[y - 1])) is not None:
								self["event_bulle_socket_close" if not i else "event_main_socket_close"] = getproperty.group(2)

								if i == 1:
									break
								i += 1
						break
				else:
					continue
				break

		if (socket_name := self.get("socket_name")) is not None:
			for line, content in enumerate(dumpscript):
				if "getproperty <q>[public]::bytesAvailable" in content and f"getproperty <q>[public]::{socket_name}" in dumpscript[line - 1]:
					for x in range(line, line + 15):
						if "increment_i" in dumpscript[x] and (getproperty := await find_one(GET_PROPERTY, dumpscript[x - 1])) is not None:
							self["data_id"] = getproperty.group(2)
							break
					else:
						continue
					break

			for line, content in enumerate(dumpscript):
				if "getproperty <q>[public]::bytesAvailable" in content and f"getproperty <q>[public]::{socket_name}" in dumpscript[line - 1]:
					if "getlocal_0" in dumpscript[line - 2] and "label" in dumpscript[line - 3]:
						if "jump" in dumpscript[line - 4] and "iftrue" in dumpscript[line - 5]:
							if (getproperty := await find_one(GET_PROPERTY, dumpscript[line - 6])) is not None:
								self["read_data"] = getproperty.group(2)
								break

		for line, content in enumerate(dumpscript):
			if "getproperty <q>[public]::errorID" in content:
				for x in range(line, line + 8):
					if "callpropvoid" in dumpscript[x] and (getlex := await find_one(GET_LEX, dumpscript[x - 1])) is not None:
						self["packet_handler_class_name"] = getlex.group(1)
						break
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::int, <q>[public]::String, <q>[public]::String = , <q>[public]::Boolean = false, <q>[public]::Boolean = false, <q>[public]::Array = null)(6 params, 4 optional)"):
				self["packet_handler"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]flash.events::ProgressEvent = null, <q>[public]::Boolean = false)(2 params, 2 optional)"):
				self["event_socket_data"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if "multiply" in content and "lshift" in dumpscript[line + 1] and "bitor" in dumpscript[line + 2]:
				if (initproperty := await find_one(INIT_PROPERTY, dumpscript[line + 3])) is not None:
					if "getlocal_0" in dumpscript[line + 4] and "dup" in dumpscript[line + 5] and "setlocal r4" in dumpscript[line + 6]:
						if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 7])):
							self["data_len"] = initproperty.group(1)
							self["data_offset"] = getproperty.group(2)
							break

		for line, content in enumerate(dumpscript):
			if content.endswith("::ecriture, 1 params") and (findproperty := await find_one(FIND_PROPERTY, dumpscript[line + 1])) is not None:
				self["cipher"] = findproperty.group(1)
				break

		return self