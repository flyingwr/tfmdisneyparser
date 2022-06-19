from .regex import CALL_PROPERTY, CALL_PROPVOID, CONSTRUCTOR_2, GET_LEX, GET_PROPERTY, INIT_PROPERTY, PUBLIC_METHOD, SET_PROPERTY, find_one

from typing import Dict, List

class Player(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "getscopeobject 1" in content and "pushnull" in dumpscript[line + 1]:
				if "coerce <q>[public]flash.display::MovieClip" in dumpscript[line + 2] and "setslot 2" in dumpscript[line + 3]:
					if "findpropstrict <q>[public]::addChildAt" in dumpscript[line + 4] and "getlocal_0" in dumpscript[line + 5]:
						if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 6])) is not None:
							self["player_bitmap"] = getproperty.group(2)
							break

		if (player_bitmap := self.get("player_bitmap")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getproperty <q>[public]::{player_bitmap}" in content and "getlocal r4" in dumpscript[line - 1]:
					if (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[line - 2])) is not None and "pushtrue" in dumpscript[line - 3]:
						self["static_animation"] = callpropvoid.group(1)
						break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Boolean)(1 params, 0 optional)"):
				if "pushnull" in dumpscript[line + 5] and "coerce" in dumpscript[line + 6] and "setlocal_3" in dumpscript[line + 7] and "pushbyte 0" in dumpscript[line + 8]:
					self["crouch"] = (await find_one(PUBLIC_METHOD, content)).group(3)
					break

		if (crouch := self.get("crouch")) is not None:
			for line, content in enumerate(dumpscript):
				if f"callpropvoid <q>[public]::{crouch}" in content and (getproperty := await find_one(GET_PROPERTY, dumpscript[line - 1])) is not None:
					self["static_side"] = getproperty.group(2)
					break

		if (static_side := self.get("static_side")) is not None:
			for line, content in enumerate(dumpscript):
				if content.endswith("x_finAnimConfetti=()(0 params, 0 optional)"):
					if f"getproperty <q>[public]::{static_side}" in dumpscript[line + 7] and (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[line + 8])) is not None:
						self["crouch2"] = callpropvoid.group(1)
						break

		for line, content in enumerate(dumpscript):
			if "getlocal_0" in content and "getlocal_1" in dumpscript[line + 1] and "callproperty <q>[public]::readShort, 0 params" in dumpscript[line + 2]:
				if (initproperty := await find_one(INIT_PROPERTY, dumpscript[line + 3])) is not None and "getlocal_0" in dumpscript[line + 4] and "getlocal_1" in dumpscript[line + 5]:
					if "callproperty <q>[public]::readByte, 0 params" in dumpscript[line + 6] and "initproperty" in dumpscript[line + 7] and "getlocal_0" in dumpscript[line + 8]:
						if "getlocal_1" in dumpscript[line + 9] and "callproperty <q>[public]::readByte, 0 params" in dumpscript[line + 10]:
							if "initproperty" in dumpscript[line + 11] and "getlocal_0" in dumpscript[line + 12] and "getlocal_1" in dumpscript[line + 13]:
								if "callproperty <q>[public]::readUTF, 0 params" in dumpscript[line + 14]:
									self["player_title"] = initproperty.group(1)
									break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Boolean, <q>[public]::int = 0)(2 params, 1 optional)") and "pushnull" in dumpscript[line + 5] and "coerce" in dumpscript[line + 6]:
				self["jump"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Number = 0, <q>[public]::Number = 0)(2 params, 2 optional)") and "constructor" in content:
				for x in range(line, line + 10):
					if "constructsuper 0 params" in dumpscript[x]:
						self["b2vec2"] = (await find_one(CONSTRUCTOR_2, content)).group(1)
						break

		for line, content in enumerate(dumpscript):
			if content.endswith(", <q>[public]::Number)(2 params, 0 optional)"):
				for x in range(line, line + 30):
					if "getlex <q>[public]::Number" in dumpscript[x] and "getproperty <q>[public]::MIN_VALUE" in dumpscript[x + 1]:
						self["get_x_form"] = (await find_one(PUBLIC_METHOD, content)).group(3)
						break
		
		if (get_x_form := self.get("get_x_form")) is not None:
			for line, content in enumerate(dumpscript):
				if f"callproperty <q>[public]::{get_x_form}" in content:
					i = 0
					for x in range(line, line + 25):
						if "getproperty <q>[public]::position" in dumpscript[x] and (getproperty := await find_one(GET_PROPERTY, dumpscript[x + 1])) is not None and "convert_d" in dumpscript[x + 2]:
							if not i:
								self["pos_x"] = self["physics_state_vx"] = getproperty.group(2)
							else:
								self["pos_y"] = self["physics_state_vy"] = getproperty.group(2)
								break
							i += 1

		if (pos_x := self.get("pos_x")) is not None and (pos_y := self.get("pos_y")) is not None:
			for line, content in enumerate(dumpscript):
				if "getlocal_3" in content and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None and f"getproperty <q>[public]::{pos_x}" in dumpscript[line + 2]:
					if "getlocal_3" in dumpscript[line + 3]:
						self["physics_state"] = getproperty.group(2)
						break

		if (b2vec2 := self.get("b2vec2")) is not None and (physics_state := self.get("physics_state")) is not None:
			for line, content in enumerate(dumpscript):
				if "setlocal r5" in content and "getlocal r4" in dumpscript[line + 1] and (callproperty := await find_one(CALL_PROPERTY, dumpscript[line + 2])) is not None:
					if "coerce" in dumpscript[line + 3] and "setlocal r6" in dumpscript[line + 4] and "getlocal_0" in dumpscript[line + 5]:
						self["get_linear_velocity"] = callproperty.group(1)
						break

		for line, content in enumerate(dumpscript):
			if "jump" in content and "label" in dumpscript[line + 1] and (getlex := await find_one(GET_LEX, dumpscript[line + 2])) is not None:
				if "getlocal r9" in dumpscript[line + 3]:
					self["shaman_handler_class_name"] = self["anim_class_name"] = getlex.group(1)

					for x in range(line, line + 12):
						if (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[x])) is not None:
							self["update_coord"] = result = callpropvoid.group(1)
							self["change_player_speed1"] = result
							break
					break

		if (anim_class_name := self.get("anim_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{anim_class_name}" in content and "getlocal r" in dumpscript[line + 1] and "getlocal r" in dumpscript[line + 2]:
					if (callpropvoid := await find_one(CALL_PROPVOID, dumpscript[line + 3])) is not None and dumpscript[line + 3].endswith(", 2 params"):
						if "setlocal r" in dumpscript[line - 1]:
							self["change_player_speed2"]  = self["update_coord2"] = callpropvoid.group(1)
							break

		for line, content in enumerate(dumpscript):
			if "not" in content and "dup" in dumpscript[line + 1] and "iftrue" in dumpscript[line + 2] and "pop" in dumpscript[line + 3]:
				if (getlex := await find_one(GET_LEX, dumpscript[line + 4])) is not None and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 5])) is not None:
					if "not" in dumpscript[line + 7] and "dup" in dumpscript[line + 8] and "iftrue" in dumpscript[line + 9]:
						self["mouse_info_class_name"] = getlex.group(1)
						self["mouse_info_instance"] = getproperty.group(2)
						break

		if (mouse_info_class_name := self.get("mouse_info_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"getlex <q>[public]::{mouse_info_class_name}" in content and "negate" in dumpscript[line - 1]:
					if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 2])) is not None and "multiply" in dumpscript[line + 3]:
						self["jump_height"] = getproperty.group(2)
						break

		for line, content in enumerate(dumpscript):
			if "findpropstrict <q>[public]flash.utils::getTimer" in content and "getlocal_1" in dumpscript[line - 1]:
				if (setproperty := await find_one(SET_PROPERTY, dumpscript[line + 2])) is not None and "returnvoid" in dumpscript[line + 3]:
					self["jump_timestamp"] = setproperty.group(1)
					break

		for line, content in enumerate(dumpscript):
			if f", <q>[public]::int)(2 params, 0 optional)" in content and "pushnull" in dumpscript[line + 5] and "coerce" in dumpscript[line + 6]:
				if "setlocal_3" in dumpscript[line + 7] and "getlocal_1" in dumpscript[line + 8] and "getlocal_2" in dumpscript[line + 9]:
					if (setproperty := await find_one(SET_PROPERTY, dumpscript[line + 10])) is not None:
						self["player_cheese"] = setproperty.group(1)
						break

		for line, content in enumerate(dumpscript):
			if " getlex <q>[public]::Math" in content and "getlocal_1" in dumpscript[line + 1]:
				if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 2])) is not None:
					if "callproperty <q>[public]::abs, 1 params" in dumpscript[line + 3] and "getlocal r" in dumpscript[line + 4]:
						self["player_id"] = getproperty.group(2)
						break

		for line, content in enumerate(dumpscript):
			if "getlocal r5" in content and "getlocal_1" in dumpscript[line + 1] and "getproperty" in dumpscript[line + 2]:
				if (setproperty := await find_one(SET_PROPERTY, dumpscript[line + 3])) is not None:
					if "getlocal r5" in dumpscript[line + 4] and "iffalse" in dumpscript[line + 6]:
						self["player_id2"] = setproperty.group(1)
						break

		return self