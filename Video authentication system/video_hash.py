from hashlib import sha256

test = "6.1.intro.mp4_download"

def videoAuthentication(file_path,block_size=1024):
    """An authentication system to test the authenticity of a streamed video
        block_size length blocks are downloaded and authenticated at a time

        This uses SHA256 as the MAC
    """


    test=file_path
    encrypted=b""
    
    print("Reading from file ",test)
    with open(test,"rb") as file:
        byte=file.read()
        print(len(byte))
        bytelis=[byte[i:i+block_size] for i in range(0,len(byte),block_size)][::-1]
        for i in range(len(bytelis)-1):

            shasum = sha256(bytelis[i]).digest()
            bytelis[i+1]+=shasum
        print(sha256(bytelis[len(bytelis)-1]).hexdigest())
        bytelis=bytelis[::-1]
        for i in bytelis:
            encrypted+=i
    
    print("Writing to ", "encrypted_"+test)
    with open("encrypted_"+test,"wb") as file:
        file.write(encrypted)

if __name__=='__main__':
    videoAuthentication(test)


