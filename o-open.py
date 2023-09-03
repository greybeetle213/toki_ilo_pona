import http.server # some of the js code needed for debugging wont work unless the file is hosted on a server
from sys import argv
import re
port = 8000
server_address = ('127.0.0.1', port)
path = argv[1]
try:
    tokiiloRAW = open(path, "r")
except:
    print("mi ken ala open e lipu "+path+". ken la ona li lon ala.")
    exit()
tokiilo = tokiiloRAW.read().replace("	", "")
tokiiloRAW.close()
##print(tokiilo)
tokiilo = tokiilo.split("\n")
js = []
## the numbers mean to insert the item from that posintion in the input to there.
functions = {
    "nimilipu": [["nimilipu", 'any'], ['document.title = ', 1]],
    "sitelentoki": [["sitelentoki", 'any', 'num', 'num'], ["sitelentoki(", 1, ", ", 2, ", ", 3, ")"]],
    "leko": [["leko", "num", "num", "num", "num"], ["leko(", 1, ", ", 2, ", ", 3, ", ", 4, ")"]],
    "kule": [["kule", "num", "num", "num"],["kule(", 1, ",", 2, ",", 3, ")"]],
    "nena": [["nena", "any"],["nena(", 1, ")"]],
    "nasinnanpa": [["nasinnanpa", "any"], ["TokiPonaToBase10(", 1, ")"]],
    "nasintoki": [["nasintoki", "any"], ["Base10ToTokiPona(", 1, ")"]],
    "nasintokitannanpakipisi": [["nasintokitannanpakipisi", "any", "str"], ["Base10ToTokiPonaFloat(", 1, ", ", 2, ")"]],
    "nasinnanpatannanpakipisi": [["nasinnanpatannanpakipisi", "any", "str"],["TokiPonaToBase10Float(", 1, ", ", 2, ")"]],
    "nanpapikipisiala": [["nanpapikipisiala", "num"], ["Math.round(",1,")"]],
    "nanpalilipikipisiala": [["nanpalilipikipisiala", "num"], ["Math.floor(",1,")"]],
    "nanpasulipikipisiala": [["nanpasulipikipisiala", "num"], ["Math.ceil(",1,")"]],
    "nasinOPENBRACKETsin_CLOSEBRACKET": [["nasinOPENBRACKETsin_CLOSEBRACKET", "num"], ["Math.sin(",1,")"]],
    "nasinOPENBRACKETko_CLOSEBRACKET": [["nasinOPENBRACKETko_CLOSEBRACKET", "num"], ["Math.cos(",1,")"]],
    "nasinOPENBRACKETtan_CLOSEBRACKET": [["nasinOPENBRACKETtan_CLOSEBRACKET", "num"], ["Math.tan(",1,")"]],
    "nasinwekapinasinOPENBRACKETsin_CLOSEBRACKET": [["nasinwekapinasinOPENBRACKETsin_CLOSEBRACKET", "num"], ["Math.asin(",1,")"]],
    "nasinwekapinasinOPENBRACKETko_CLOSEBRACKET": [["nasinwekapinasinOPENBRACKETko_CLOSEBRACKET", "num"], ["Math.acos(",1,")"]],
    "nasinwekapinasinOPENBRACKETtan_CLOSEBRACKET": [["nasinwekapinasinOPENBRACKETtan_CLOSEBRACKET", "num"], ["Math.atan(",1,")"]],
    "nanpasike": [["nanpasike"], ["Math.PI"]],
    "pana": [["pana", "any"], ["return(", 1, ")"]],
    "suli": [["suli", "any"], [1, ".length"]],
    "sulitawasitelen": [["sulitawasitelen", "str"], ["ctx$.measureText(", 1, ").actualBoundingBoxRight"]],
    "sitelen": [["sitelen", "str", "num", "num"],["sitelen(", 1, ", ", 2, ", ", 3, ")"]],
    "kalama": [["kalama", "str"], ["kalama(", 1, ")"]],
    "kalamalontenposama": [["kalamalontenposama", "str"], ["kalamalontenposama(", 1, ")"]],
    "sonaawen": [["sonaawen", "str"],["readCookie(", 1, ")"]],
    "sonaawensin": [["sonaawensin", "str", "str"], ["saveCookie(", 1, ", ", 2, ")"]],
    "nanpatannasa": [["nanpatannasa"],["Math.random()"]],
    "nanpasemepikulupuona": [["nanpasemepikulupuona", "num"], ["Math.sqrt(", 1, ")"]],
    "wekatankulupu": [["wekatankulupu", "any" , "num"], [1, ".splice(", 2, ", 1)"]],
    "linja": [["linja", "num", "num", "num", "num", "num"], ["linja(",1 ,", ", 2, ", ", 3, ", ", 4, ", ", 5, ")"]],
    "sike": [["sike", "num", "num", "num"], ["sike(",1 ,", ", 2, ", ", 3, ")"]],
    "tokipiwekaala": [["tokipiwekaala", "str"], [1, ".replaceAll(' ', '')"]]
}
reservedWords = ["tokipiwekaala", "pikulupu", "lilon", "tankipisi", "weka", "nanpasemepikulupuona", "sonaawen", "sonaawensin", "nanpatannasa", "suli", "pana", "nanpasulipikipisiala", "nanpalilipikipisiala", "nanpapikipisiala", "antela", "nasinnanpa", "nimilipu", "nanpa", "sitelentoki", "li", "lipokie", "lipokikine", "likulupue", "likulupukine", "sikela", "pokipitokiilo", "la", "pini", "anu", "lililitawa", "lisulitawa", "lisama", "lisamaala" "te", "to", "kulupu", "e", "kule", "leko"]
te = False
kulupuAmmount = 0
sikeExists = False
firstteList = False
firstte = False
teFunction = False
nanpa = False
functionToken = False
functionTokens = []
lineNumbers = [] # this varible is used to know what line to display when an error is thrown in the js

def Base10ToTokiPona(base10num):
    if not isinstance(base10num, (int, float)) or isinstance(base10num, bool):
        return "nanpapakala"
    if base10num % 1 != 0:
        raise ValueError("CONVERSIONFLOATERROR")
    tokiPonaNumber = ""
    if base10num < 0:
        tokiPonaNumber += "weka"
        base10num *= -1
    if base10num == 0:
        return "ala"
    endOfNumber = str(base10num)
    if len(endOfNumber) % 2 == 0:
        alisNeeded = len(endOfNumber) / 2 - 1
        base10num = int(endOfNumber[:2])
        endOfNumber = endOfNumber[2:]
    else:
        tempnum = int(endOfNumber[0])
        endOfNumber = str(base10num)[1:]
        while tempnum > 0:
            if tempnum >= 20:
                tempnum -= 20
                tokiPonaNumber += "mute"
            elif tempnum >= 5:
                tempnum -= 5
                tokiPonaNumber += "luka"
            elif tempnum >= 2:
                tempnum -= 2
                tokiPonaNumber += "tu"
            elif tempnum >= 1:
                tempnum -= 1
                tokiPonaNumber += "wan"
        if base10num >= 100:
            tokiPonaNumber += "ali"
        alisNeeded = len(str(base10num)[1:]) / 2 - 1
        if str(base10num)[1:] != "":
            base10num = int(str(base10num)[1:])
        else:
            base10num = 0
        if alisNeeded < 0:
            alisNeeded = 0
        if endOfNumber[:2] == "":
            base10num = 0
        else:
            base10num = int(endOfNumber[:2])
        endOfNumber = endOfNumber[2:]
    while base10num > 0 or len(endOfNumber) > 0 or alisNeeded > 0:
        while base10num > 0:
            if base10num >= 20:
                base10num -= 20
                tokiPonaNumber += "mute"
            elif base10num >= 5:
                base10num -= 5
                tokiPonaNumber += "luka"
            elif base10num >= 2:
                base10num -= 2
                tokiPonaNumber += "tu"
            elif base10num >= 1:
                base10num -= 1
                tokiPonaNumber += "wan"
        if alisNeeded > 0:
            alisNeeded -= 1
            if endOfNumber[:2] == "":
                base10num = 0
            else:
                base10num = int(endOfNumber[:2])
            endOfNumber = endOfNumber[2:]
            tokiPonaNumber += "ali"
    return tokiPonaNumber

def toki_pona_to_base_10(tpnum):
    tpnum = tpnum.replace(" ", "")
    base_ten_number = 0
    weka = False

    if tpnum[:4] == "weka":
        weka = True
        tpnum = tpnum[4:]

    if tpnum == "ala":
        return 0

    while len(tpnum) > 0:
        if tpnum.startswith("a"):
            tpnum = tpnum[3:]
            base_ten_number *= 100
        elif tpnum.startswith("m"):
            tpnum = tpnum[4:]
            base_ten_number += 20
        elif tpnum.startswith("l"):
            tpnum = tpnum[4:]
            base_ten_number += 5
        elif tpnum.startswith("t"):
            tpnum = tpnum[2:]
            base_ten_number += 2
        elif tpnum.startswith("w"):
            tpnum = tpnum[3:]
            base_ten_number += 1

    if weka:
        base_ten_number *= -1

    return base_ten_number
def checkNumber(number):
    if number == "":
        return False
    if number[:4] == "weka":
        number = number[4:]
    if number == "ala":
        return True
    while number != "":
        if number[:3] == "ali" or number[:3] == "ale":
            number = number[3:]
        elif number[:4] == "mute":
            number = number[4:]
        elif number[:4] == "luka":
            number = number[4:]
        elif number[:2] == "tu":
            number = number[2:]
        elif number[:3] == "wan":
            number = number[3:]
        else:
            return False
    return True
def checkSyntax(line_number, syntax, line):
    if len(line) != len(syntax):
        raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\ntoki ni li wile e ijo pi mute ante. ona o kepeken nasin ni:"+"  ".join(syntax))
    for i in range(0, len(line)):
        if syntax[i] == 'any':
            if line[i] in reservedWords:
                raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\npoki pi toki ilo li ken ala kepeken nimi ni: "+line[i])
        elif syntax[i] == 'num':
            if '"' in line[i] or line[i] in reservedWords:
                raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken nanpa taso: "+line[i])
        elif syntax [i] == "str":
            if checkNumber(line[i]):
                raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken sitelen taso"+line[i])
        elif syntax[i] == 'var' or line[i] in reservedWords:
            if '"' in line[i] or checkNumber(line[i]):
                raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken poki taso: "+line[i])
        elif syntax[i] != line[i]:
            raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\ntoki ni o kepeken nasin ni:"+"  ".join(syntax))
def convertFunctionCallToJS(args):
    ##print("tokens: " + str(functionTokens) + "  tokenlen: " + str(len(functionTokens)) + "  correctlen: " + str(len(functions[functionTokens[0]][0]))) # if the last item in the line was part of a funcion, and a string or list, the function wont properly get anilized, so that can be fixed here
    checkSyntax(line_number, functions[args[0]][0], args)
    if len(args) == len(functions[args[0]][0]):
        codeLine = ""
        for item in functions[args[0]][1]:
            if type(item) == str:
                codeLine += item
            else: # if its an int, add the corrosponding item from the tokens list
                codeLine += args[item]
        return(codeLine)
    raise Exception("toki nanpa "+Base10ToTokiPona(line_number)+"\nla ijo li pakala")
def convertConditinal(tokens): #things like == and && and < etc.
    output = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "lisama":
            tokens[i] = "=="
        if tokens[i] == "lisamaala":
            tokens[i] = "!="
        if tokens[i] == "lililitawa":
            tokens[i] = "<"
        if tokens[i] == "lisulitawa":
            tokens[i] = ">"
        if tokens[i] == "la":
            tokens[i] = "&&"
        if tokens[i] == "anu":
            tokens[i] = "||"
        if tokens[i] == "lilon":
            output[i-1] = tokens[i+1] + ".includes("+tokens[i-1]+")"
            i += 1
        else:
            output.append(tokens[i])
        i += 1
    return(output)

for line_number, line in enumerate(tokiilo): # get all functions that are deffined in the code
    line = line.split("  ")
    tokens = []
    for i in range(0,len(line)):
        if line[i].replace(" ", "") != "toki:":
            tokens.append(line[i].replace(" ", ""))
        else:
            break
    #print(tokens)
    if len(tokens) > 0:
        if tokens[0].replace(" ", "") == "pokipitokiilo":
                if tokens[-1] != "la":
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nnimi 'la' o pini e toki ni:\n"+"  ".join(tokens))
                checkSyntax(line_number, ["pokipitokiilo", "var"], tokens[:2])
                if tokens[1] == ":sike":
                    tokens[1] = "_sike"
                    sikeExists = True
                else:
                    functionMethod = [tokens[1]+"("]
                    for i in range(1, len(tokens[2:-1])+1):
                        functionMethod.append(i)
                        functionMethod.append(", ")
                    if(functionMethod[-1] == ", "):
                        functionMethod.pop()
                    functionMethod.append(")")
                    functions[tokens[1]] = [[tokens[1]]+["any"]*len(tokens[2:-1]), functionMethod]
                    #print([tokens[1:-1], functionMethod])
tokens = []
line = []
line_number = 0
for line_number, line in enumerate(tokiilo):
    rawLine = line.replace("    ", "")
    line = line.split("  ")
    firstParse = []
    #print(line)
    wordNum = 0
    while wordNum < len(line):
        line[wordNum] = line[wordNum].replace("[", "OPENBRACKET").replace("]", "CLOSEBRACKET").replace(":", "_")
        spacelessWord = line[wordNum].replace(" ", "")
        if not re.fullmatch(r"([a-zA-z]|_|OPENBRACKET|CLOSEBRACKET)*", spacelessWord):
            raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nsitelen ni li ken ala lon:\n"+spacelessWord+"\n"+"  ".join(line))
        word = line[wordNum]
        if spacelessWord == "toki_":
            break
        if spacelessWord != "":
            if checkNumber(spacelessWord):
                #print("num")
                line[wordNum] = str(toki_pona_to_base_10(spacelessWord))
                spacelessWord = line[wordNum] 
            if spacelessWord == "nanpa":
                if line[wordNum+1].replace(" ", "") in functions:
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\npoki pi toki ilo li ken ala lon pini pi nimi 'nanpa': "+"  ".join(line))
                if checkNumber(line[wordNum+1]):
                    line[wordNum+1] = str(toki_pona_to_base_10(line[wordNum+1]))
                firstParse[-1] += "["+line[wordNum+1]+"]"
                wordNum += 1
            elif spacelessWord == "te": 
                foundTo = False
                for i in range(wordNum, len(line)):
                    if line[i].replace(" ", "") == "to":
                        foundTo= True
                        break
                if foundTo == False:
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nsitelen 'to' o pini e sitelen 'te': "+"  ".join(line))
                firstParse.append('"' + "  ".join(line[wordNum+1:i]) + '"')
                wordNum = i
            else:
                firstParse.append(spacelessWord)
        wordNum += 1
    secondParse = []
    ##print(firstParse)
    wordNum = 0
    while wordNum < len(firstParse):
        spacelessWord = firstParse[wordNum].replace(" ", "")
        if spacelessWord == "kulupu": 
            foundPini = False
            for i in range(wordNum, len(firstParse)):
                if firstParse[i] == "pini":
                    foundPini = True
                    break
            if foundPini == False:
                raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nsitelen 'pini' o pini e sitelen 'kulupu': "+"  ".join(line))
            
            # Group elements enclosed within 'kulupu' and 'pini'
            sublist = firstParse[wordNum+1:i]
            secondParse.append('[' + ", ".join(sublist) + ']')
            
            wordNum = i
        else:
            secondParse.append(firstParse[wordNum])
        wordNum += 1
    tokens = []
    wordNum = 0
    while wordNum < len(secondParse):
        spacelessWord = secondParse[wordNum].replace(" ", "")
        if spacelessWord in functions:
            functionBits = secondParse[wordNum:wordNum+len(functions[spacelessWord][0])]
            #checkSyntax(line_number, functions[spacelessWord][0], functionBits)
            #print(functionBits)
            tokens.append(convertFunctionCallToJS(functionBits))
            wordNum += len(functionBits) - 1
        else:
            tokens.append(secondParse[wordNum])
        wordNum += 1
    #print(tokens)
    if kulupuAmmount != 0:
        raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nnimi 'pini' o pini e sitelen 'kulupu': "+"  ".join(line))
    if functionToken: 

        raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nnimi pi mute pi lili ike li lon pini pi nimi '" + functionTokens[0] + "': "+"  ".join(line))
    #None means anything. 1 means a number. 2 means variable
    if "".join(tokens).replace(" ", "") != "":
        if tokens[0] == "pokipitokiilo":
            if tokens[1] == "_sike":
                tokens[1] = "_sike()"
            js.append("function "+tokens[1]+"{")
            lineNumbers.append([line_number, rawLine])
        elif tokens[0] == "sikela":
            if tokens[-1] != "la":
                raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\nnimi 'la' o pini e toki ni:\n"+"  ".join(tokens))
            tokens = convertConditinal(tokens)
            js.append("while (" + " ".join(tokens[1:-1])+"){")
            lineNumbers.append([line_number, rawLine])
        elif tokens == ["pini"]:
            js.append("}")
            lineNumbers.append([line_number, rawLine])
        elif tokens[0] == "antela":
            if len(tokens) != 1:
                tokens = convertConditinal(tokens)
                js.append("} else if (" + " ".join(tokens[1:-1])+"){")
                lineNumbers.append([line_number, rawLine])
            else:
                js.append("}else{")
                lineNumbers.append([line_number, rawLine])
        elif tokens[-1] == "la":
            tokens = convertConditinal(tokens)
            js.append("if (" + " ".join(tokens[:-1])+"){")
            lineNumbers.append([line_number, rawLine])
        elif len(tokens) > 2:
            if tokens[1] == "li":
                checkSyntax(line_number, ["var", "li", "any"], tokens)
                js.append(tokens[0]+" = "+tokens[2])
                lineNumbers.append([line_number, rawLine])
            elif tokens[1] == "lipokie":
                if '"' in tokens[0] or type(tokens[0]) == int:
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken poki taso: "+line[0])
                for i in range(0,len(tokens[2:])):
                    if tokens[i+2] == "e":
                        tokens[i+2] = "+"
                    elif tokens[i+2] == "pikulupu":
                        tokens[i+2] = "*"
                    elif tokens[i+2] == "tankipisi":
                        tokens[i+2] = "/"
                js.append(tokens[0] + " = " + " ".join(tokens[2:]))
                lineNumbers.append([line_number, rawLine])
            elif tokens[1] == "lipokikine":
                if '"' in tokens[0] or type(tokens[0]) == int:
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken poki taso: "+line[0])
                for i in range(0,len(tokens[2:])):
                    if tokens[i+2] == "e":
                        tokens[i+2] = "+"
                    elif tokens[i+2] == "pikulupu":
                        tokens[i+2] = "*"
                    elif tokens[i+2] == "tankipisi":
                        tokens[i+2] = "/"
                js.append(tokens[0] + " = safeAdd([" + tokens[0] + ", " + ", ".join(tokens[2:])+"])")
                lineNumbers.append([line_number, rawLine])
            elif tokens[1] == "likulupue":
                if '"' in tokens[0] or type(tokens[0]) == int:
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken poki taso: "+line[0])
                for i in range(0,len(tokens[2:])):
                    if tokens[i+2] == "e":
                        tokens[i+2] = ", "
                    elif tokens[i+2] == "pikulupu":
                        tokens[i+2] = "*"
                    elif tokens[i+2] == "tankipisi":
                        tokens[i+2] = "/"
                js.append(tokens[0] + " = [" + "  ".join(tokens[2:]) + "]")
                lineNumbers.append([line_number, rawLine])
            elif tokens[1] == "likulupukine":
                if '"' in tokens[0] or type(tokens[0]) == int:
                    raise Exception("pakala li lon toki nanpa "+Base10ToTokiPona(line_number)+"!\n"+"  ".join(line)+"\nni li ken poki taso: "+line[0])
                for i in range(0,len(tokens[2:])):
                    if tokens[i+2] == "e":
                        tokens[i+2] = ", "
                    elif tokens[i+2] == "pikulupu":
                        tokens[i+2] = "*"
                    elif tokens[i+2] == "tankipisi":
                        tokens[i+2] = "/"
                js.append(tokens[0] + ".push(" + "  ".join(tokens[2:]) + ")")
                lineNumbers.append([line_number, rawLine])
            else:
                js.append("".join(tokens))
                lineNumbers.append([line_number, rawLine])
        else:
            js.append("".join(tokens))
            lineNumbers.append([line_number, rawLine])
templateCodeRAW = open("ilo-pi-toki-ilo/toki-ilo-open.txt", "r")
templateCode = templateCodeRAW.read()
templateCodeRAW.close()
templateCodeEndRAW = open("ilo-pi-toki-ilo/toki-ilo-pini.txt", "r")
templateCodeEND = templateCodeEndRAW.read().split("\n")
templateCodeEndRAW.close()
jsTemp = templateCode.split("\n")
jsTemp.append("path$ = '" + "/".join(path.split("/")[:-1]) + "/'")
startLineNum = "startLineNum = "+str(len(jsTemp))
jsTemp = jsTemp + js
lineNumbersFile = open("ilo-pi-toki-ilo/lineNumbers.js", "w")
lineNumbersFile.write("lineNumbers$ = " + str(lineNumbers)+"\n"+startLineNum)
lineNumbersFile.close()
if sikeExists:
    jsTemp += ["sike$ = setInterval(function () {try {_sike()} catch (err) {errorDisplayer(err)}}, 100/30)"]
jsTemp += templateCodeEND
outputFile = open("ilo-pi-toki-ilo/main.js", "w")
outputFile.write("\n".join(jsTemp))
outputFile.close()

class NoCacheHTTPRequestHandler(
    http.server.SimpleHTTPRequestHandler
):
    def send_response_only(self, code, message=None):
        super().send_response_only(code, message)
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')

directory = 'index.html'
httpd = http.server.HTTPServer(server_address, NoCacheHTTPRequestHandler)
try:
    print("o open e ni: http://localhost:"+str(port)+"/"+directory)
    httpd.serve_forever()
except:
    httpd.shutdown()
    print("\npini")