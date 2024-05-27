from bitstring import BitStream

coded_block_pattern_idc_0 = [
[47 ,0]
,[31 ,16]
,[15 ,1]
,[0  ,2]
,[23 ,4]
,[27 ,8]
,[29 ,32]
,[30 ,3]
,[7  ,5]
,[11 ,10]
,[13 ,12]
,[14 ,15]
,[39 ,47]
,[43 ,7 ]
,[45 ,11]
,[46 ,13]
,[16 ,14]
,[3  ,6 ]
,[5  ,9 ]
,[10 ,31]
,[12 ,35]
,[19 ,37]
,[21 ,42]
,[26 ,44]
,[28 ,33]
,[35 ,34]
,[37 ,36]
,[42 ,40]
,[44 ,39]
,[1  ,43]
,[2  ,45]
,[4  ,46]
,[8  ,17]
,[17 ,18]
,[18 ,20]
,[20 ,24]
,[24 ,19]
,[6  ,21]
,[9  ,26]
,[22 ,28]
,[25 ,23]
,[32 ,27]
,[33 ,29]
,[34 ,30]
,[36 ,22]
,[40 ,25]
,[38 ,38]
,[41 ,41]
]

coded_block_pattern_idc_1 = [
[15 ,0]
,[0 ,1  ]
,[7 ,2  ]
,[11 ,4 ]
,[13 ,8 ]
,[14 ,3 ]
,[3 ,5  ]
,[5 ,10 ]
,[10 ,12]
,[12 ,15]
,[1 ,7]
,[2 ,11]
,[4 ,13]
,[8 ,14]
,[6 ,6]
,[9 ,9]
]

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

    def me(self, ChromaArrayType=0, inter=False):
        codeNum = self.ue()
        idx = 1 if inter else 0
        if ChromaArrayType == 1 or ChromaArrayType == 2 :
            return coded_block_pattern_idc_0[codeNum][idx]
        else:
            return coded_block_pattern_idc_1[codeNum][idx]
    
    def te(self, n):
        if n == 0:
            return 0
        if n > 1:
            return self.ue()
        else:
            b = self.f(1)
            return  0 if b == 1 else 1
            

    
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