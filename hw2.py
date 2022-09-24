import numpy

#function converts between coordinats and array indices
def convertCords(r, c):
    correctCords = (r -1, c - 1)
    return correctCords

#Class defining the state including array of rooms where 0 = clean and 1 = dirty, and vaccuum coordinates
class world:
    def __init__(self, vacLoc, grid):
        self.vacLoc = vacLoc
        self.grid = grid

    def printWorld(self):
        for i in self.grid:
            for j in i:
                print(j, end=" ")
            print()

#function to instantiate the initial world based on choice of instance as described in the HW2 document
def startInstance(choice):
    grid = numpy.zeros((4,5), int)
    if(choice == 1):
        w1 = world((2,2), grid)
        w1.grid[convertCords(1,2)] = 1
        w1.grid[convertCords(2,4)] = 1
        w1.grid[convertCords(3,5)] = 1
        return w1
    elif(choice == 2):
        w2 = world((3,2), grid)
        w2.grid[convertCords(1,2)] = 1
        w2.grid[convertCords(2,1)] = 1
        w2.grid[convertCords(2,4)] = 1
        w2.grid[convertCords(3,3)] = 1
        return w2
    else:
        return 0

#Get instance choice from user
choice = 0
while (choice != 1) and (choice != 2):
    choice = int(input("Which instance would you like to solve for? (input 1 or 2):"))
    if choice == 1 or choice == 2:
        continue
    print("\nPlease enter valid input\n")

#Instantiate world and print
w = startInstance(choice)
print("\n")
w.printWorld()
print("Vacuum Location: %s" % (w.vacLoc,))


        
        



