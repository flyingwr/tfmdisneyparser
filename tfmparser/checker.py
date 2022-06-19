from .regex import CALL_PROPVOID, GET_LEX, GET_PROPERTY, FIND_PROPSTRICT, PUBLIC_METHOD, SET_PROPERTY, find_one

from typing import Dict, List

class Checker(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if content.endswith("=()(0 params, 0 optional)"):
				if "pushnull" in dumpscript[line + 5] and "coerce <q>" in dumpscript[line + 6]:
					if "setlocal_1" in dumpscript[line + 7] and "getlex" in dumpscript[line + 8]:
						if "getproperty" in dumpscript[line + 9] and "iffalse" in dumpscript[line + 10]:
							if "findpropstrict" in dumpscript[line + 11] and "getlex" in dumpscript[line + 12]:
								self["checker_class_name"] = (await find_one(GET_LEX, dumpscript[line + 8])).group(1)
								self["check_id"] = (await find_one(GET_PROPERTY, dumpscript[line + 9])).group(2)

								for x in range(line + 12, line + 25):
									if "coerce" in dumpscript[x] and (getlex := await find_one(GET_LEX, dumpscript[x + 2])) is not None:
										if (getproperty := await find_one(GET_PROPERTY, dumpscript[x + 3])) is not None:
											if (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[x + 5])) is not None:
												if (_getproperty := await find_one(GET_PROPERTY, dumpscript[x + 7])) is not None:
													self["socket_class_name"] = getlex.group(1)
													self["bulle_socket_instance"] = getproperty.group(2)
													self["main_socket_instance"] = _getproperty.group(2)
													self["data_sender"] = callpropvoid.group(1)
													break
								break

		if (checker_class_name := self.get("checker_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{checker_class_name}" in content and "convert_i" in dumpscript[line - 2] and "multiply" in dumpscript[line - 3]:
					if "iffalse" in dumpscript[line + 2] and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 4])):
						self["check_pos"] = getproperty.group(2)
						break

		if (socket_class_name := self.get("socket_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{socket_class_name}" in content and "getproperty" in dumpscript[line + 1]:
					if (findpropstrict := await find_one(FIND_PROPSTRICT, dumpscript[line + 2])) and "getlocal_1" in dumpscript[line + 3]:
						if "constructprop" in dumpscript[line + 4] and "callpropvoid" in dumpscript[line + 5]:
							if "iffalse" in dumpscript[line - 1] and "getlocal_2" in dumpscript[line - 2]:
								self["command_packet_class_name"] = findpropstrict.group(1)
								break

			if (bulle_socket_instance := self.get("bulle_socket_instance")) is not None:
				for line, content in enumerate(dumpscript):
					if content.endswith(", <q>[public]::int)(2 params, 0 optional)") and "getlocal_1" in dumpscript[line + 5]:
						for x in range(line, line + 10):
							if f"getlex <q>[public]::{socket_class_name}" in dumpscript[x] and f"getproperty <q>[public]::{bulle_socket_instance}" in dumpscript[x + 1]:
								if (findpropstrict := await find_one(FIND_PROPSTRICT, dumpscript[x + 2])) is not None:
									self["crouch_packet_class_name"] = findpropstrict.group(1)
									break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::int, <q>[public]::int, <q>[public]::int, <q>[public]::int = 0, <q>[public]::Number = 0, <q>[public]::Number = 0, <q>[public]::Boolean = true)(7 params, 4 optional)"):
				self["create_function"] = (await find_one(PUBLIC_METHOD, content)).group(3)

				if (getlex := await find_one(GET_LEX, dumpscript[line + 5])) is not None:
					self["create_class_name"] = getlex.group(1)
					break
		
		return self