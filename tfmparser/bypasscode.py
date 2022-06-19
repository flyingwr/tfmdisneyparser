from .regex import INIT_PROPERTY, find_one

from typing import Dict, List

class BypassCode(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "getproperty <q>[public]::loaderURL" in content and (initproperty := await find_one(INIT_PROPERTY, dumpscript[line + 1])) is not None:
				self["loader_url"] = initproperty.group(1)
				break

		for line, content in enumerate(dumpscript):
			if "getlocal_0" in content:
				if "getlex <q>[public]::stage" in dumpscript[line + 1] and "getproperty <q>[public]::loaderInfo" in dumpscript[line + 2] and "getproperty <q>[public]::length" in dumpscript[line + 4]:
					if (initproperty := await find_one(INIT_PROPERTY, dumpscript[line + 5])) is not None:
						self["bypass_code"] = initproperty.group(1)
						break
		return self