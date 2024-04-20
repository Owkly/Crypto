
def read(i):
    with open("/home/lucie/crypto/md5_collider/md5_collider/RES"+str(i),"rb") as f:
        out = f.read()
        print(out.hex())

for i in range(1,5):
    read(i)