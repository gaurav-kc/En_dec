# find recent code at 
# first argument is the input directory name 
# second argument is the output directory name 
# adding a comment 222
# comment from git
with open("Screenshot from 2020-11-28 15-55-25.png", "rb") as image:
    f1 = image.read()
    b1 = bytearray(f1)
with open("Screenshot from 2020-11-28 15-56-22.png", "rb") as image:
    f2 = image.read()
    b2 = bytearray(f2)

imgcount = 2 
len1 = int(len(b1))
len2 = int(len(b2))
print(len1)
print(len2)
len1 = len1.to_bytes(4,'little')
len2 = len2.to_bytes(4,'little')
imgcount = imgcount.to_bytes(4,'little')

f = open("temp.lol","wb")

for i in range(0, len(b1)):
    b1[i] = (b1[i] + 56)%256
for i in range(0, len(b2)):
    b2[i] = (b2[i] + 56)%256

final = imgcount + len1 + len2 + b1 + b2
f.write(final)
