from .regex import CALL_PROPERTY, FINAL_METHOD, GET_LEX, find_one

from typing import Dict, List

class DomainManager(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "getlocal r5" in content and "pushtrue" in dumpscript[line + 1] and (callproperty := await find_one(CALL_PROPERTY, dumpscript[line + 2])) is not None and dumpscript[line + 2].endswith(", 2 params"):
				if "coerce <q>[public]flash.display::Sprite" in dumpscript[line + 3]:
					if (getlex := await find_one(GET_LEX, dumpscript[line - 1])) is not None:
						self["get_definition"] = callproperty.group(1)
						self["domain_manager_class_name"] = getlex.group(1)
						break

		for line, content in enumerate(dumpscript):
			if "add" in content and (callproperty := await find_one(CALL_PROPERTY, dumpscript[line + 1])) is not None:
				if "coerce <q>[public]flash.display::Bitmap" in dumpscript[line + 2] and "jump" in dumpscript[line + 3] and "pushnull" in dumpscript[line + 4]:
					self["load_img"] = callproperty.group(1)
					break

		return self