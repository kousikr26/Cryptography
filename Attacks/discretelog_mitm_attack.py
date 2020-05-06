import gmpy2
from gmpy2 import mpz
import time
"""
A meet in the middle attach for discrete logarithm whch works in O(exp(sqrt(n))) using a hash table(dictionary) instead of bruteforce of O(exp(n)) where n is size of the number
Time taken: 2.1 seconds
n = 40 bits

"""
def modInverse(b, m):
    return pow(b, m - 2, m)



def modDivide(a, b, m):
    a = a % m
    inv = modInverse(b, m)    
    return (inv*a) % m

start=time.time()
expbits=40
p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333

p=mpz(p)
g=mpz(g)
h=mpz(h)
hash_table={}
print("Generating Hash table")
inc=modInverse(g,p)
inv=1
for i in range(pow(2,expbits//2)+10):
    # if(i%10000==0):
    #     print("Hashing "+str(i)+"/"+str(pow(2,expbits//2))+" complete")
    keyval=(h*inv)%p
    inv=(inv*inc)%p
    hash_table[keyval]=i
print("Meet in the middle")
base=pow(g,pow(2,expbits//2),p)
curr=1
for j in range(pow(2, expbits//2)+10):
    # if(j % 10000 == 0):
    #     print("Checking "+str(j)+"/"+str(pow(2, expbits//2))+" complete")
    checkval=curr
    curr=(curr*base)%p
    if checkval in hash_table:
        print("Success, x0 =",j,"x1 =",hash_table[checkval])
        print("x = ",(((j*pow(2,expbits//2))%p)+hash_table[checkval])%p)
        break
print("Time taken ",time.time()-start)