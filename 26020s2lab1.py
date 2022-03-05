import sys
import re

global reordered

if(len(sys.argv) < 3):
    print("Not enough arguments to proceed.")
    exit()

# We use regular expression to validate input lines, prevent errors
pattern = "^(\d+)(\s(\d+))+[^\D]"

# Define 26 colors scheme
colors = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

try:
    # Open the input file and read all lines, do the splition
    global reordered
    with open(sys.argv[1], "r") as f:
        temp = f.readlines()

        # Create interference graph by using list representation, it is a 2-d array because it will store each separate dependency number for each line
        interference_list = []
        for i in range(len(temp)):
            if(re.search(pattern, temp[i])):
                # Replace useless newline char and split by a space, then put it into the interference_list list
                interference_list.append(temp[i].replace("\n", "").split(" "))

        # "reordered" list is used to store the results after appending the number of neighbours for each register
        reordered = []
        for i in range(len(interference_list)):
            interference_list[i].insert(0,len(interference_list[i])-1)
            reordered.append(interference_list[i])

        # Sort this list according to the first param of each list, which is the number of neighbours, in reverse order
        reordered.sort(reverse=True)

        f.close()

        # Create a list "colored", which is used to record the current used colors for each register and provide a basis of generating the results
        colored = [None]*len(reordered)

        # Checking the same numbered neighbours of elements and adjust to the correct order
        for i in range(len(reordered)):
            for j in range(len(reordered)):
                # Ensure we only change once per pair, not undo our efforts
                if(j > i):
                    # If the number of neighbours are the same from the same element, since we have ordered the number, 
                    # we can just interchange them if the first id > the second id
                    if(reordered[i][0] == reordered[j][0]):
                        if(reordered[i][1] != reordered[j][1]):
                            if(int(reordered[i][1]) > int(reordered[j][1])):
                                # Enforcing lowest id takes priority
                                temp = reordered[i]
                                reordered[i] = reordered[j]
                                reordered[j] = temp

        # Main coloring logic
        for i in range(len(reordered)):
            # Each time run through each list of "reordered", adding each neighbour's color to the "neighbor_list"
            # Then check from the first color "A", check whether it is in the neighbor_list, if it is, check another color, until after color #26
            # if the color has not been used, simply record this information with node number into "colored", and break it (jump out the loop)
            neighbor_list = []
            for j in range(2,len(reordered[i])):
                neighbor_list.append(colored[int(reordered[i][j])-1])
            for k in range(len(colors)):
                if(colors[k] not in neighbor_list):
                    colored[int(reordered[i][1])-1] = colors[k]
                    break
                else:
                    if(k == 26):
                        print("Registers are used out!")
                        exit(0)

        # Writing to a file
        with open(sys.argv[2],'w') as f:
            for i in range(len(colored)):
                if(i != len(colored)-1):
                    f.write(str(i+1)+colored[i]+'\n')
                else:
                    # Last line has no newline character
                    f.write(str(i+1)+colored[i])
            f.close()

        print("Writing Done!")

except Exception as e:
    print("File failed to open/write or other problem(s) occurred. Because", e)
    exit()