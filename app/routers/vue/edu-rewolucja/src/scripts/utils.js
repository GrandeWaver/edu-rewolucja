
var utils = {
    isBlankVal(string){
        if(string === undefined || String(string).length == 0){
            return true
        } else {
            return false
        }
    },
    encodeRank(rank_coded){
        let rank_encoded = []
      
        if(rank_coded.includes("1")){
          rank_encoded.push('początkujący')
        }
        if(rank_coded.includes("2")){
          rank_encoded.push('podstawowy')
        }
        if(rank_coded.includes("3")){
          rank_encoded.push('średni')
        }
        if(rank_coded.includes("4")){
          rank_encoded.push('zaawansowany')
        }
      
        return rank_encoded.join(", ")
    },
    codeRank(rank_encoded){
      let rank_coded = ''
    
      if(rank_encoded.includes("początkujący")){
        rank_coded += '1'
      }
      if(rank_encoded.includes("podstawowy")){
        rank_coded += '2'
      }
      if(rank_encoded.includes("średni")){
        rank_coded += '3'
      }
      if(rank_encoded.includes("zaawansowany")){
        rank_coded += '4'
      }
      
      return rank_coded
     }
}

export default utils