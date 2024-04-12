from os import listdir, mkdir
from os.path import isdir

print("#######################################################")
print("#             Matinf compiler                         #")
print("#######################################################")
print("Welcome to Matinf Compiler v0.3")

symbols = ["=", ":", "\"","{", "}"]
keyword = ["def", "case", "match","Int","String","Double","List","if","then","else"]

def colorCode(code):
    codeArr = code.split('<div class="code">')
    out = ""
    if len(codeArr) > 1 :
        out = codeArr[0]
        for c in range(1, len(codeArr)):
            out += '<div class="code">'
            curCode = codeArr[c].split("</div>")
            wordArr = curCode[0].split(" ")
            for w in wordArr :
                if w in keyword :
                    out += '<label class="keyword">'+w+"</label>"
                else :
                    chars = [*w]
                    for c in chars :
                        if c in symbols :
                            out += '<label class="punctuation">'+c+"</label>"
                        else :
                            out += c
                out += " "
            out += "</div>"+curCode[1]
        return out


def compile(path, workspace, activePath):
    na = path.split("/")
    fullNa = na[len(na)-1].split(".")[0]
    print(fullNa)
    out = ""
    f1 = open(path, "r")
    f = open(workspace+"/"+fullNa+".html", "w")
    out += "<html><head><title>"+fullNa+'</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"><link href="file://'+activePath+'/style.css" rel="stylesheet" type="text/css" /></head><body>'
    chars = [*f1.read()]
    isPTitle = False
    isTitle = 0
    isCode = False
    for c in chars :
        if isPTitle :
            if c == "1":
                isTitle = 1
                out += "<h1>"
            elif c == "2":
                isTitle = 2
                out += "<h2>"
            elif c == "3" :
                isTitle = 3
                out += "<h3>"
            else :
                out+=c
            isPTitle = False
        elif c == "<":
            isPTitle = True
        elif c == "\n" :
            if isTitle == 1 :
                out += "</h1>"
            elif isTitle == 2 :
                out += "</h2>"
            elif isTitle == 3 :
                out += "</h3>"
            else :
                out += "<br>"
            isTitle = 0
        elif c == "§" :
            if not isCode :
                isCode = True
                out += '<div class="code">'
            else :
                isCode = False
                out += "</div>"
        else :
            out += c
    out += "<script>MathJax = {tex: {inlineMath: ['$', '$']}};</script><script id=\"MathJax-script\" async src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js\"></script></body></html>"
    coloredText = colorCode(out)
    f.write(coloredText)
    f.close()
    f1.close()

def raiseErr(message):
    print("\033[31m" + message+ "\033[31m" )

def createWorkspace(curPath):
    print("What is the name of the new workspace ?")
    nW = str(input(""))
    mkdir(curPath+"/"+nW)
    return curPath+"/"+nW


def chooseWorkspace(path):
    dirs = listdir(path)
    for fol in range(len(dirs)) :
        print(str(fol)+". " + str(dirs[fol])) 
    print("a. append workspace")
    print("Which workpace to choose ?")
    res = str(input(""))
    for fol in range(len(dirs)) :
        if res == str(fol) :
            return path+"/"+dirs[fol]
    if res == "a" :
        return createWorkspace(path)
    else :
        raiseErr("Invalid choose")
        chooseWorkspace(path)

def chooseFileToComile(path):
    dirs = listdir(path)
    for fol in range(len(dirs)) :
        splited = dirs[fol].split(".")
        if len(splited) > 1 :
            if splited[1] == "mip" : 
                print(str(fol)+". " + str(dirs[fol]))
    print("Which file to compile ?")
    res = str(input("")) 
    for fol in range(len(dirs)) :
        splited = dirs[fol].split(".")
        if len(splited) > 1 :
            if splited[1] == "mip" : 
                if res == str(fol) :
                    return path+"/"+dirs[fol]
    raiseErr("Invalid choose")
    chooseFileToComile(path)
    
try :
    global wPath
    f = open("meta.datapy","r")
    wPath = f.read()
    f.close()
    
except :
    f = open("meta.datapy", "w")
    print("No metadata found")
    print("Please enter the path where the compiler have to work")
    pa = str(input(""))
    f.write(pa)
    f.close()

try :
    global nPath, fPath
    nPath = chooseWorkspace(wPath)
    fPath = chooseFileToComile(nPath)
except :
    raiseErr("Current path is invalid")
    f = open("meta.datapy", "w")
    print("No metadata found")
    print("Please enter the path where the compiler have to work")
    pa = str(input(""))
    f.write(pa)
    f.close()
compile(fPath, nPath, wPath)