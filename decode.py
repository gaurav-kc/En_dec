# find this project at https://github.com/gaurav-kc/Enc_dec

# only 1 argument. The name of directory which has encrypted files

with open("temp.lol", "rb") as image:
    f = image.read()
    b = bytearray(f)
imgcount = bytearray()
for i in range(0,4):
    imgcount.append(b[i])

imgcount = int.from_bytes(imgcount, byteorder='little')
print(imgcount)
index = 4
sizes = []
for i in range(0,imgcount):
    count = 4
    temp = bytearray()
    while count:
        count = count - 1
        temp.append(b[index])
        index = index + 1
    temp = int.from_bytes(temp, byteorder='little')
    print(temp)
    sizes.append(temp)

filecount = 0
for i in range(0,imgcount):
    filename = "file_" + str(filecount) + ".png"
    currsize = sizes[filecount]
    filecount = filecount + 1
    tempimg = bytearray()
    while currsize:
        currsize = currsize - 1
        b[index] = (b[index] + 200)%256
        tempimg.append(b[index])
        index = index + 1
    f = open(filename,"wb")
    f.write(tempimg)
    f.close()
# f = open("original.png","wb")
# for i in range(0, len(b)):
#     b[i] = (b[i] + 200)%256
# f.write(b)
