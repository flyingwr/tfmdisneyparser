from .regex import CALL_PROPVOID, COERCE, CONSTRUCTOR, FINAL_METHOD, FIND_PROPSTRICT, GET_LEX, GET_PROPERTY, INIT_PROPERTY, PUBLIC_METHOD, PUBLIC_SLOT, find_one

from typing import Dict, List

class UI(dict):
	async def fetch(self, dumpscript: List) -> Dict:
		for line, content in enumerate(dumpscript):
			if "slot 0: var" in content and ":<q>[public]__AS3__.vec::Vector" in content:
				if ":<q>[public]flash.utils::Timer" in dumpscript[line + 2]:
					if "Boolean =" not in dumpscript[line + 1]:
						if (slot := await find_one(PUBLIC_SLOT, dumpscript[line + 1])) is not None:
							self["ui_element_class_name"] = slot.group(2)
							break

		if (ui_element_class_name := self.get("ui_element_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if f"method <q>[public]::{ui_element_class_name}" in content and content.endswith("=(<q>[public]::int, <q>[public]::int)(2 params, 0 optional)"):
					if "findpropstrict" in dumpscript[line + 5]:
						if "getlocal_1" in dumpscript[line + 6] and "getlocal_2" in dumpscript[line + 7]:
							if "constructprop" in dumpscript[line + 8] and "coerce" in dumpscript[line + 9]:
								if "setlocal_3" in dumpscript[line + 10] and "getlocal_3" in dumpscript[line + 11]:
									if "getlex" in dumpscript[line + 12] and "getproperty" in dumpscript[line + 13] and "callpropvoid" in dumpscript[line + 14]:
										if "getlocal_0" in dumpscript[line + 15] and "getlocal_3" in dumpscript[line + 16]:
											if "callpropvoid" in dumpscript[line + 17] and "getlocal_3" in dumpscript[line + 18] and "returnvalue" in dumpscript[line + 19]:
												self["prep_ui_class_name"] = (await find_one(GET_LEX, dumpscript[line + 12])).group(1)
												self["set_prep_ui"] = (await find_one(CALL_PROPVOID, dumpscript[line + 14])).group(1)
												self["add_ui_element"] = (await find_one(CALL_PROPVOID, dumpscript[line + 17])).group(1)
												break

			if (prep_ui_class_name := self.get("prep_ui_class_name")) is not None:
				for line, content in enumerate(dumpscript):
					if f"getlex <q>[public]::{prep_ui_class_name}" in content:
						for x in range(line, line - 10, -1):
							if "getproperty <q>[public]::TIMER" in dumpscript[x] and "getlocal_0" in dumpscript[x + 1]:
								if (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None:
									self["prep_ui4_instance"] = getproperty.group(2)
									break
						else:
							continue
						break

				if (prep_ui4_instance := self.get("prep_ui4_instance")) is not None:
					for line, content in enumerate(dumpscript):
						if f"getlex <q>[public]::{prep_ui_class_name}" in content and (getproperty := await find_one(GET_PROPERTY, dumpscript[line + 1])) is not None:
							for x in range(line, line + 10):
								if "callpropvoid" in dumpscript[x] and "findpropstrict <q>[public]flash.display::Shape" in dumpscript[x + 1]:
									if "coerce" in dumpscript[x + 3] and "setlocal_1" in dumpscript[x + 4] and "getlocal_1" in dumpscript[x + 5]:
										if (result := getproperty.group(2)) != prep_ui4_instance:
											self["prep_ui1_instance"] = result
											break
							else:
								continue
							break

			for line, content in enumerate(dumpscript):
				if content.endswith(f"=(<q>[public]::String, <q>[public]::{ui_element_class_name})(2 params, 0 optional)"):
					if (public_method := await find_one(PUBLIC_METHOD, content)) is not None:
						self["ui_items_list_class_name"] = public_method.group(2)
						break
			
			if (ui_items_list_class_name := self.get("ui_items_list_class_name")) is not None:
				for line, content in enumerate(dumpscript):
					if f"method <q>[public]::{ui_items_list_class_name}" in content and content.endswith("=(<q>[public]::int)(1 params, 0 optional)"):
						self["select_item"] = (await find_one(PUBLIC_METHOD, content)).group(3)
						break
		
		for line, content in enumerate(dumpscript):
			if "=(<q>[public]::String, <q>[public]::Function = null, <q>[public]::int = 10)(3 params, 2 optional)" in content:
				self["set_box"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Boolean = true)(1 params, 1 optional)"):
				for x in range(line, line + 10):
					if "pushnull" in dumpscript[x] and "coerce <q>[public]flash.display::DisplayObject" in dumpscript[x + 1] and "setlocal r4" in dumpscript[x + 2]:
						self["set_draggable"] = (await find_one(PUBLIC_METHOD, content)).group(3)
						break
				else:
					continue
				break

		for line, content in enumerate(dumpscript):
			if "=(<q>[public]::String)(1 params, 0 optional)" in content:
				if "findproperty <q>[public]::mouseEnabled" in dumpscript[line + 5]:
					if "initproperty <q>[public]::mouseEnabled" in dumpscript[line + 8]:
						if "getlex" in dumpscript[line + 9]:
							if "getlocal_0" in dumpscript[line + 10] and "getlocal_1" in dumpscript[line + 11]:
								if "callpropvoid" in dumpscript[line + 12] and "returnvoid" in dumpscript[line + 13]:
									self["ui_manager_class_name"] = (await find_one(GET_LEX, dumpscript[line + 9])).group(1)
									self["on_mouse_box"] = (await find_one(CALL_PROPVOID, dumpscript[line + 12])).group(1)
									break

		for line, content in enumerate(dumpscript):
			if "=(<q>[public]flash.display::DisplayObject, <q>[public]::Boolean = false, <q>[public]::Boolean = false)(3 params, 2 optional)" in content:
				for x in range(line, line + 30):
					if (coerce := await find_one(COERCE, dumpscript[x])) is not None:
						self["ui_sprite_class_name"] = coerce.group(1)
						break
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::int, <q>[public]::String = null)(2 params, 1 optional)"):
				if "pushnull" in dumpscript[line + 5] and "coerce <q>[public]flash.utils::ByteArray" in dumpscript[line + 6]:
					self["ui_sprite2_class_name"] = (await find_one(FINAL_METHOD, content)).group(2)
					break
		
		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Function = null, <q>[public]::Object = null, <q>[public]::Boolean = true)(3 params, 3 optional)"):
				self["on_mouse_click"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::int, <q>[public]::int, <q>[public]::int = 0)(3 params, 1 optional)"):
				if "getlex" in dumpscript[line + 5]:
					if "getlocal_0" in dumpscript[line + 6] and "getlocal_3" in dumpscript[line + 7]:
						if "callpropvoid" in dumpscript[line + 8]:
							self["main_ui_class_name"] = (await find_one(GET_LEX, dumpscript[line + 5])).group(1)
							self["add_ui"] = (await find_one(CALL_PROPVOID, dumpscript[line + 8])).group(1)
							break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::int, <q>[public]::int, <q>[public]::Boolean, <q>[public]::int, <q>[public]::int = 0, <q>[public]::int = 0)(6 params, 2 optional)"):
				self["set_shape"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]flash.events::FocusEvent)(1 params, 0 optional)"):
				if "pushnull" in dumpscript[line + 5] and (coerce := await find_one(COERCE, dumpscript[line + 6])) is not None:
					self["ui_button_class_name"] = coerce.group(1)
					break

		if (ui_button_class_name := self.get("ui_button_class_name")) is not None:
			for line, content in enumerate(dumpscript):
				if content.endswith("=(<q>[public]::Boolean)(1 params, 0 optional)") and f"method <q>[public]::{ui_button_class_name}" in content:
					if "getlocal_0" in dumpscript[line + 5] and "getlocal_1" in dumpscript[line + 6]:
						if "initproperty" in dumpscript[line + 7] and "getlocal_1" in dumpscript[line + 8]:
							self["set_button_state"] = (await find_one(PUBLIC_METHOD, content)).group(3)
							self["button_state"] = (await find_one(INIT_PROPERTY, dumpscript[line + 7])).group(1)
							break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::String = , <q>[public]::int = 0)(2 params, 2 optional)"):
				self["ui_check_box_class_name"] = (await find_one(CONSTRUCTOR, content)).group(1)
				
				for x in range(line, line + 200):
					if "getproperty <q>[public]::y" in dumpscript[x] and "setproperty <q>[public]::y" in dumpscript[x + 1]:
						if (findpropstrict := await find_one(FIND_PROPSTRICT, dumpscript[x + 3])) is not None:
							self["ui_text_field_class_name"] = findpropstrict.group(1)
							break
				else:
					continue
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Function = null, <q>[public]::Object = null, <q>[public]::Boolean = false)(3 params, 3 optional)"):
				self["check_box_callback"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::Boolean, <q>[public]::int = 60, <q>[public]::Boolean = false)(3 params, 2 optional)"):
				self["set_scrollable"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if "add" in content and "coerce_s" in dumpscript[line + 1]:
				if "setlocal_1" in dumpscript[line + 2] and "getlocal_0" in dumpscript[line + 3]:
					if "getproperty" in dumpscript[line + 4] and "getproperty" in dumpscript[line + 5]:
						if "getlocal_1" in dumpscript[line + 6] and "setproperty <q>[public]::text" in dumpscript[line + 7]:
							if "getlocal_1" in dumpscript[line + 8] and "getproperty <q>[public]::length" in dumpscript[line + 9]:
									self["text_field"] = (await find_one(GET_PROPERTY, dumpscript[line + 5])).group(2)
									break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::String, <q>[public]::Boolean = true, <q>[public]::Boolean = true)(3 params, 2 optional)"):
				self["set_display_text"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		for line, content in enumerate(dumpscript):
			if content.endswith(", <q>[public]::Function)(3 params, 0 optional)") and "method <q>[public]::void" not in content:
				if "findpropstrict" in dumpscript[line + 5]:
					self["ui_check_button_class_name"] = (await find_one(PUBLIC_METHOD, content)).group(2)

					for x in range(line, line + 20):
						if "setlocal r4" in dumpscript[x] and "getlocal r4" in dumpscript[x + 1]:
							self["text_field2"] = (await find_one(GET_PROPERTY, dumpscript[x + 2])).group(2)
							break
					break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]flash.events::Event)(1 params, 0 optional)"):
				if "getlocal_0" in dumpscript[line + 5] and "getlocal_0" in dumpscript[line + 6]:
					if "getproperty" in dumpscript[line + 7] and "not" in dumpscript[line + 8]:
						self["check_button_exec"] = (await find_one(PUBLIC_METHOD, content)).group(3)
						self["is_selected"] = (await find_one(GET_PROPERTY, dumpscript[line + 7])).group(2)
						break

		for line, content in enumerate(dumpscript):
			if content.endswith("=()(0 params, 0 optional)"):
				if "getlocal_0" in dumpscript[line + 5] and "getproperty" in dumpscript[line + 6]:
					if "callpropvoid <q>[public]::clear, 0 params" in dumpscript[line + 7] and "getlocal_0" in dumpscript[line + 8]:
						if "returnvalue" in dumpscript[line + 9]:
							public_method = await find_one(PUBLIC_METHOD, content)
							self["packet_out_class_name"] = public_method.group(2)
							self["reset_ui"] = public_method.group(3)
							
							self["socket_data"] = getproperty = (await find_one(GET_PROPERTY, dumpscript[line + 6])).group(2)
							self["packet_out_bytes"] = getproperty
							break

		for line, content in enumerate(dumpscript):
			if content.endswith("=(<q>[public]::String, <q>[public]::Function, <q>[public]::Object = null, <q>[public]::Boolean = false)(4 params, 2 optional)"):
				self["add_to_list"] = (await find_one(PUBLIC_METHOD, content)).group(3)
				break

		return self