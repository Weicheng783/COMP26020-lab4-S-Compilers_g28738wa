import sys
import re

global reordered

if(len(sys.argv) < 3):
    print("Not enough arguments to proceed.")
    exit()

pattern = "^(\d+)(\s(\d+))+[^\D]"

# Define 26 colors scheme
colors = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# Open the input file and read all lines, do the splition
try:
    global reordered
    with open(sys.argv[1], "r") as f:
        temp = f.readlines()
        # print(interference)
        interference_list = []

        for i in range(len(temp)):
            # print(temp[i], re.search(pattern, temp[i]))
            if(re.search(pattern, temp[i])):
                interference_list.append(temp[i].replace("\n", "").split(" "))

        reordered = []
        for i in range(len(interference_list)):
            interference_list[i].insert(0,len(interference_list[i])-1)
            reordered.append(interference_list[i])

        reordered.sort(reverse=True)

        # print("interference_list", interference_list)
        # print("reordered", reordered)

        f.close()

        colored = [None]*len(reordered)

        # Checking the same numbered elements and adjust to the correct order

        for i in range(len(reordered)):
            for j in range(len(reordered)):
                if(j > i):
                    if(reordered[i][0] == reordered[j][0]):
                        if(reordered[i][1] != reordered[j][1]):
                            if(int(reordered[i][1]) > int(reordered[j][1])):
                                # Enforcing lowest id takes priority
                                # print(reordered)
                                temp = reordered[i]
                                reordered[i] = reordered[j]
                                reordered[j] = temp
                                # print(reordered)
                                # room.append(reordered)

        # print("reordered, now", reordered)

        # Main coloring logic
        # print("colored, before", colored)

        for i in range(len(reordered)):
            # color_picker = 0
            neighbor_list = []
            for j in range(2,len(reordered[i])):
                neighbor_list.append(colored[int(reordered[i][j])-1])
            for k in range(len(colors)):
                if(colors[k] not in neighbor_list):
                    # print(int(reordered[i][1])-1)
                    colored[int(reordered[i][1])-1] = colors[k]
                    break
                else:
                    if(k == 26):
                        print("Registers are used out!")
                        exit(0)

        # print("colored, after", colored)

        # Writing to a file
        with open(sys.argv[2],'w') as f:
            for i in range(len(colored)):
                if(i != len(colored)-1):
                    f.write(str(i+1)+colored[i]+'\n')
                else:
                    f.write(str(i+1)+colored[i])
            f.close()

        print("Writing Done!")


except Exception as e:
    print("File failed to open/write or other problem(s) occurred. Because", e)
    exit()