from pwdlib import PasswordHash
pwdcontext = PasswordHash.recommended()
print(pwdcontext.hash("dude"))
