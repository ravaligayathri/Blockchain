import hashlib
import ECC
class Node:
    def __init__(self,data):
        self.parent = None
        # self.data = data
        self.hash = data
        self.left = None
        self.right = None

    def generateHash(self,data):
        h = ECC.hash(data.encode('UTF-8'))
        return h

class MerkelTree:
    def __init__(self, listOfNodeHashes):
        self.leafNodes = listOfNodeHashes

    def setHash(self,node, hashVal):
        node.hash = hashVal

    def setParent(self, node, parent):
        node.parent = parent

    def merkelTreeCreate(self):
        # leafNodes = []

        # n1 = Node("1")
        # n1.hash = n1.generateHash(n1.data)
        # n2 = Node("2")
        # n2.hash = n1.generateHash(n2.data)
        # n3 = Node("3")
        # n3.hash = n1.generateHash(n3.data)
        # n4 = Node("4")
        # n4.hash = n1.generateHash(n4.data)
        # n5 = Node("5")
        # n5.hash = n1.generateHash(n5.data)
        # n6 = Node("6")
        # n6.hash = n1.generateHash(n6.data)

        # leafNodes.append(n1)
        # leafNodes.append(n2)
        # leafNodes.append(n3)
        # leafNodes.append(n4)
        # leafNodes.append(n5)
        # leafNodes.append(n6)


        parentList = self.leafNodes.copy()
        if (len(self.leafNodes)==1):
            return self.leafNodes[0]

        counter = 0
        counter2 = 1
        parentCount = 0
        flag = 0
        diffList = []
        while (len(self.leafNodes)!=1):
            while (counter < len(self.leafNodes)-1):
                hashChild1 = self.leafNodes[counter].hash
                hashChild2 = self.leafNodes[counter2].hash

                print("Hash of Child 1:",hashChild1)
                print("Hash of child 2:",hashChild2)
                
                diffList.append(self.leafNodes[counter])
                diffList.append(self.leafNodes[counter2])

                parentList.append(Node(hashChild1+hashChild2))
                parentHash = parentList[-1].generateHash(hashChild1+hashChild2)
                parentList[-1].left = self.leafNodes[counter]
                parentList[-1].right = self.leafNodes[counter2]
                print("Parent Hash:",parentHash)
                parentCount = parentCount + 1
                parentList[len(parentList)-1].hash = parentHash

                counter = counter + 2
                counter2 = counter2 + 2
                #leafNodes.clear()
                print("Parent Count:",parentCount)
            
            if ((len(self.leafNodes)-len(diffList))%2 == 0):
                self.leafNodes.clear()
            else:
                print("Odd number of nodes found")
                lastNode = self.leafNodes[-1]
                print("Hash of odd Node:",lastNode.hash)
                self.leafNodes.clear()
                flag = 1
            diffList.clear()

            counter = 0
            counter2 = 1

            if (flag == 0):
                self.leafNodes = parentList[len(parentList)-parentCount:]
            else:
                print("Carrying forward the last node")
                self.leafNodes.extend(parentList[len(parentList)-parentCount:])
                self.leafNodes.append(lastNode)
                # print("List of parents:",self.leafNodes)
                flag = 0
            # print("Currently in Leaf Nodes:",self.leafNodes)
            parentCount = 0
        print("Parent Hash",self.leafNodes[0].hash)

        return parentList

if __name__=="__main__":

    leafNodes = []

    #n1 = Node("Empty")
    # st = "eefrewrer"
    # hash = ECC.hash(st.encode('UTF-8'))
    # print(hash)
    n1 = Node("1")
    n1.hash = n1.generateHash(n1.hash)
    leafNodes.append(n1)
    n2 = Node("2")
    n2.hash = n2.generateHash(n2.hash)
    leafNodes.append(n2)
    n3 = Node("3")
    n3.hash = n3.generateHash(n3.hash)
    leafNodes.append(n3)
    n4 = Node("4")
    n4.hash = n4.generateHash(n4.hash)
    leafNodes.append(n4)
    n5 = Node("5")
    n5.hash = n5.generateHash(n5.hash)
    leafNodes.append(n5)
    n6 = Node("6")
    n6.hash = n6.generateHash(n6.hash)
    leafNodes.append(n6)
    n7 = Node("7")
    n7.hash = n7.generateHash(n7.hash)
    leafNodes.append(n7)
    n8 = Node("8")
    n8.hash = n8.generateHash(n8.hash)
    leafNodes.append(n8)
    n9 = Node("9")
    n9.hash = n9.generateHash(n9.hash)
    leafNodes.append(n9)
    n10 = Node("10")
    n10.hash = n10.generateHash(n10.hash)
    leafNodes.append(n10)

    print(leafNodes)

    tree = MerkelTree(leafNodes)
    p  = tree.merkelTreeCreate()


    
    #p = MerkelTree.merkelTreeCreate([1,2,3,4])

    # h1 = n1.generateHash(n1.data)
    # n1.setHash(n1,h1)
    # print("Hash1:",n1.hash)
    # n2 = Node(leafNodes[1])
    # h2 = n1.generateHash(n2.data)
    # n2.setHash(n2,h2)
    # print("Hash2:",n2.hash)
    # par = Node(n1.data+n2.data)
    # hp = par.generateHash(par.data)
    # par.setHash(par,hp)
    # print("Parent Hash:",par.hash)
    # n1.setParent(n1,par)
    # n2.setParent(n2,par)
    # print("Node1 parent:",n1.parent)
    # print("Node2 parent:", n2.parent)

    # n3 = Node(leafNodes[2])
    # h3 = n3.generateHash(n3.data)
    # n3.setHash(n3,h3)
    # print("Hash3:",n3.hash)
    # n4 = Node(leafNodes[3])
    # h4 = n4.generateHash(n4.data)
    # n4.setHash(n4,h4)
    # print("Hash4:",n2.hash)
    # par2 = Node(n3.data+n4.data)
    # hp2 = par2.generateHash(par2.data)
    # par2.setHash(par2,hp2)
    # print("Parent Hash:",par2.hash)
    # n3.setParent(n3,par2)
    # n4.setParent(n4,par2)
    # print("Node3 parent:",n3.parent)
    # print("Node4 parent:", n4.parent)

    # merkelList = []
    # merkelList.append(par)
    # merkelList.append(par2)

    # print(merkelList)