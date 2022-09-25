import copy
import numpy
import datetime

#function converts between coordinats and array indices
def convertCords(r, c):
    correctCords = (r -1, c - 1)
    return correctCords

#Class defining the state including array of rooms where 0 = clean and 1 = dirty, and vaccuum coordinates
class world:
    def __init__(self, vacLoc, grid):
        self.vacLoc = vacLoc
        self.grid = grid

    #Method to print grid of rooms
    def printWorld(self):
        for i in self.grid:
            for j in i:
                print(j, end=" ")
            print()

#Class defining the nodes for the search tree
class node:
    def __init__(self, worldState, parent, depth, pathCost, stepName):
        self.state = worldState
        self.parent = parent
        self.depth = depth
        self.pathCost = pathCost
        self.stepName = stepName

#function to instantiate the initial world based on choice of instance as described in the HW2 document
def startInstance(choice):
    grid = numpy.zeros((4,5), int)
    if(choice == 1):    #For instance 1
        w1 = world([2,2], grid)
        w1.grid[convertCords(1,2)] = 1
        w1.grid[convertCords(2,4)] = 1
        w1.grid[convertCords(3,5)] = 1
        return w1
    elif(choice == 2):  #For Instance 2
        w2 = world([3,2], grid)
        w2.grid[convertCords(1,2)] = 1
        w2.grid[convertCords(2,1)] = 1
        w2.grid[convertCords(2,4)] = 1
        w2.grid[convertCords(3,3)] = 1
        return w2
    elif(choice == 3):  # instance defined for search algorithm testing
        w3 = world([2,5], grid)
        w3.grid[convertCords(3, 5)] = 1
        w3.grid[convertCords(2, 5)] = 1
        w3.grid[convertCords(2, 4)] = 1
        return w3
    else:
        return 0

#function to expand the passed node and generate more nodes for the tree
def generateNodes(parentNode):
    newNodes = []
    generated = 0

    if(parentNode.state.vacLoc[1] != 1):    #Node generated by Left action
        lWorld = copy.deepcopy(parentNode.state)
        lWorld.vacLoc[1] -= 1
        leftNode = node(lWorld, parentNode, parentNode.depth + 1, parentNode.pathCost + 1.0, "L")
        newNodes.append(leftNode)
        generated += 1

    if(parentNode.state.vacLoc[1] != 5):    #Node generated by Right action
        rWorld = copy.deepcopy(parentNode.state)
        rWorld.vacLoc[1] += 1
        rightNode = node(rWorld, parentNode, parentNode.depth + 1, parentNode.pathCost + 0.9, "R")
        newNodes.append(rightNode)
        generated += 1

    if(parentNode.state.vacLoc[0] != 1):    #Node generated by Up action
        uWorld = copy.deepcopy(parentNode.state)
        uWorld.vacLoc[0] -= 1
        upNode = node(uWorld, parentNode, parentNode.depth + 1, parentNode.pathCost + 0.8, "U")
        newNodes.append(upNode)
        generated += 1

    if(parentNode.state.vacLoc[0] != 4):    #Node generated by Down action
        dWorld = copy.deepcopy(parentNode.state)
        dWorld.vacLoc[0] += 1
        downNode = node(dWorld, parentNode, parentNode.depth + 1, parentNode.pathCost + 0.7, "D")
        newNodes.append(downNode)
        generated += 1

    sWorld = copy.deepcopy(parentNode.state)    #Node generated by Suck action
    suckNode = node(sWorld, parentNode, parentNode.depth + 1, parentNode.pathCost + 0.6, "S")
    if(parentNode.state.grid[convertCords(parentNode.state.vacLoc[0],parentNode.state.vacLoc[1])] == 1):
        suckNode.state.grid[convertCords(suckNode.state.vacLoc[0],suckNode.state.vacLoc[1])] = 0
    newNodes.append(suckNode)
    generated += 1

    return newNodes, generated

def getDirtCount(node): #Count the number of dirty rooms
    count = 0
    for i in node.state.grid:
        for j in i:
            if j == 1:
                count += 1
    return count

def goalTest(node): #Test if all rooms are now clean
    if getDirtCount(node) == 0:
        return True
    return False

#function for running the Uniform cost Tree Search
def IDTS(initialState):
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    root = node(initialState, -1, 0, 0, "Start")
    generated = 1
    expanded = 0
    fringe = [root]
    solutionFound = False
    solutionNode = root

    limit = -1
    while(not solutionFound):   #While loop for when solution has yet to be found
        limit += 1
        fringe = [root]
        while len(fringe) != 0:
            endTime = datetime.datetime.now()
            if endTime >= startTime + datetime.timedelta(hours=1):  #If alotted time has passed
                runTime = startTime - endTime
                print("\nTime ran out, an hour has elapsed.")
                print("Run time = " + str(runTime))
                print("Reached limit = " + str(limit))
                print("Nodes generated = " + str(generated))
                print("Nodes expanded = " + str(expanded) + "\n")
                break
            currentNode = fringe.pop(0) #Remove first node from fringe
            if currentNode.depth < limit:   #if node is not at depth limit
                newNodes, newGenerated = generateNodes(currentNode) #Expand romoved node
                expanded += 1
                generated += newGenerated
                fringe.extend(newNodes) #add generated nodes to the fringe
                fringe.sort(key=lambda x: (-x.depth, x.state.vacLoc[0], x.state.vacLoc[1]))   #Sort the fringe
            if goalTest(currentNode):   #Test expanded node
                endTime = datetime.datetime.now()
                solutionNode = currentNode
                solutionFound = True
                break

    if solutionFound:   #If a solution has been found, display data
        print("A solution has been found!\n")
        solutionPath = [root]
        current = solutionNode
        while current.depth != 0:
            solutionPath.append(current)
            current = current.parent
        solutionPath.sort(key=lambda x: x.depth)
        print("Solution Path: ")    #Print solution path
        for x in solutionPath:
            print(x.stepName + "-->")
        print("Done!\n")
        runTime = endTime - startTime
        print("Run time = " + str(runTime)) #print runtime
        print("Nodes generated = " + str(generated))    #print nodes generated
        print("Nodes expanded = " + str(expanded) + "\n")   #print nodes expanded
        print("\nFinal State:")
        print("Vac Location: " + str(solutionNode.state.vacLoc))
        solutionNode.state.printWorld()



#Get instance choice from user
choice = 0
while (choice != 1) and (choice != 2) and (choice != 3):
    choice = int(input("Which instance would you like to solve for? (input 1 or 2):"))
    if choice == 1 or choice == 2 or choice == 3:
        continue
    print("\nPlease enter valid input\n")

#Instantiate world and print
w = startInstance(choice)
print("\nInitialState:")
w.printWorld()
print("Vacuum Location: %s" % (w.vacLoc,))
print("\nIterative Deepening Cost Tree Search...\n")
IDTS(w) #Run search
