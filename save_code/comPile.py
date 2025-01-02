pile=[
    ["0","5","4",")","e","z","",],
    ["1","2","3","(","f","y",],
    ["9","6","[","]","g","x",],
    ["8","7",","," ","h","w",],
    ["a","b","c","d","i","v",],
    ["n","m","l","k","j","u",],
    ["o","p","q","r","s","t",],
]
def inPile(digit):
    global pile
    for y,i in enumerate(pile):
        for x,j in enumerate(i):
            if j==digit.lower():
                return ("0"if digit.lower()==digit else "1")+str(y)+str(x)
    return "006"
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
        decompiled+=(pile[dig2][dig3]if dig1==0 else pile[dig2][dig3].upper())
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
# print(runPiler())#"[0, (1360, None)]"))
# runPiler([4,(None,None),[]])
    