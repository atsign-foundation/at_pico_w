""" From original secrets.py CPython library 
"""

import random
import ubinascii

class IVNonce:

    def _randbytes(self, nbytes):
        """Generate n random bytes."""
        # CPython isn't limited to 32 bits:
        # return random.getrandbits(nbytes * 8).to_bytes(n, 'little')
        
        randbytes = bytearray()
        while nbytes > 0:
            num_bytes = min(nbytes, 4)  # Generation is limited to 32 bits (4 bytes)
            randbits = random.getrandbits(num_bytes * 8)
            randbytes.extend(randbits.to_bytes(num_bytes, 'little'))
            nbytes -= num_bytes
        return bytes(randbytes)
    
    def token_bytes(self):
        return self.randbytes
    
    def token_hex(self):
        # check upython compat for decode
        return binascii.hexlify(token_bytes()).decode('ascii') 

    def __init__(self, n:int=16):
        self.n = n
        self.randbytes = self._randbytes(n)