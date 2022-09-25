

M =[[0,0,0],
    [0,0,1],
    [0,1,1]]

for i in range(len(M)):
    for j in range(len(M[i])):
        if M[i][j] == 1:
            for y in range(len(M[i])):
                M[i][y] = 1
            for x in range(len(M[j])):
                M[x][j] = 1

print(M)
