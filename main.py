# This is a Python script for creating valuations and calculating slopes and minQ.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt

class VALUATIONS:
    diff1 = []
    diff2 = []
    diff = []
    val = []
    vfslopes = []
    vbslopes = []
    vqsw = []
    vsw = []
    vq = []
    alpha = 1/30
    beta = 0.6 * alpha

########

    def diff_block(self, block_num ,block_len):
        print("length=", block_num * block_len )
        list=[]
        for i in range(block_num):
            list.append(1)
            for j in range(block_len-1):
                list.append(0)
        return list

    def generate_diff(self):
        na = int(1/self.alpha)
        self.diff1 = self.diff_block(int(0.55 * na), na)
        #print("diff1:", self.diff1)
        nb = int(1 / self.beta)
        self.diff2 = self.diff_block(nb, nb)
        #print("diff2:", self.diff2)
        #self.diff = self.diff1 + self.diff2 + list(reversed(self.diff1))
        self.diff = self.diff1 + self.diff2 + self.diff1
        self.diff.append(1)
        #print("diff:", self.diff)

    def generate_val_from_diff(self):
        curr = 0
        self.val.append(curr)
        for x in self.diff:
            self.val.append(curr + x)
            curr = curr + x
        print("Length:", len(self.val), ", val[", len(self.val)-1, "]=", self.val[len(self.val)-1], ", val[", int(len(self.val)/2), "]=", self.val[int(len(self.val)/2)])
        print("val[480] = ", self.val[480], ", val[481] = ", self.val[481])
        print("val[530] = ", self.val[530], ", val[531] = ", self.val[531])
        print("val[2980] = ", self.val[2980], ", val[2981] = ", self.val[2981])
        print("val[3460] = ", self.val[3460], ", val[3461] = ", self.val[3461])
        #print("val:", self.val)
        self.is_monotone()
        self.is_subadditive()

    def generate_additive_val(self):
        self.val.append(0)
        for x in range(10):
            self.val.append(x+1)
        print("Length:", len(self.val), ", val[", len(self.val)-1, "]=", self.val[len(self.val)-1], ", val[", int(len(self.val)/2), "]=", self.val[int(len(self.val)/2)])
        #print("val:", self.val)
        self.is_monotone()
        self.is_subadditive()
        
###########

    def is_monotone(self):
        curr = self.val[0]
        for x in self.val:
            if x < curr:
                print ("val is not monotone")
                return False
            curr = x
        print("val is monotone")
        return True

    def is_subadditive(self):
        for k in range(len(self.val)):
            for j in range(k):
                if self.val[k] > self.val[j] + self.val[k - j]:
                    print("val is not sub-additive. val[", j, "]+val[", k - j, "]=", self.val[j], "+", self.val[k - j], "=", self.val[j] + self.val[k - j], "<", "val[", k,
                          "]=", self.val[k])
                    return False
        print ("val is sub-additive")
        return True


###########

    def fslope(self, k):
        max = 0
        for i in range(len(self.val) - 1 - k):
            #print("fslope: k = ", k, "i = ", i)
            tmp = (self.val[k + i + 1] - self.val[k]) / (i + 1)
            if tmp > max:
                max = tmp
        #print("fslope[", k, "] = ", max)
        return max

    def bslope(self, k):
        min = self.val[len(self.val)-1]
        for i in range(k):
            #print("bslope: k = ", k, "i = ", i)
            tmp = (self.val[k] - self.val[k-i-1]) / (i + 1)
            if tmp < min:
                min = tmp
        #print("bslope[", k, "] = ", min)
        return min

    def generate_slopes(self):
        for k in range(len(self.val)):
            if k < len(self.val)-1:
              self.vfslopes.append(self.fslope(k))
            else:
              self.vfslopes.append(0)
            if k > 0:
              self.vbslopes.append(self.bslope(k))
            else:
              self.vbslopes.append(0)
        #print("slopes:", self.vslopes)

#############

    def qsw(self, k):
        length = len(self.val)-1
        return (length - k) * (self.vfslopes[k] - self.vbslopes[length - k]) + k * (self.vfslopes[length - k] - self.vbslopes[k])
        #return (length - k) * (self.vfslopes[k]) + k * (self.vfslopes[length - k])

    def sw(self, k):
        return self.val[k] + self.val[len(self.val) - k - 1]

    def q(self, k):
        if (self.qsw(k) / self.sw(k)) < 1.4:
          print("q[", k, "] = ", self.qsw(k) / self.sw(k))
        return self.qsw(k) / self.sw(k)

############

    def generate_vectors(self):
        for k in range(len(self.val)):
            self.vqsw.append(self.qsw(k))
            self.vsw.append(self.sw(k))
            self.vq.append(self.q(k))
        #print("qsw:", self.vqsw)
        #print("sw:", self.vsw)
        #print("q:", self.vq)


###################


    def min_q(self):
        min = len(self.val) * self.val[1]
        min_index = 0
        index = 0
        for x in self.vq:
            if x < min:
                min = x
                min_index = index
            index = index + 1

        print("Minimum is obtained at ", min_index)
        print ("q=", min)
        print ("sw=", self.vsw[min_index])
        print ("qsw=", self.vqsw[min_index])



###################


    def print_val(self):
        plt.plot(self.val, label='val[k]')
        #plt.plot(self.vq, label='q[k]')
        plt.xlabel('k')
        plt.legend()
        plt.show()





valuations = VALUATIONS()
valuations.generate_diff()
print("*********************************")
valuations.generate_val_from_diff()
#valuations.generate_additive_val()
#print("*********************************")
valuations.generate_slopes()
#print("*********************************")
valuations.generate_vectors()
print("*********************************")
valuations.min_q()
valuations.print_val()
