# The data is provided via a class DataSimulator
import re
import DataSimulator as DSim
import ECC
import hashlib
import MerkelTree
# The object DS provides a function
# getNewData() that can be called
# repeatedly to simulate the newly
# received information


class BlockChain:
    def __init__(self):
        self.blockchain = []
        self.merkelTrees = []
        self.hashedDic = {}
    
    def addBlock(self, hashPrev, nonce, merkelRoot, merkelTree):
        newBlock = {'previousBlockHash': hashPrev, 'nonce': nonce, 'merkelRoot': merkelRoot, 'merkelTree': merkelTree}
        self.blockchain.append(newBlock)
        return newBlock
    
    def verifySignature(self, d):
        status = ECC.verify(d['pk'], d["msg"], d["signature"])
        return status
    
    def storeMerkelTree(self, merkelTree):
        self.merkelTrees.append(merkelTree)

    def createBlockchain(self):
        ds = DSim.DataSimulator()
        data = ds.getNewData()
        treeNodeList = []
        for obj in data:
            if self.verifySignature(obj) == True:
                message = str(obj['msg'])
                publicKey = str(obj['pk'])
                signature = str(obj['signature'])
                encryptionString = message + publicKey + signature
                hashedOutput = ECC.hash(encryptionString.encode('UTF-8'))
                self.hashedDic[(publicKey, message, signature)] = hashedOutput
                print("Verification Passed!")
                treeNodeList.append(MerkelTree.Node(hashedOutput))
            else:
                print("Verification Failed!")
        mTree = MerkelTree.MerkelTree(treeNodeList)
        treeNodes = mTree.merkelTreeCreate()
        block.storeMerkelTree(treeNodes)
        rootofMerkel = treeNodes[-1]
        block.addBlock("00000000000000000000000000000000", "0", rootofMerkel, mTree)
        print(block.blockchain[0]['merkelRoot'].hash)
        print(len(block.blockchain))
        print(self.hashedDic)

    def proofOfWork(self, msg):
        for key, value in self.hashedDic.items():
            (publicKey, message, signature) = key
            if message == msg:
                print(value)

    # def generateHash(self):
    #     key = hashlib.sha256()
    #     key.update(str(self.blockchain[0]['prevHash']).encode())
    #     key.update(str(self.blockchain[0]['data']['msg']).encode())
    #     key.update(str(self.blockchain[0]['data']['pk']).encode())
    #     key.update(str(self.blockchain[0]['data']['signature']).encode())
    #     key.update(str(self.blockchain[0]['merkelRoot']).encode())
    #     hash = key.hexdigest()
    #     print(hash)
    #     return hash

    # def generateHashForMerkel(self,JsonOb):
    #     key = hashlib.sha256()
    #     key.update(str(self.blockchain[0]['data']['msg']).encode())
    #     key.update(str(self.blockchain[0]['data']['pk']).encode())
    #     key.update(str(self.blockchain[0]['data']['signature']).encode())
    #     hash = key.hexdigest()
    #     print(hash)
    #     return hash


if __name__ == "__main__":
    block = BlockChain()
    block.createBlockchain()
    block.proofOfWork("94 dead in china earthquake")
    # ha = ""
    # i = 0
    # while(not (re.match(r'(000[0])',str(ha)))):
    #     h = "24b9c4a8638cefab569d1bc14915f6d4" + "00000000000000000000000000000000" + str(i)
    #     i = i + 1
    #     ha = ECC.hash(h.encode('UTF-8'))
    # print(i)
    # print(ha)



























#
# This is list of dict types, each of them of the form
# {
#     "msg"       : str         # the message
#     "pk"        : str         # the public key
#     "signature" : [int, int]  # the ECC signature (a point on the curve)
# }
# the public key pk is given as readable list of parameters
# Curve( 463 -2 2 ); G( 155 452 ); PK( 424 5 ); PKOrder( 149 )
# Thus, the curve is
# x^3 -2x + 2 % 463 == y^2 % 463
# with
#  - a base point G=(155, 452),
#  - public key point P=(424, 5) and
#  - the order of the sub-group induced by G is 149, i.e. 149*G = (0,0)


# Let's look at a single element of the received data

#d = newData[20]
#print d
#
## To verify the signature, we need to import the ECC module for actual curve operations
#
#import ECC
#
## Let's check whether this signature is correct. The verify function is
##
##   ECC.verify(pubKeyString, message, signature)
##
## hence we call it with the public key string d['pk'], the message and the signature
#
#print ECC.verify(d['pk'], d["msg"], d["signature"])
## True
#
## Or, if we write down the parameters explicitly
#print ECC.verify(d['pk'], "cabinet meets to balance budget priorities", (9,30))
## True
#
#
## Thus evaluates to True. If we change the message a bit (cabinet -> Cabinet), we get
#print ECC.verify(d['pk'], "Cabinet meets to balance budget priorities", (9,30))
## False
#
## And finally, for the Merkle Tree
## of all valid entries, we need to
## be able to hash an element. We
## use the str function, provided
## by Python
#
#print (str(d))
## -> "{u'msg': u'cabinet meets to balance budget priorities', u'pk': u'Curve( 463 -2 2 ); G( 155 452 ); PK( 263 231 ); PKOrder( 149 )', u'signature': [9, 30]}"
#
#
## And this string can be given to ECC.hash(s)
#
#print ECC.hash(str(d))

