import sqlalchemy as sql
from pathlib import Path
import sys

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password):
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 1_200_000,
        )
    return base64.urlsafe_b64encode(kdf.derive(password))

def decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)

def Hash(x, salt):
    h = hashes.Hash(hashes.SHA256())
    h.update(x + salt)
    return h.finalize()

while True:
    path = input('Database path> ')
    if path == '':
        sys.exit()
    if not Path(path).is_file():
        print(f'No such file could be found on disk.')
    else:
        print('Fetching database from memory.')
        break

engine = sql.create_engine(f'sqlite:///{path}')
meta = sql.MetaData()
meta.reflect(bind = engine)

SaltsT = meta.tables['salts']
FilesT = meta.tables['files']

print('Fetching salt.')

salts = []

with engine.connect() as conn:
    rows = conn.execute(sql.select(SaltsT))
    for id, salt in rows:
        salts.append(salt)

salt = salts[0]

while True:
    password = input('Please enter your password: ')
    pss = bytes(password, encoding = 'utf-8')
    key = derive_key(pss)
    h = Hash(key, salt)

    x = sql.select(FilesT).where(FilesT.c.hash == h)
    with engine.connect() as conn:
        ys = conn.execute(x)
        for h, cipher in ys:
            break
        else:
            print('Invalid password. Please try again.')
            continue

    break

plain = decrypt(key, cipher).decode('utf-8')
print('======Decrypting File======')
print(plain)