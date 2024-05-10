from bitstring import BitStream

class RBSPBits :
    def __init__(self, bits):
        self.bits = BitStream(bits)
    
    def f(self, n):
        return self.bits.read(n).uint
    
    def u(self, n):
        return self.bits.read(n).uint
    
    def ue(self):
        return self.bits.read('ue')
    
    def se(self):
        return self.bits.read('se')
    
    def more_rbsp_data(self):
        if not self.bits.pos < self.bits.len:
            return False
        has = self.bits.peek(1)
        i = self.bits.length - 1
        while i >= 0:
            if self.bits[i] == True:
                if self.bits.pos == i:
                    return False
                else:
                    return True
            i -= 1
        return False
    
    def byte_aligned(self):
        return (self.bits.pos % 8) == 0