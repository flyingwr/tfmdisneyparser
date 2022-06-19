from .regex import GET_LEX, GET_PROPERTY, PUBLIC_SLOT, find_one

from typing import Dict, List

class ChatContainer(dict):
	async def fetch(self, dumpscript) -> Dict:
		for line, content in enumerate(dumpscript):
			if "getlocal_0" in content and "getproperty <q>[public]::x" in dumpscript[line + 2] and "setproperty <q>[public]::x" in dumpscript[line + 3]:
				if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None and "returnvoid" in dumpscript[line + 4]:
					self["chat_container"] = getproperty.group(2)
					break

		for line, content in enumerate(dumpscript):
			if "callproperty <q>[public]::getChildAt, 1 params" in content and (getlex := await find_one(GET_LEX, dumpscript[line + 1])) is not None:
				if "istypelate" in dumpscript[line + 2] and "not" in dumpscript[line + 3]:
					self["ui_input_class_name"] = getlex.group(1)
					break
			
		return self