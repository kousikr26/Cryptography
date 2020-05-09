from Crypto.Cipher import AES
from Crypto import Random
from multiprocessing import cpu_count
from pathos.multiprocessing import ProcessingPool as Pool
import time

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def xorEncrypt(key,inp,block):
    aes=AES.new(key, AES.MODE_ECB)
    decrypt_out = aes.encrypt(inp)
    return (byte_xor(block, decrypt_out))



class EncryptAES(object):
    """An implementation of CBC and CTR based block cipher encryption and decryption methods
        - Key should be a hex encoded byte string
        - Use 'cbc' or 'ctr' as 2nd argument(default is cbc)
        - Block size in bytes , default is 16 bytes(AES-128)
    """
    
    def __init__(self,key,mode='cbc',block_size=16,cores=cpu_count()):
        self.key=key
        self.mode=mode
        self.block_size=block_size
    
    def encrypt(self,message):
        if(self.mode=='cbc'):

            remainder = self.block_size-(len(message) % self.block_size)
            #Padding input message according to standard AES byte padding method
            if(remainder == 0):
                message += self.block_size*'a'
            else:
                message += remainder*hex(remainder)[2]
            
            message = message.encode('ASCII')
            blocks = []
            
            for i in range(0, len(message), self.block_size):
                blocks.append(message[i:i+self.block_size])
            
            aes=AES.new(self.key,AES.MODE_ECB)
            iv = Random.get_random_bytes(self.block_size)
            cipher_blocks = [iv]
            xor_inp=iv

            #Chaining blocks and ciphering
            for i in range(len(blocks)):
             
                temp_out = aes.encrypt(byte_xor(xor_inp, blocks[i]))
                cipher_blocks.append(temp_out)
                xor_inp=temp_out
            
            cipher_text=b''
            for i in cipher_blocks:
                cipher_text+=i
            return cipher_text
        elif(self.mode=='ctr'):
            message = message.encode('ASCII')
            blocks = []

            for i in range(0, len(message), self.block_size):
                blocks.append(message[i:i+self.block_size])
            #generate random IV
            iv = Random.get_random_bytes(self.block_size)
            #Generate inputs to multiprocessing function
            key_all = [self.key for i in range(len(blocks))]
            xor_inps = [bytes.fromhex(str(hex(int(iv.hex(), self.block_size)+i))[2:])
                        for i in range(len(blocks))]

            #Parallelise Encryption
            with Pool(8) as p:  # uses all cores available in parallel
                out = p.map(xorEncrypt, key_all, xor_inps, blocks)
           
            cipher_text=iv+b''.join(out)
            return cipher_text
    def decrypt(self,cipher):
        if(self.mode=='cbc'):
            #Extracing IV from cipher
            iv=cipher[0:self.block_size]
            cipher_blocks=[]
            for i in range(self.block_size,len(cipher),self.block_size):
                cipher_blocks.append(cipher[i:i+self.block_size])
            
            message_blocks=[]
            xor_inp=iv
            aes = AES.new(self.key, AES.MODE_ECB)
            #Chaining blocks and deciphering
            for i in range(len(cipher_blocks)):
                decrypt_out=aes.decrypt(cipher_blocks[i])
                message_blocks.append(byte_xor(xor_inp,decrypt_out))
                xor_inp=cipher_blocks[i]
            
            
            #Calculating pad      
            padding = int(str(message_blocks[len(message_blocks)-1])[-2],16)
            
            message_text=b''
            for i in message_blocks:
                message_text+=i
            #removing padding
            message_text=message_text[:-padding]
            return message_text.decode("utf-8")
        elif(self.mode=='ctr'):
            #separate IV from cipher
            iv = cipher[0:self.block_size]
            #Split cipher into blocks of given block_size
            cipher_blocks = []
            for i in range(self.block_size, len(cipher), self.block_size):
                cipher_blocks.append(cipher[i:min(i+self.block_size,len(cipher))])
            #Generate inputs for Multiprocessing function
            key_all=[self.key for i in range(len(cipher_blocks))]
            #xor_inps is the sequence iv, iv+1,iv+2... used in ctr mode
            xor_inps = [bytes.fromhex(str(hex(int(iv.hex(), self.block_size)+i))[2:]) for i in range(len(cipher_blocks))]
            with Pool(8) as p:  # uses all cores available in parallel
                out = p.map(xorEncrypt,key_all, xor_inps,cipher_blocks)

            message_text = (b''.join(out)).decode("utf-8")
            return message_text


        



if __name__=='__main__':
    file=open("bible.txt","r")
    message = file.read()
    cipher = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
    cipher=bytes.fromhex(cipher)
    key = "36f18357be4dbd77f050515c73fcf9f2"
    key=bytes.fromhex(key)

    print("Using",cpu_count(),"cores")
    startTime=time.time()
    aes=EncryptAES(key,mode='ctr',cores=1)
    aes.decrypt(aes.encrypt(message))
    print("Time taken non parallel ", time.time()-startTime,
          " seconds", "Message length ", len(message))
    
    startTime = time.time()
    aes_parallel=EncryptAES(key, mode='ctr',cores=cpu_count())
    aes.decrypt(aes.encrypt(message))
   
    print("Time taken parallel",time.time()-startTime," seconds", "Message length ",len(message))
