# Authors
# Gayathri Hanuma Ravali Kuppachi - 012557064
# Gayatri Milind Hungund - 013738426
# Parth Bhadreshkumar Patel - 013705718

import DataSimulator as DSim
import ECC
from collections import OrderedDict
import re

'''
Datastructure for Block Chain
'''
class Block:
    def __init__(self):
        self.prev_hash = "00000000000000000000000000000000"
        self.merkle_root = ""
        self.nonce = "0"


'''
Creating a blockchain
'''
class Blockchain:

    def __init__(self):
        self.list_merkletree = OrderedDict()
        self.leaves_list = []
        self.block = Block()

    '''
    Method to return list of merkle trees
    '''
    def get_merkle_list(self):
        return self.list_merkletree

    ''' Creating leaf nodes for Merkle Tree
        Verify if valid signature.
        If True, start building leaf nodes for Merkle Tree    
    '''
    def insertMerkleData(self, newData):
        leaves_list = self.leaves_list
        for i in range(len(newData)):
            data = newData[i]
            verify_flag = ECC.verify(data['pk'], data["msg"], data["signature"])
            if (verify_flag == True):
                d = str(data)
                leaves_list.append(str(d))

        return leaves_list

    '''
    Method to construct Merkle Tree.
    Compare leaf with its adjacent node and make them left child and right child
    If both are present hash the value of left and right child else only hash the value 
    of left child if there is no right child present.
    Store message as key and its hash as value in an orderedDictionary. Do this recursively. 
    For ex: second level of merkle tree will have hash(A)+hash(B)
    as key and hash(hash(A)+hash(B)) as its value if A, B are leaf nodes of merkle tree. 
    This helps in keeping track of hashes and is useful for proof of work.
    Recursively call method until there is only one element left which will be root of the Merkle Tree.
    '''
    def buildMerkle(self, leaves_list):

        list_merkletree = self.list_merkletree
        temp_tree = []
        for i in range(0, len(leaves_list), 2):
            left_child = leaves_list[i]
            if i + 1 != len(leaves_list):
                right_child = leaves_list[i + 1]
            else:
                right_child = ''

            leftchild_hash = ECC.hash(str(left_child).encode())

            if right_child != '':
                rightchild_hash = ECC.hash(str(right_child).encode())

            list_merkletree[leaves_list[i]] = leftchild_hash
            if right_child != '':
                list_merkletree[leaves_list[i + 1]] = rightchild_hash

            if right_child != '':
                temp_tree.append(leftchild_hash + rightchild_hash)

            else:
                temp_tree.append(leftchild_hash)

        if len(leaves_list) != 1:
            self.leaves_list = temp_tree
            self.list_merkletree = list_merkletree
            self.buildMerkle(temp_tree)

    '''
    Method to add blocks into the blockchain.
    Keep incrementing nonce by checking if hash value of previous hash , nonce and merkle root combined starts with 0000.
    Once condition is satisfied, nonce is generated and use this hash value as prev hash for the next block to be added.
    Returning entire block object to the main blockchain calling function 
    '''
    def addBlock(self, merkle_root, previ_hash):
        print("\nPrevioushash==", previ_hash)
        print("Merkle root===", merkle_root)

        block_hash = ""
        nonce_b = 0
        while (not (re.match(r'(000[0])', str(block_hash)))):
            h = str(previ_hash) + str(merkle_root) + str(nonce_b)
            block_hash = ECC.hash(h.encode())
            nonce_b = nonce_b + 1

        print("Nonce===", nonce_b)
        print("block hash===", block_hash, "\n")

        b = Block()
        b.prev_hash = block_hash
        b.merkle_root = merkle_root
        b.nonce = nonce_b

        return b

    '''
    Method to generate proof of work.
    Accepts message headline as input and merkle tree dictionary.
    Traverses through the dictionary and displays the entire path to reach the headline in each block 
    and returns the block path containing the message
    '''
    def proof_of_work(self, msg_headline, merkle_trees_dic):
        root_element = ""
        root_list = []
        tree_traversal = []
        hash_value_message = ""
        hash_value = ""
        print("\n##################### Proof of Work #####################")
        for key, nested_tree_list in merkle_trees_dic.items():
            for nested_key, nested_val in nested_tree_list.items():
                if msg_headline in nested_key:
                    print("Headline Found: ", nested_key, " Tuple hash: ", nested_val)
                    hash_value_message = nested_tree_list[nested_key]
                    hash_value = hash_value_message
                    #print("Hash value::::", hash_value)
        tree_traversal.append(hash_value)
        for key, nested_tree_list in merkle_trees_dic.items():
            for nested_key, nested_val in nested_tree_list.items():
                if (hash_value in nested_key):
                    tree_traversal.append(nested_val)
                    #print(tree_traversal)
                    hash_value = nested_val
        return tree_traversal

    '''
    Helper method to display path from Merkle root to message in a block
    '''
    def printTraversal(self, tree_traversal_list,list_blocks):
        reversed_list = tree_traversal_list[::-1]
        blocknumber=""
        for i in range(len(list_blocks)):
            if list_blocks[i]["merkle_root"]==reversed_list[0]:
                blocknumber=i
        print("\nFollowing is the traversal path from Merkle root to leaf node found in Block ", blocknumber)
        for i in range(len(tree_traversal_list)):
            print(reversed_list[i])

'''
Main method which facilitates creation of blockchain
Number of blocks is configurable.
Use getNewData to generate new data for every block, then generate a merkle tree
Call addblock method which generates nonce and creates a data structure for the block
Block is returned and stored in a list of blocks which is later used for proof of work
'''
if __name__ == "__main__":

    num_blocks = 5
    merkle_trees = {}
    list_blocks = []
    ds = DSim.DataSimulator()
    oldprevhash = "00000000000000000000000000000000"
    print("\n##################### Creating Blockchain #####################")
    for i in range(0, num_blocks):
        data = ds.getNewData()
        blockchain = Blockchain()
        leaves_data = blockchain.insertMerkleData(data)
        blockchain.buildMerkle(leaves_data)
        list_trees = blockchain.get_merkle_list()
        merkle_root = next(reversed(list_trees.values()))
        merkle_trees[merkle_root] = list_trees
        print("\n##################### Block ", i, "#####################")
        block = blockchain.addBlock(merkle_root, oldprevhash)
        block_dict = dict()
        block_dict["merkle_root"] = block.merkle_root
        block_dict["prev_hash"] = block.prev_hash
        block_dict["nonce"] = block.nonce
        oldprevhash = block.prev_hash
        list_blocks.append(block_dict)

    '''
    Call Proof of work function.

    '''
    blockchainObj = Blockchain()
    msg_headline = "cabinet meets to balance budget priorities"
    node_list = blockchainObj.proof_of_work(msg_headline, merkle_trees)
    blockchainObj.printTraversal(node_list,list_blocks)
