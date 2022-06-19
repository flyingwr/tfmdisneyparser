from .regex import CALL_PROPVOID, GET_LEX, GET_PROPERTY, INIT_PROPERTY, find_one

from typing import Dict, List

class Move(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "not" in content and "dup" in dumpscript[line + 1] and "iffalse" in dumpscript[line + 2]:
				if "pop" in dumpscript[line + 3] and (getlex := await find_one(GET_LEX, dumpscript[line + 4])) is not None:
					if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 5])) is not None:
						if "convert_b" in dumpscript[line + 6] and "iffalse" in dumpscript[line + 7]:
							if "getlocal_3" in dumpscript[line - 2]:
								self["move_class_name"] = getlex.group(1)
								self["move_free"] = getproperty.group(2)
								break
		return self