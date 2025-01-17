import gmpy2
from gmpy2 import mpz,div,gcdext
import time
from math import ceil,sqrt
""" Various attacks on RSA when the primes are chosen close together"""

n1 = "17976931348623159077293051907890247336179769789423065727343008115 \
     77326758055056206869853794492129829595855013875371640157101398586 \
     47833778606925583497541085196591615128057575940752635007475935288 \
     71082364994994077189561705436114947486504671101510156394068052754 \
     0071584560878577663743040086340742855278549092581"
n2 = "6484558428080716696628242653467722787263437207069762630604390703787 \
    9730861808111646271401527606141756919558732184025452065542490671989 \
    2428844841839353281972988531310511738648965962582821502504990264452 \
    1008852816733037111422964210278402893076574586452336833570778346897 \
    15838646088239640236866252211790085787877"
n3 = "72006226374735042527956443552558373833808445147399984182665305798191 \
    63556901883377904234086641876639384851752649940178970835240791356868 \
    77441155132015188279331812309091996246361896836573643119174094961348 \
    52463970788523879939683923036467667022162701835329944324119217381272 \
    9276147530748597302192751375739387929"
n4 = "22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540"
e=65537
n1 = mpz(n1)
n2 = mpz(n2)
n3 = mpz(n3)
n4 = mpz(n4)
e=mpz(e)


def modInverse(b, m):
    return pow(b, m - 2, m)
def attack1(N):
    """
    |p-q|<2N^(1/4)
    """
    A, r = gmpy2.isqrt_rem(N)
    if(r>0):
        A+=1
    x,r=gmpy2.isqrt_rem(A*A-N)
    if(r>0):
        x+=1
    if(N%(A-x)==0 and N%(A+x)==0):
        print("Factors are ",A-x,A+x)
        return A-x,A+x
    
def attack2(N):
    """
    |p-q|<2^11 N^(1/4)
    """
    sqrtN, _ = gmpy2.isqrt_rem(N)
    if _>0:
        sqrtN+=1
    for i in range(sqrtN,sqrtN+pow(2,20)+10):
        x, r = gmpy2.isqrt_rem(i*i-N)
        if(r > 0):
            x += 1
        if(N % (i-x) == 0 and N % (i+x) == 0):
            print("Factors are ", i-x, i+x)
            break


def attack3(N):
    """
    |3p-2q|<N^(1/4)
    """
    N*=4
    A, r = gmpy2.isqrt_rem(6*N)
    if(r > 0):
        A += 1
    x, r = gmpy2.isqrt_rem(A*A-6*N)
    if(r > 0):
        x += 1
    
    if(N % div(A-x,6) == 0 and N % div(A+x,4) == 0):
        print("Factors are ", div(A-x,6), div(A+x,4))

def attack4(N,e,c):
    """Given RSA modulus N with |p-q|<2N^(1/4)
        public exponent e,
        and ciphertext c

        Note: e.d=1 mod(phi(N))
    """
    p, q = attack1(N)
    phi=(p-1)*(q-1)
    #print(p*q)
    g,s,t=gcdext(e,phi)
    d=s
    
    m=pow(c,d,N)
    print("Decrypted message ",m)
    print("Hex encoding",hex(m))

    




attack1(n1)
attack2(n2)
attack3(n3)
attack4(n1,e,n4)
