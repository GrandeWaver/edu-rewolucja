
var utils = {
    isBlankVal(string){
        if(string === undefined || String(string).length == 0){
            return true
        } else {
            return false
        }
    }
}

export default utils