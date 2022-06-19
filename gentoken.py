import secrets

def gen_token() -> str:
	return secrets.token_hex(32)

if __name__ == "__main__":
	print(gen_token())