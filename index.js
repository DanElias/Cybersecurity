class Cypher {

    /**
     * Constructor for class Cypher
     * @param {String} text 
     * @param {String} password 
     */
    constructor(text = "", password = "") {
        this.text = text
        this.password = password
        this.encryptedText = ""
    }

    /**
     * Sets plain text
     * @param {String} text 
     */
    SetText(text) {
        this.text = text
    }

    /**
     * Sets the encrypted text
     * @param {String} text 
     */
    SetEncryptedText(encryptedText) {
        this.encryptedText = encryptedText
    }

    /**
     * Encrypts a text
     */
    Encrypt () {
        let textLen = this.text.length
        let n = Math.ceil(textLen / 16)
        this.encryptedText = ""
        for (let  i = 0; i < n; i++) {
            let spiralMatrix = this.SpiralMatrix(4, this.text.slice(i*16,(i+1)*16))
            let transposedMatrix = this.Transpose(spiralMatrix)
            let key = this.Hash()
            let xorMatrix = this.XOR(transposedMatrix, key)
            let shiftedMatrix = this.ShiftBitsRight(xorMatrix)
            for (let j = 0; j < 4; j++) {
                for (let k = 0 ; k < 4; k++) {
                    this.encryptedText += " " + shiftedMatrix[j][k].toString(16)
                }
            }
        }
        this.encryptedText = this.encryptedText.slice(1, this.encryptedText.length)
        return this.encryptedText
    }

    /**
     * Decrypts an encyrpted string
     */
    Decrypt() {
        console.log(this.encryptedText)
        let textArr = this.encryptedText.split(" ").map(function(encryptedChar) {
            return BigInt("0x" + encryptedChar, 16);
        });
        let text = ""
        let n = Math.ceil(textArr.length / 16)
        for (let  i = 0; i < n; i++) {
            let matrix = this.ToMatrix(textArr.slice(i*16,(i+1)*16), 4)
            let shiftedMatrixInv = this.ShiftBitsLeft(matrix)
            let key = this.Hash()
            let xorMatrixInv = this.XORInverse(shiftedMatrixInv, key)
            let transposedMatrixInv = this.Transpose(xorMatrixInv)
            text += this.SpiralMatrixInv(transposedMatrixInv)
        }
        return text.trim()
    }

    /**
     * Substitutes each value in the matrix with an XOR of each value and the key
     * Generates Confusion
     * @param {Array of Arrays} matrix 
     * @param {256 bits BigInt} key 
     * @returns matrix
     */
    XOR (matrix = [[]], key)  {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                matrix[i][j] = BigInt(matrix[i][j].charCodeAt(0)) ^ key
            }
        }
        return matrix
    }

    /**
     * 
     * @param {Array of Arrays} matrix 
     * @param {256 bits BigInt} key 
     * @returns matrix
     */
    XORInverse (matrix = [[]], key) {
        let newMatrix = [[0, 0 ,0 , 0],[0, 0 ,0 , 0],[0, 0 ,0 , 0],[0, 0 ,0 , 0]]
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                newMatrix[i][j] = String.fromCharCode(Number(matrix[i][j] ^ key))
            }
        }
        return newMatrix
    }

    /**
     * Shifts 2 bits to the left, and the last 2 adds them to the beginning
     * @param {Array of Arrays} matrix
     * @returns {Array of Arrays} matrix 
     */
    ShiftBitsRight (matrix) {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                let binaryStr = matrix[i][j].toString()
                let tempLasts = binaryStr.slice(-2)
                binaryStr = tempLasts + binaryStr.slice(0, binaryStr.length - 2)
                matrix[i][j] = BigInt(binaryStr,2) 
            }
        }
        return matrix
    }

    /**
     * Shifts 2 bits to the right, and the first 2 adds them to the beginning
     * @param {Array of Arrays} matrix
     */
    ShiftBitsLeft (matrix) {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                let binaryStr = matrix[i][j].toString()
                let tempFirsts = binaryStr.slice(0,2)
                binaryStr = binaryStr.slice(2, binaryStr.length) + tempFirsts
                matrix[i][j] = BigInt(binaryStr,2) 
            }
        }
        return matrix
    }

    /**
     * Hashes the user's password
     */
    Hash () {
        // TO-DO - Generate 256 bits with the password given by the user
        let hexStr = 0x3f6ef2d06e3d45001e5bb6f4c0e34231b11b11cd6789c4d41598cee73fe65f46
        let newInt = BigInt(hexStr)
        return newInt
    }

    /**
     * Fills a matrix in a clockwise spiral form with a given string
     * Generates Difusion
     * @param {Number Integer} n 
     * @param {String} text 
     * @returns 
     */
    SpiralMatrix (n = 4, text = "") {
        let results = [];
        for(let i = 0; i < n; i++){
            results.push([]);
        }

        let counter = 0;
        let startCol = 0;
        let startRow = 0;
        let endCol = n - 1;
        let endRow = n - 1;

        while( startCol <= endCol && startRow <= endRow ){
            //top row - move down
            for(let col = startCol; col <= endCol; col++){
                if (text[counter]) {
                    results[startRow][col] = text[counter];
                } else {
                    results[startRow][col] = ' '
                }
                counter++;
            }
            startRow++;
            //right column - move left
            for(let row = startRow; row <= endRow; row++){
                if (text[counter]) {
                    results[row][endCol] = text[counter];
                } else {
                    results[row][endCol] = ' '
                }
                counter++;
            }
            endCol--;
            //bottom row - move up
            for(let col = endCol; col >= startCol; col--){
                if (text[counter]) {
                    results[endRow][col] = text[counter];
                } else {
                    results[endRow][col] = ' '
                }
                counter++;
            }
            endRow--;
            //left column -  move right
            for(let row = endRow; row >= startRow; row--){
                if (text[counter]) {
                    results[row][startCol] = text[counter];
                } else {
                    results[row][startCol] = ' '
                }
                counter++;
            }
            startCol++;
        }
        return results;
    }

    /**
    * Fills a matrix in a clockwise spiral form with a given string
    * Generates Difusion
    * @param {Number Integer} n 
    * @param {String} text 
    * @returns 
    */
    SpiralMatrixInv (matrix, n = 4) {
        let result = "";
        let startCol = 0;
        let startRow = 0;
        let endCol = n - 1;
        let endRow = n - 1;

        while( startCol <= endCol && startRow <= endRow ){
            //top row - move down
            for(let col = startCol; col <= endCol; col++){
                result = result + matrix[startRow][col]
            }
            startRow++;
            //right column - move left
            for(let row = startRow; row <= endRow; row++){
                result = result + matrix[row][endCol]
            }
            endCol--;
            //bottom row - move up
            for(let col = endCol; col >= startCol; col--){
                result = result + matrix[endRow][col]
            }
            endRow--;
            //left column -  move right
            for(let row = endRow; row >= startRow; row--){
                result = result + matrix[row][startCol]
            }
            startCol++;
        }
        return result;
    }

    /**
     * Transposes a matrix (rows for columns and columns for rows)
     * Generates Difusion
     * @param {Array(Array)} matrix 
     * @returns 
     */
    Transpose (matrix) {
        let transposedMatrix = matrix
        let len = transposedMatrix.length
        for (let i = 0; i < len; i++) {
            for (let j = i; j < len; j++) {
                let temp = transposedMatrix[i][j];
                transposedMatrix[i][j] = transposedMatrix[j][i];
                transposedMatrix[j][i] = temp;
            }
        }
        return transposedMatrix
    }

    /**
     * Slice: (start, end) not including the element at index end. If end is greater
     * than the array length, then it just grabs the elements that do exist 
     * @param {Array} array 
     * @param {number} size 
     */
    ToMatrix(array, size) {
        let res = [];
        let index = 0;
        while(index < array.length){
            res.push(array.slice(index, index + size));
            index += size;
        }
        return res;
    }
}

function encrypt() {
    text = document.getElementById("plain-text").value
    myEncrypt.SetText(text)
    encryptedText = myEncrypt.Encrypt()
    document.getElementById("encrypted-plain-text").value = encryptedText
    document.getElementById("cryptogram").value = encryptedText
}

function decrypt() {
    text = document.getElementById("cryptogram").value
    decryptedText = myEncrypt.Decrypt()
    document.getElementById("decrypted-cryptogram").value = decryptedText
}

myEncrypt = new Cypher()

/*
myEncrypt = new Cypher("Hola estamos aquí algo padre hoys", "contraseña")
encryptedText = myEncrypt.encrypt()
console.log("The encrypted text is: " + encryptedText.split(" ").join(""))
decryptedText = myEncrypt.decrypt()
console.log("The decrypted text is: " + decryptedText)
*/