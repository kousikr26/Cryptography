

def IP(text):
    perm = [1,5,2,0,3,7,4,6]
    outtext = ""
    for i in perm:
        outtext+=text[i]
    return outtext
def IPinv(text):
    perm = [3,0,2,4,6,1,7,5]
    outtext = ""
    for i in perm:
        outtext+=text[i]
    return outtext
def swapNibble(text):
    return text[4:]+text[:4]

def expPerm(text):
    outtext = ""
    perm = [3,0,1,2,1,2,3,0]
    for i in perm:
        outtext+=text[i]
    return outtext
def xor(text1,text2):
    outtext=""
    for i in range(len(text1)):
        if(text1[i]!=text2[i]):
            outtext+='1'
        else:
            outtext+='0'
    return outtext
def P10(text):
    outtext=""
    perm = [2,4,1,6,3,9,0,8,7,5]
    for i in perm:
        outtext+=text[i]
    return outtext
def P8(text):
    outtext=""
    perm = [5,2,6,3,7,4,9,8]
    for i in perm:
        outtext+=text[i]
    return outtext
def P4(text):
    outtext=""
    perm = [1,3,2,0]
    for i in perm:
        outtext+=text[i]
    return outtext
def LCS1(text):
    return text[1:5]+text[0]+text[6:]+text[5]
def LCS2(text):
    return text[2:5]+text[0:2]+text[7:]+text[5:7]

def S0(text):
    row = int(text[0] + text[3], 2)
    column = int(text[1] + text[2], 2)
    perm = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
     ]
    return bin(perm[row][column])[2:].zfill(4)
def S1(text):
    row = int(text[0] + text[3], 2)
    column = int(text[1] + text[2], 2)
    perm = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
     ]
    return bin(perm[row][column])[2:].zfill(4)

def generateKeys(key):
    intermediateKey = LCS1(P10(key))
    key1 = P8(intermediateKey)
    intermediateKey2 = LCS2(intermediateKey)
    key2 = P8(intermediateKey2)
    return key1,key2

def fBox(text,halfKey):
    left = text[:4]
    right = text[4:]
    expanded = expPerm(right)
    xored = xor(expanded,halfKey)
    substituted = P4(S0(xored[:4])+S1(xored[4:]))
    xored2 = xor(substituted,left)
    return xored2+right
def encryptSDES(plaintext,key):
    key1,key2 = generateKeys(key)
    return IPinv(fBox(swapNibble(fBox(IP(plaintext),key1)),key2))

def decryptSDES(ciphertext,key):
    key1,key2 = generateKeys(key)
    return IPinv(fBox(swapNibble(fBox(IP(ciphertext),key2)),key1))

plaintext=""
ciphertext="01000110"
key = "1010000010"


print("Ciphertext : "+ciphertext)
print("Key : "+key)
plaintext = decryptSDES(ciphertext,key)
print("Plaintext : "+plaintext)
print("Rencrypting plaintext with key : " +encryptSDES(plaintext,key))
