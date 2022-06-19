from .regex import GET_LEX, GET_PROPERTY, SET_PROPERTY, find_one

from typing import Dict, List

class Timer(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "callpropvoid <q>[public]::start, 0 params" in content:
				if "getproperty" in dumpscript[line - 1] and "findpropstrict <q>[public]::Date" in dumpscript[line + 2]:
					self["check_timer"] = (await find_one(GET_PROPERTY, dumpscript[line - 1])).group(2)

					for x in range(line, line + 10):
						if "subtract" in dumpscript[x] and (setproperty := await find_one(SET_PROPERTY, dumpscript[x + 1])) is not None:
							self["check_timestamp"] = setproperty.group(1)
							break
					break

		for line, content in enumerate(dumpscript):
			if "dup" in content and "iftrue" in dumpscript[line + 1] and "pop" in dumpscript[line + 2]:
				if (getlex := await find_one(GET_LEX, dumpscript[line + 3])) is not None and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 4])) is not None:
					if "convert_b" in dumpscript[line + 5] and "iffalse" in dumpscript[line + 6] and "returnvoid" in dumpscript[line + 7]:
						self["timer_class_name"] = getlex.group(1)
						self["timer_prop"] = getproperty.group(2)
						break

		if (timer_class_name := self.get("timer_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{timer_class_name}" in content and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None:
					if "iffalse" in dumpscript[line + 2] and "findpropstrict <q>[public]::Error" in dumpscript[line + 3]:
						self["timer_instance"] = getproperty.group(2)
						break

		return self