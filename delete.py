class temp:
    def __init__(self, hih):
        self.hih = hih

    def lele(self, kik, mode=5):
        self.hih["5"] = 10
    
hih = {}
hih["5"] = 5
t =temp(hih)
t.lele(hih, 5)
print(hih["5"])