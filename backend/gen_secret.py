import secrets
with open("secret_key.key", "r+") as f:
    if f.read():
        print("there is already a key in secret_key.key")
    else:
        f.write(secrets.token_hex(16))


