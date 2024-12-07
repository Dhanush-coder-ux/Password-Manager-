from cryptography.fernet import Fernet
import os
import json

def decrypt():
    with open('key.key','rb') as k:
        key=k.read()
    with open('password.key','rb') as p:
        password=p.read()
    
    de=Fernet(key).decrypt(password)
    return json.loads(de.decode())

def encrypt(domain_name,password,isdelete):
    if not os.path.exists('key.key'):
        key=Fernet.generate_key()
        with open('key.key','wb') as w:
            w.write(key)
    else:
        with open('key.key','rb') as r:
            key=r.read()
    f=Fernet(key)

    if os.path.exists('password.key'):
        decryptpass=decrypt()
        if isdelete:
            decryptpass=isdelete
        else:
            decryptpass['domain'].append(domain_name)
            decryptpass['domain_password'].append(password)
    else:
        decryptpass={'domain':[domain_name],"domain_password":[password]}

    enc=f.encrypt(json.dumps(decryptpass).encode())
    with open('password.key','wb') as p:
        p.write(enc)
        
def delet(domain,domain_pass):
    dltdecrypt=decrypt()
    if os.path.exists('password.key'):
        dltdecrypt['domain'].remove(domain) 
        dltdecrypt['domain_password'].remove(domain_pass)
        encrypt(None,None,dltdecrypt)
        print("successfullly dlt !!")
    else:
        print("password does not dlt")