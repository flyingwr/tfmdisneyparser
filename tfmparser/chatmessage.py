from .regex import CALL_PROPVOID, find_one

from typing import Dict, List

class ChatMessage(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if 'pushstring "Navigateur : "' in content:
				if (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[line - 2])) is not None:
					self["chat_message"] = callpropvoid.group(1)
					break
				
		for line, content in enumerate(dumpscript):
			if "add" in content:
				if "getlocal r93" in dumpscript[line + 1]:
					if "callpropvoid" in dumpscript[line + 2]:
						if "jump" in dumpscript[line + 3]:
							self["chat_message2"] = (await find_one(CALL_PROPVOID, dumpscript[line + 2])).group(1)
							break

		return self