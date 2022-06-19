from .regex import GET_LEX, GET_PROPERTY, INIT_PROPERTY, find_one

from typing import Dict, List

class Map(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "getproperty <q>[public]::y" in content and "setproperty <q>[public]::y" in dumpscript[line + 1]:
				if "getlocal_2" in dumpscript[line - 5]:
					if "getlex" in dumpscript[line - 4]:
						if "getproperty" in dumpscript[line - 3]:
							if "getproperty" in dumpscript[line - 2]:
								if "getproperty" in dumpscript[line - 1]:
									self["map_class_name"] = (await find_one(GET_LEX, dumpscript[line - 4])).group(1)
									self["map_instance"] = (await find_one(GET_PROPERTY, dumpscript[line - 3])).group(2)
									self["obj_container"] = (await find_one(GET_PROPERTY, dumpscript[line - 2])).group(2)
									
									if "getlocal_2" in dumpscript[line + 2]:
										if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 3])) is not None:
											self["player_clip"] = getproperty.group(2)
											break
		
		if (map_class_name := self.get("map_class_name")) is not None and (map_instance := self.get("map_instance")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{map_class_name}" in content and f"getproperty <q>[public]::{map_instance}" in dumpscript[line + 1] and "setproperty <q>[public]::x" in dumpscript[line - 1]:
					if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 2])) is not None and "findpropstrict <q>[public]::int" in dumpscript[line + 3]:
						self["clip_fromage"] = getproperty.group(2)
						break

		if (obj_container := self.get("obj_container")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getproperty <q>[public]::{obj_container}" in content and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None:
					if "coerce <q>[public]__AS3__.vec::Vector" in dumpscript[line + 2] and "convert_i" in dumpscript[line + 6]:
						if "setlocal_" in dumpscript[line + 7]:
							self["hole_list"] = getproperty.group(2)
							break

		for line, content in enumerate(dumpscript):
			if "getproperty <q>[public]::_I" in content and "dup" in dumpscript[line + 1] and "setlocal_1" in dumpscript[line + 2]:
				if (initproperty := await find_one(INIT_PROPERTY, dumpscript[line + 3])) is not None:
					self["tfm_obj_container"] = initproperty.group(1)
					break

		return self