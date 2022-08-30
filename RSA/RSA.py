# Jason Ketterer
# FSUID: jrk08j

import math
from random import randint

class RSA():
    '''RSA encryption/decryption system'''

    def __init__(self):
        self._messages = []
        self._e = 0
        self._d = 0
        self._N = 0

    def inputFunc(self):
        num_messages = self.getIntInput("Enter the number of messages: ")
        print("Enter the messages:")
        while num_messages > 0:
            m = self.getIntInput("")
            self._messages.append(m)
            num_messages -= 1

    def printFunc(self, m):
        return "message is " + str(m)

    def printDecryptedMsg(self, print_msg):
        '''decorator for printFunc'''
        def wrapper(m):
            print("The decrypted message is " + print_msg(m))
        return wrapper

    def printEncryptedMsg(self, print_msg):
        '''decorator for printFunc'''
        def wrapper(m):
            print("The encrypted message is " + print_msg(m))
        return wrapper

    def primeGen(self, n):
        '''Generator function that finds 2 primes starting at n'''
        num_primes = 2
        while num_primes > 0:
            if self.isPrime(n):
                yield n
                num_primes -= 1
            n += 1

    def isPrime(self, n):
        '''From: https://en.wikipedia.org/wiki/Primality_test
            Based on observation that all primes greater than 6 are of the form 6k+-1'''
        if n <= 3:
            return n > 1
        elif n % 2 == 0 or n % 3 == 0:
            return False

        k = 5

        while k * k <= n:
            if n % k == 0 or n % (k + 2) == 0:
                return False
            k += 6

        return True

    def keyGen(self):
        '''Generates public/private keys'''
        minPrime = self.getIntInput("Enter the minimum value for the prime numbers: ")
        primes = self.primeGen(minPrime)
        p = primes.__next__()
        q = primes.__next__()
        self._N = p * q
        lambda_N = self.totient(p,q)
        self._e = self.find_e(lambda_N)
        self._d = self.multiplicativeInverse(self._e, lambda_N)
        print("N is " + str(self._N))
        print("e is " + str(self._e))

    def multiplicativeInverse(self, e, l):
        '''d is the modular multiplicative inverse of e modulo l
        This is just the 's' coefficient of the Bezout identity
        sa + tb = gcd(a,b), which can be computed using the Extended
        Euclidean algorithm'''
        result = self.gcdExtended(e,l)
        d = result['s']

        # d must be in the range of [0, 1, 2, ...l-1]
        if d < 0:
            d += l
        return d

    def find_e(self, lambda_N):
        '''Finds an integer e such that:
            1 < e < lambda_N and GCD(e, lambda_N) = 1'''
        while True:
            e = randint(2, lambda_N-1)
            result = self.gcdExtended(e, lambda_N)
            if result['gcd'] == 1:
                break
        return e

    def gcdExtended(self, a, b):
        """Computes the GCD of a and b and the Bezout coefficients s, t:
            sa + tb = gcd(a,b)
            returns a dict with keys = s, t, gcd
            Based on the information and algorithms presented in the text:
            Discrete Mathematics and Its Applications, 7th ed., Ken Rosen, pp. 267-270"""
        x = a
        y = b
        oldold_s = 1
        old_s = 0
        oldold_t = 0
        old_t = 1
        while y != 0:
            q = x // y
            r = x % y
            x = y
            y = r
            s = oldold_s - q * old_s
            t = oldold_t - q * old_t
            oldold_s = old_s
            oldold_t = old_t
            old_s = s
            old_t = t

        return { 's': oldold_s, 't': oldold_t, 'gcd': x }

    def totient(self, p, q):
        '''two versions of this function, one of which uses
        the lcm; using version in hw doc...'''
        # return self.lcm(p-1, q-1)
        return (p-1) * (q-1)

    def lcm(self, a, b):
        result = self.gcdExtended(a,b)
        return a * b // result['gcd']

    def getIntInput(self, prompt):
        """Helper function to get and validate integer input from user"""
        i = 0
        while True:
            try:
                i = int( input(prompt) )
                break
            except ValueError:
                print("Input not an integer.")
                continue
        return i

    def encrypt(self, m):
        '''encrypt message m by using m^e mod N'''
        return self.modularExponentiation(m, self._e, self._N)

    def decrypt(self, c):
        '''decrypt ciphered message c by using c^d mod N'''
        return self.modularExponentiation(c, self._d, self._N)

    def modularExponentiation(self, b, e, m):
        '''calculates x = b^e mod m
            Based on pseudocode here: https://en.wikipedia.org/wiki/Modular_exponentiation'''
        if m == 1:
            return 0
        x = 1
        b = b % m
        while e > 0:
            if e % 2 == 1:
                x = (x * b) % m
            e >>= 1
            b = (b * b) % m
        return x

    def messages(self):
        '''driver function for the RSA system'''
        self.inputFunc()
        self.keyGen()

        # use iterator to encrypt messages
        encrypted = []
        msg_iter = iter(self._messages)

        while True:
            try:
                encrypted.append(self.encrypt(next(msg_iter)))
            except StopIteration:
                break

        printMsg = self.printEncryptedMsg(self.printFunc)

        for m in encrypted:
            printMsg(m)

        # use iterator to decrypt messages
        decrypted = []
        msg_iter = iter(encrypted)

        while True:
            try:
                decrypted.append(self.decrypt(next(msg_iter)))
            except StopIteration:
                break

        printMsg = self.printDecryptedMsg(self.printFunc)

        for m in decrypted:
            printMsg(m)

def main():
    rsa = RSA()
    rsa.messages()

if __name__ == '__main__': main()
