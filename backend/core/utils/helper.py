import secrets

# Code generator
def generate_verification_code(length=6):
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))

