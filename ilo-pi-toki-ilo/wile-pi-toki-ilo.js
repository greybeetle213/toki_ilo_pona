// Save a cookie
function saveCookie(cookieName, data) {
    let expirationDays = 999 * 360
    if(typeof(data) != "string"){
        throw new TypeError()
    }
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + expirationDays);
  
    const cookieValue = encodeURIComponent(data) + (expirationDays ? `; expires=${expirationDate.toUTCString()}` : '') + '; path=/';
    document.cookie = `${cookieName}=${cookieValue}`;
}


function gcd(a, b) {
    return (b) ? gcd(b, a % b) : a;
} 

function decimalToFraction(_decimal) {

	if (_decimal%1 == 0){
		return {
			top		: _decimal,
			bottom	: 1,
			display	: _decimal + ':' + 1
		};
	}  else {

		var top		= _decimal.toString().replace(/\d+[.]/, '');
		var bottom	= Math.pow(10, top.length);
		if (_decimal > 1) {
			top	= +top + Math.floor(_decimal) * bottom;
		}
		var x = gcd(top, bottom);
		return {
			top		: (top / x),
			bottom	: (bottom / x),
			display	: (top / x) + ':' + (bottom / x)
		};
	}
};

// Read a cookie
function readCookie(cookieName) {
    const name = cookieName + '=';
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        let c = cookie;
        while (c.charAt(0) === ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
        const decodedValue = decodeURIComponent(c.substring(name.length, c.length));
        return decodedValue;
        }
    }
    return 0
}
  

function errorDisplayer(err, isSyntaxError=false){
    testError = err // so that the error can be accesed from the js debug console if needed
    if(typeof(sike$) != "undefined"){
        clearInterval(sike$)
    }
    ctx$.fillStyle = "#000000"
    leko(0,0,200,200)
    ctx$.fillStyle = "#FF0000"
    if(!isSyntaxError){
        var stack = err.stack
        stack = stack.split("\n")
        if(stack[stack.length-1] == ""){
            stack.pop()
        }
        var relevantStack = []
        for(i=0; i<stack.length; i++){
            stack[i] = stack[i].split(/@|:/)
            var indexOfFilePath = stack[i].length-3 
            stack[i][indexOfFilePath] = stack[i][indexOfFilePath].split(/\/+/)
            if(stack[i][indexOfFilePath][stack[i][indexOfFilePath].length-1] === "main.js" && Number(stack[i][indexOfFilePath+1]) - startLineNum - 1 < lineNumbers$.length && Number(stack[i][indexOfFilePath+1]) - startLineNum - 1 >= 0){ // if the error message is in the "main.js" file and is not on a line that is outside of the range of lines of tokiilo code contained in lineNumbers$
                relevantStack.push(stack[i])
            }
        }
    }else{
        relevantStack =['syntaxerror']
        err.name = "SyntaxError"
    }
    //console.log(relevantStack)
    var printLine = 2
    if (err.message == "KALAMAERROR"){
        sitelentoki("pakala li lon.. ken la sitelen anu kalama ni li lon ala" ,0,12)
    } else if (err.message == "CONVERSOINFLOATERROR"){
        sitelentoki("pakala li lon.. sina wile nasin toki e nanpa kipisi la o kepeken" ,0,12)
        printLine += 1
        sitelentoki("nasintokitannanpakipisi" ,0,24)
    }else {
        switch(err.name){
            case "RangeError":
                sitelentoki("pakala li lon.. suli nanpa anu lili nanpa li ike",0,12)
                break
            case "ReferenceError":
                sitelentoki("pakala li lon.. sina lukin kepeken ijo pi lon ala",0,12)
                break
            case "SyntaxError":
                sitelentoki("pakala li lon.. toki ilo pi nasin pakala li lon",0,12)
                break
            case "TypeError":
                sitelentoki("pakala li lon.. ni li ken ala kepeken ijo pi nasin ni",0,12)
                break
            case "URIError":
                sitelentoki("pakala li lon.. nasin URI ni li ike",0,12)
                break
            case "InvalidStateError":
                sitelentoki("pakala li lon.. ken la sitelen anu kalama ni li lon ala",0,12)
            default:
                sitelentoki("pakala li lon.." ,0,12)
                break
        }
    }
    for(i=0; i<relevantStack.length; i++){
        if(!isSyntaxError){
            var line = lineNumbers$[Number(relevantStack[i][indexOfFilePath+1])-startLineNum-1]
        }else{
            var line = lineNumbers$[err.lineno-startLineNum-1]
        }
        //console.log(lineNumbers$[Number(relevantStack[i][3])-startLineNum-1])
        sitelentoki("toki ilo nanpa " + Base10ToTokiPona(line[0]+1) + ": ", 0, 12*printLine)
        printLine += 1
        splitLine = line[1].split(" ")
        lineToPrint = ""
        var word = 0
        var wordNum = splitLine.length
        while(word < wordNum){
            if(!splitLine[0] || (ctx$.measureText(lineToPrint).actualBoundingBoxRight + ctx$.measureText(splitLine[0]+" ").actualBoundingBoxRight < 180)){
                lineToPrint += " " + splitLine[0]
                splitLine = splitLine.slice(1)
                word ++
            }else{
                sitelentoki(lineToPrint, 0, printLine*12)
                printLine += 1
                lineToPrint = ""
            }
        }
        if (lineToPrint += ""){
            sitelentoki(lineToPrint, 0, printLine*12)
            printLine += 1
        }
    }
}
window.addEventListener("error", async function(event) {
    testError = event
    await new Promise(resolve => {
        document.addEventListener("DOMContentLoaded", resolve);
    });
    ctx$ = document.getElementById("canvas").getContext("2d")
    // redefine ctx
    // define the size of  pixel all sizes are based around this
    canvas$ = document.getElementById("canvas")
    ctx$.font = "12px Sitelen_Pona"
    const SitelenPona$ = new FontFace('Sitelen_Pona', 'url(ilo-pi-toki-ilo/FairfaxPona.ttf)');
    await SitelenPona$.load()  
    document.fonts.add(SitelenPona$)
    errorDisplayer(event, true)
});    

// window.onerror = function(message, source, lineno, colno, error) {
//     console.log(message, source, lineno, colno, error)
// };

sprites$ = {}
function sitelen(path, x, y){
    var path = path$ + path
    if(!sprites$[path]){
        sprites$[path] = new Image()
        sprites$[path].src = path
        sprites$[path].onload = function() {
            ctx$.drawImage(sprites$[path], x, y)
        };
    } else {
        ctx$.drawImage(sprites$[path], x, y)
    }
}

sounds$ = {}
function kalama(path){
    var path = path$ + path
    if(!sounds$[path]){
        //console.log("kalama!")
        sounds$[path] = new Audio(path)
        sounds$[path].addEventListener("error", function(event) {
            errorDisplayer(new DOMException("KALAMAERROR"))
        });
        sounds$[path].onload = function() {
            sounds$[path].play()
        };
    } else {
        sounds$[path].play()
    }
}

function kalamalontenposama(path){
    var path = path$ + path
    if(!sounds$[path]){
        //console.log("kalama!")
        sounds$[path] = new Audio(path)
        sounds$[path].addEventListener("error", function(event) {
            errorDisplayer(new DOMException("KALAMAERROR"))
        });
        sounds$[path].onload = function() {
            sounds$[path].play()
        };
    } else {
        soundClode = sounds$[path].cloneNode()
        console.log("played")
        soundClode.play()
    }
}

function checkNumber(number) { //checks if a string follows all the rules of a toki pona number
    if (number === "" || typeof(number) == "number") {
        return false;
    }
    if (number.slice(0, 4) === "weka") {
        number = number.slice(4);
    }

    if (number === "ala") {
        return true;
    }
    while (number !== "") {
        if (number.slice(0, 3) === "ali" || number.slice(0, 3) === "ale") {
            number = number.slice(3);
        } else if (number.slice(0, 4) === "mute") {
            number = number.slice(4);
        } else if (number.slice(0, 4) === "luka") {
            number = number.slice(4);
        } else if (number.slice(0, 2) === "tu") {
            number = number.slice(2);
        } else if (number.slice(0, 3) === "wan") {
            number = number.slice(3);
        } else {
            return false;
        }
    }
    return true;
}

function TokiPonaToBase10(tpnum){   
    tpnum = tpnum.replaceAll(" ", "")
    if(!checkNumber(tpnum)){
        throw new TypeError()
    }
    var baseTenNumber = 0
    var weka = false
    if(tpnum.slice(0,4) == "weka"){
        weka = true
        tpnum = tpnum.slice(4)  
    }
    if(tpnum == "ala"){
        return(0)
    }
    while(tpnum.length>0){
        switch(tpnum[0]){
            case "a":
                tpnum = tpnum.slice(3)
                baseTenNumber *= 100
                break
            case "m":
                tpnum = tpnum.slice(4)
                baseTenNumber += 20
                break
            case "l":
                tpnum = tpnum.slice(4)
                baseTenNumber += 5
                break
            case "t":
                tpnum = tpnum.slice(2)
                baseTenNumber += 2
                break
            case "w":
                tpnum = tpnum.slice(3)
                baseTenNumber += 1
                break
        }
    }
    if(weka){
        baseTenNumber *= -1
    }
    return baseTenNumber
}

function Base10ToTokiPona(base10num){
    if(isNaN(base10num)){
        return "nanpapakala"
    }
    if(base10num % 1 != 0){
        throw new Error("CONVERSOINFLOATERROR")
    }
    var tokiPonaNumber = ""
    if(base10num < 0){
        tokiPonaNumber += "weka"
        base10num *= -1
    }
    if(base10num == 0){
        return "ala"
    }
    var endOfNumber = String(base10num)
    if(String(base10num).length % 2 == 0){
        var alisNedded = (String(base10num).length/2)-1
        base10num = Number(endOfNumber.slice(0,2))
        endOfNumber = endOfNumber.slice(2)
    }else{
        var tempnum = Number(endOfNumber.slice(0,1))
        endOfNumber = String(base10num).slice(1)
        while(tempnum>0){
            if(tempnum>=20){
                tempnum -= 20
                tokiPonaNumber += "mute"
            } else if(tempnum>=5){
                tempnum -= 5
                tokiPonaNumber += "luka"
            } else if(tempnum>=2){
                tempnum -= 2
                tokiPonaNumber += "tu"
            } else if(tempnum>=1){
                tempnum -= 1
                tokiPonaNumber += "wan"
            }
        }
        if(base10num >= 100){
            tokiPonaNumber += "ali"
        }
        var alisNedded = String(base10num).slice(1).length/2-1
        base10num = Number(String(base10num).slice(1))
        if(alisNedded<0){
            alisNedded = 0
        }
        base10num = Number(endOfNumber.slice(0,2))
        endOfNumber = endOfNumber.slice(2)
    }
    while(base10num > 0 || endOfNumber.length > 0 || alisNedded > 0){
        while(base10num>0){
            if(base10num>=20){
                base10num -= 20
                tokiPonaNumber += "mute"
            } else if(base10num>=5){
                base10num -= 5
                tokiPonaNumber += "luka"
            } else if(base10num>=2){
                base10num -= 2
                tokiPonaNumber += "tu"
            } else if(base10num>=1){
                base10num -= 1
                tokiPonaNumber += "wan"
            }
        }
        if(alisNedded > 0){
            alisNedded--
            base10num = Number(endOfNumber.slice(0,2))
            endOfNumber = endOfNumber.slice(2) 
            tokiPonaNumber += "ali"
        }
    }
    return tokiPonaNumber
}

function Base10ToTokiPonaFloat(floatNum, joiner){
    if(isNaN(floatNum)){
        return("nanpapakala")
    }
    decimalBit = floatNum - Math.floor(floatNum)
    decimalBit = Math.round(decimalBit*1000)/1000
    wholeBit = Math.floor(floatNum)
    fraction = decimalToFraction(decimalBit)
    //console.log(floatNum)
    //console.log(Base10ToTokiPona(wholeBit)+joiner+Base10ToTokiPona(fraction.top)+" tan kipisi "+Base10ToTokiPona(fraction.bottom))
    return(Base10ToTokiPona(wholeBit)+joiner+Base10ToTokiPona(fraction.top)+" tan kipisi "+Base10ToTokiPona(fraction.bottom))
}

function TokiPonaToBase10Float(floatNum, joiner){
    if(!floatNum.includes(joiner) || typeof(floatNum) != "string"){
        throw new TypeError()
    }
    floatNum = floatNum.split(joiner)
    if(floatNum.includes(" tan kipisi ")){
        floatNum[1] = floatNum[1].split(" tan kipisi ")
    } else {
        floatNum[1] = floatNum[1].split("tankipisi")
    }
    return(TokiPonaToBase10(floatNum[0]) + TokiPonaToBase10(floatNum[1][0]) / TokiPonaToBase10(floatNum[1][1]))
}

function sitelentoki(text, x, y){
    if (typeof(text) == "undefined"){
        throw new ReferenceError()
    }
    if (typeof(text) != "string"){
        throw new TypeError()
    }
    ctx$.fillText(text, x, y)
}

function kule(r,g,b){
    r = Math.round((r/9)*255)
    g = Math.round((g/9)*255)
    b = Math.round((b/9)*255)
    if(r > 255 || b > 255 || g > 255){
        throw new RangeError()
    }
    if(r < 0 || b < 0 || g < 0){
        throw new RangeError()
    }
    ctx$.fillStyle = 'rgb('+r+', '+g+', '+b+')'
    ctx$.strokeStyle = 'rgb('+r+', '+g+', '+b+')'
}

function leko(x, y, width, height){
    ctx$.beginPath();
    ctx$.fillRect(x, y, width, height); // rect(x, y, width, height)
    ctx$.stroke();
}

function linja(x0, y0, x1, y1, thickness){
   var dx =  Math.abs(x1-x0), sx = x0<x1 ? 1 : -1;
   var dy = -Math.abs(y1-y0), sy = y0<y1 ? 1 : -1;
   var err = dx+dy, e2;    
   dx *= thickness
   dy *= thickness
   err *= thickness                               /* error value e_xy */
   for (;;){                                                          /* loop */
      ctx$.fillRect(x0,y0, thickness,thickness);
      if (x0 == x1 && y0 == y1) break;
      e2 = 2*err;
      if (e2 >= dy) { err += dy; x0 += sx; }                        /* x step */
      if (e2 <= dx) { err += dx; y0 += sy; }                        /* y step */
   }
}

function sike( xc, yc, d) {  // NOTE: for fill only!
    r = d/2
    var x = r, y = 0, cd = 0;
  
    // middle line
    ctx$.rect(xc - x, yc, r<<1, 1);
  
    while (x > y) {
      cd -= (--x) - (++y);
      if (cd < 0) cd += x++;
      ctx$.rect(xc - y, yc - x, y<<1, 1);    // upper 1/4
      ctx$.rect(xc - x, yc - y, x<<1, 1);    // upper 2/4
      ctx$.rect(xc - x, yc + y, x<<1, 1);    // lower 3/4
      ctx$.rect(xc - y, yc + x, y<<1, 1);    // lower 4/4
    }
    ctx$.fill();
  }

function nena(button){
    switch(button){
        case "pokaopen":
            return left
        case "pokapini":
            return right
        case "anpa":
            return down
        case "sewi":
            return up
        case "nanpawan":
            return keyX
        case "nanpatu":
            return keyZ
    }
}

function safeAdd(items) { //only allows adding of variables of the same type
    if (items.length === 0) {
        return 0; // Handle empty array case
    }
    const type = typeof items[0];
    let answer = items[0];

    for (let i = 1, len = items.length; i < len; i++) {
        if (typeof items[i] === type) {
            answer += items[i];
        } else {
            throw new TypeError();
        }
    }

    return answer;
}

var left = false
var right = false
var down = false
var up = false
var keyX = false
var keyZ = false

document.addEventListener('keydown', (event) => {
    if (event.key == 'ArrowLeft') {
        left = true
    }
})
document.addEventListener('keyup', (event) => {
    if (event.key == 'ArrowLeft') {
        left = false
    }
})
document.addEventListener('keydown', (event) => {
    if (event.key == 'ArrowRight') {
        right = true
    }
})
document.addEventListener('keyup', (event) => {
    if (event.key == 'ArrowRight') {
        right = false
    }
})
document.addEventListener('keydown', (event) => {
    if (event.key == 'ArrowUp') {
        up = true
    }
})
document.addEventListener('keyup', (event) => {
    if (event.key == 'ArrowUp') {
        up = false
    }
})
document.addEventListener('keydown', (event) => {
    if (event.key == 'ArrowDown') {
        down = true
    }
})
document.addEventListener('keyup', (event) => {
    if (event.key == 'ArrowDown') {
        down = false
    }
})
document.addEventListener('keydown', (event) => {
    if (event.key == 'x') {
        keyX = true
    }
})
document.addEventListener('keyup', (event) => {
    if (event.key == 'x') {
        keyX = false
    }
})
document.addEventListener('keydown', (event) => {
    if (event.key == 'z') {
        keyZ = true
    }
})
document.addEventListener('keyup', (event) => {
    if (event.key == 'z') {
        keyZ = false
    }
})