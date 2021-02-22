

def encryptCaesar(text, key):
    text = text.lower()
    newtext = ""
    for i in range(len(text)):
        if(text[i]==' '):
            newtext+=' '
            continue
        newtext+=(chr((ord(text[i])-ord('a')+key)%26 + ord('a')))
    return newtext


def decryptCaesar(text, key):
    text = text.lower()
    newtext=""
    for i in range(len(text)):
        if(text[i]==' '):
            newtext+=' '
            continue
        newtext+=chr((ord(text[i])-ord('a')+26-key)%26 + ord('a'))
    return newtext

key = 3

message = "Meet me near serpentine at midnight"
print("Message : ",message)
cipher = encryptCaesar(message,key)
print("Encrypted message : ",cipher)
decryptedMessage = decryptCaesar(cipher,key)
print("Decrypted message : ",decryptedMessage)
