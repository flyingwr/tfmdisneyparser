from .regex import CALL_PROPVOID, GET_LEX, GET_PROPERTY, INIT_PROPERTY, find_one

from typing import Dict, List

class Shaman(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "greaterthan" in content and "iffalse" in dumpscript[line + 1] and "getlocal_0" in dumpscript[line + 2]:
				if "getlocal r4" in dumpscript[line + 3] and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 4])) is not None:
					if (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[line + 5])) is not None:
						self["remove_shaman_obj"] = callpropvoid.group(1)
						self["shaman_obj_var"] = getproperty.group(2)
						break

		for line, content in enumerate(dumpscript):
			if "setlocal_1" in content and "getlocal_0" in dumpscript[line + 1]:
				if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 2])) is not None and "getproperty <q>[public]::length" in dumpscript[line  + 3]:
					if "convert_i" in dumpscript[line + 4] and "setlocal_2" in dumpscript[line + 5]:
						if "coerce" in dumpscript[line - 1]:
							self["shaman_obj_list"] = getproperty.group(2)
							break

		return self