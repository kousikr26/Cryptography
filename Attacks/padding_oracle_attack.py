import urllib.request
import sys
from multiprocessing import Pool, cpu_count

TARGET = 'http://crypto-class.appspot.com/po?er='
BLOCK_SIZE = 16
""" A parallelised implementation of the padding oracle attack on a dummy website"""

def strxor(a, b):     # xor two strings of different 
    a = b'\x00'*(16-len(a))+a
    b=b'\x00'*(16-len(b))+b
    return bytes(x ^ y for x, y in zip(a, b))


def incrementBytes(by):
    bynum = int.from_bytes(by, 'big')
    bynum += 1
    return bynum.to_bytes(len(by), 'big')

def joinlis(lis):
    return b''.join(lis)
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------


class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.request.quote(q)  # Create query URL
        req = urllib.request.Request(target)       # Send request to server
        try:
            f = urllib.request.urlopen(req)  
            print("success")
            return True
        except urllib.error.HTTPError as e:
           # print("We got: {}".format(e.code))     # Print response code
            if e.code == 404:
                return True  # good padding
            return False  # bad padding
def blockattack(blockn):
    freq = b' etaonhisrdluwmycgf,bp.vk"I\'-T;HMWA_SB?x!jEzCqLDYJNO:PRGFKVUXQ()0*128453679Z[]/$@&#%+<=>\\^`{|}~\x10\x0f\x0e\x0d\x0c\x0b\x0a\x09\x08\x07\x06\x05\x04\x03\x02\x01\x00'
    blocks = [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    padlen = 1
    padval=b'\x01'

    suffix=b''

    po = PaddingOracle()

    for j in range(BLOCK_SIZE):
        
        
        #for i in range(255):
        for i in range(len(freq)):
            blockscopy=blocks[:]
            guess=bytes([freq[i]])
            
            
            blockscopy[blockn]=strxor(blockscopy[blockn],strxor(guess+suffix,padval*padlen))
            
            querytext=joinlis(blockscopy[:blockn+2]).hex()

            if(po.query(querytext)):
                print("CHARACTER FOUND  ", guess)
                suffix=guess+suffix
                padlen+=1
                padval=incrementBytes(padval)
                
                break
            # guess=decrementBytes(guess)
                    
                

    print("GUESS IS ",suffix)
def attack(ciphertext):
    freq = b' etaonhisrdluwmycgf,bp.vk"I\'-T;HMWA_SB?x!jEzCqLDYJNO:PRGFKVUXQ()0*128453679Z[]/$@&#%+<=>\\^`{|}~\x10\x0f\x0e\x0d\x0c\x0b\x0a\x09\x08\x07\x06\x05\x04\x03\x02\x01\x00'
    blocks = [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    
    with Pool(len(blocks)+2) as p:  # uses all cores available in parallel
        arglst = [i for i in range(len(blocks)-1)]
        out = p.map(blockattack, arglst)
        print()
        print(out)


       






if __name__ == "__main__":
    ciphertext = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
    print('Avaliable Cores:', cpu_count())
    ciphertext=bytes.fromhex(ciphertext)
    attack(ciphertext)
    
    
