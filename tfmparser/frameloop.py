from .regex import CALL_PROPVOID, GET_LEX, GET_PROPERTY, SET_PROPERTY, find_one

from typing import Dict, List

class FrameLoop(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "inclocal_i r2" in content and "getlocal_2" in dumpscript[line + 1]:
				if "getlex" in dumpscript[line + 2] and "getproperty" in dumpscript[line + 3]:
					if "getproperty <q>[public]::length" in dumpscript[line + 5]:
						if "iflt" in dumpscript[line + 6] and (getlex := await find_one(GET_LEX, dumpscript[line + 7])) is not None:
							self["frame_loop_class_name"] = getlex.group(1)
							break

		if (frame_loop_class_name := self.get("frame_loop_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{frame_loop_class_name}" in content:
					if "getlocal r6" in dumpscript[line - 1] and "pop" in dumpscript[line - 2] and "iftrue" in dumpscript[line - 3]:
						if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None:
							self["victory_time"] = getproperty.group(2)
							break

			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{frame_loop_class_name}" in content and "iffalse" in dumpscript[line - 1] and "greaterthan" in dumpscript[line - 2]:
					for x in range(line, line + 10):
						if (setproperty := await find_one(SET_PROPERTY, dumpscript[x])) is not None:
							for y in range(x, x + 5):
								if "::msgAntitriche" in dumpscript[y]:
									self["new_check"] = setproperty.group(1)
									break
							else:
								continue
							break
					else:
						continue
					break

		return self