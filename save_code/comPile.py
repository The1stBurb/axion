pile=[
    ["0","5","4",")",],
    ["1","2","3","(",],
    ["9","6","[","]",],
    ["8","7",","," ",],
    ["","","","",]
]
def inPile(digit):
    global pile
    for y,i in enumerate(pile):
        for x,j in enumerate(i):
            if j==digit:
                return "0"+str(y)+str(x)
    return "040"
def comPile(txt):
    if not isinstance(txt,str):
        txt=str(txt)
    compiled=""
    for digit in txt:
        compiled+=inPile(digit)
    return compiled
def decomPile(txt):
    global pile
    chunks=[]
    for i in range(len(txt)//3):
        chunks.append(txt[i*3:(i+1)*3])
    decompiled=""
    for chnk in chunks:
        dig1,dig2,dig3=int(chnk[0]),int(chnk[1]),int(chnk[2])
        decompiled+=pile[dig2][dig3]
    return decompiled
def runPiler(txt=""):
    if txt=="":
        saved=""
        with open("save_code/save.pile","r") as save:
            saved=save.read()
        return decomPile(saved)
    else:
        save2=comPile(txt)
        with open("save_code/save.pile","w")as save:
            save.write(save2)
# print(runPiler())#"[0, (1360, 560)]")
    