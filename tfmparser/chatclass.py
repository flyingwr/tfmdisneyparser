from .regex import CALL_PROPERTY, CALL_PROPVOID, GET_LEX, GET_PROPERTY, CONSTRUCTOR, INIT_PROPERTY, PUBLIC_METHOD, SET_PROPERTY, find_one

from typing import Dict, List

class Chat(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "(<q>[public]::int, <q>[public]::int, <q>[public]::int)(3 params, 0 optional)" in content:
				for x in range(line, line + 15):
					if "applytype 1 params" in dumpscript[x]:
						if (constructor := await find_one(CONSTRUCTOR, content)) is not None:
							self["chat_class_name"] = constructor.group(1)
							
							for y in range(x, x + 100):
								if "initproperty <q>[public]::mouseEnabled" in dumpscript[y]:
									if "getlocal_0" in dumpscript[y + 1] and "getlocal_3" in dumpscript[y + 2]:
										if "initproperty" in dumpscript[y + 3]:
											if "getlocal_0" in dumpscript[y + 4]:
												if "getlex" in dumpscript[y + 5]:
													if (getproperty := await find_one(GET_PROPERTY, dumpscript[y + 6])) is not None:
														self["chat_instance"] = getproperty.group(2)
														break
							break

		if (chat_instance := self.get("chat_instance")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getproperty <q>[public]::{chat_instance}" in content:
					if "setlocal_3" in dumpscript[line - 2]:
						if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None:
							if "coerce_a" in dumpscript[line + 2]:
								if "setlocal r4" in dumpscript[line + 3]:
									self["player_list"] = getproperty.group(2)

									for x in range(line, line + 30):
										if "toLowerCase" in dumpscript[x]:
											if (_getproperty := await find_one(GET_PROPERTY, dumpscript[x - 1])) is not None:
												self["player_name"] = _getproperty.group(2)
											break
									else:
										continue
									break

			for line, content in enumerate(dumpscript):
				if f"getproperty <q>[public]::{chat_instance}" in content:
					if "returnvalue" in dumpscript[line + 3]:
						if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 2])) is not None:
							self["player"] = (await find_one(GET_PROPERTY, dumpscript[line + 1])).group(2)
							self["player_physics"] = getproperty.group(2)
							break
			
			if (player := self.get("player")) is not None:
				for line, content in enumerate(dumpscript):
					if f"getproperty <q>[public]::{player}" in content:
						if "getlocal_0" in dumpscript[line - 1] and "getlocal_0" in dumpscript[line + 2]:
							if "findpropstrict <q>[public]::int" in dumpscript[line + 5]:
								self["player_moving_right"] = (await find_one(GET_PROPERTY, dumpscript[line + 1])).group(2)
								self["player_moving_left"] = (await find_one(GET_PROPERTY, dumpscript[line + 4])).group(2)
								break

				for line, content in enumerate(dumpscript):
					if f"getproperty <q>[public]::{player}" in content and "getlocal_0" in dumpscript[line - 1]:
						if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None and "getlocal_3" in dumpscript[line + 2]:
							if "findpropstrict <q>[public]::int" in dumpscript[line + 3] and "getlocal r4" in dumpscript[line + 4]:
								self["current_frame"] = getproperty.group(2)
								break

				if (current_frame := self.get("current_frame")) is not None:
					for line, content in enumerate(dumpscript):
						if f"getproperty <q>[public]::{player}" in content and f"getproperty <q>[public]::{current_frame}" in dumpscript[line + 1]:
							if "getlocal_0" in dumpscript[line - 1] and (getproperty := await find_one(GET_PROPERTY, dumpscript[line - 2])) is not None:
								self["is_jumping"] = getproperty.group(2)
								break

				if (player_moving_right := self.get("player_moving_right")) is not None:
					for line, content in enumerate(dumpscript):
						if f"getproperty <q>[public]::{player_moving_right}" in content:
							if "callpropvoid <q>[public]::addChildAt, 2 params" in dumpscript[line - 2] and "iffalse" in dumpscript[line + 1] and "getlocal_0" in dumpscript[line + 2]:
								if "pushtrue" in dumpscript[line + 3] and (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[line + 4])) is not None:
									self["animation_course"] = callpropvoid.group(1)
									break

				for line, content in enumerate(dumpscript):
					if "convert_b" in content and "iffalse" in dumpscript[line + 1] and "getlocal r4" in dumpscript[line + 2]:
						if (setproperty := await find_one(SET_PROPERTY, dumpscript[line + 6])) is not None and "returnvoid" in dumpscript[line + 7]:
							self["is_down"] = setproperty.group(1)
							break
							
			for line, content in enumerate(dumpscript):
				if f"getproperty <q>[public]::{chat_instance}" in content:
					if "getproperty <q>[public]::stage" in dumpscript[line + 1] and "getproperty <q>[public]::focus" in dumpscript[line + 2]:
						for x in range(line, line - 10, -1):
							if "not" in dumpscript[x]:
								if ((getproperty := await find_one(GET_PROPERTY, dumpscript[x - 1])), (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[x + 1]))) != (None, None):
									self["chat_is_upper"] = getproperty.group(2)
									self["chat_shift"] = callpropvoid.group(1)
									break
						else:
							continue
						break

		if (player_name := self.get("player_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"initproperty <q>[public]::{player_name}" in content:
					if "getlocal_0" in dumpscript[line + 1]:
						if "getlocal r4" in dumpscript[line + 2]:
							if (initproperty := await find_one(INIT_PROPERTY, dumpscript[line + 3])):
								self["is_dead"] = initproperty.group(1)
								break
			
			for line, content in enumerate(dumpscript):
				if f"getproperty <q>[public]::{player_name}" in content and "getlocal_0" in dumpscript[line - 1]:
					if "iffalse" in dumpscript[line + 1] and (getlex := await find_one(GET_LEX, dumpscript[line + 2])):
						if f"getproperty <q>[public]::{chat_instance}" in dumpscript[line + 3]:
							self["ui_scoreboard_class_name"] = getlex.group(1)
							break

			if (is_dead := self.get("is_dead")) is not None:
				for line, content in enumerate(dumpscript):
					if f"initproperty <q>[public]::{is_dead}" in content:
						for x in range(line, line - 20, -1):
							if "readBoolean" in dumpscript[x]:
								if (initproperty := await find_one(INIT_PROPERTY, dumpscript[x + 1])):
									self["player_is_shaman"] = initproperty.group(1)
									break

		for line, content in enumerate(dumpscript):
			if "=(<q>[public]::int, <q>[public]::String, <q>[public]::Function = null)(3 params, 1 optional)" in content:
				if (constructor := await find_one(CONSTRUCTOR, content)) is not None:
					self["chat_class_name2"] = constructor.group(1)
					break

		for line, content in enumerate(dumpscript):
			if "getproperty <q>[public]::caretIndex" in content:
				if "getlocal_2" in dumpscript[line - 2]:
					if (getproperty := await find_one(GET_PROPERTY, dumpscript[line - 1])) is not None:
						if "convert_i" in dumpscript[line + 1]:
							self["chat_text_field"] = getproperty.group(2)
							break

		for line, content in enumerate(dumpscript):
			if "=(<q>[public]flash.events::Event)(1 params, 0 optional)" in content:
				for x in range(line, line + 10):
					if "pushbyte 0" in dumpscript[x] and "setlocal r5" in dumpscript[x + 1] and "pushnull" in dumpscript[x + 2] and "coerce" in dumpscript[x + 3]:
						self["event_chat_text"] = (await find_one(PUBLIC_METHOD, content)).group(3)
						break
		return self