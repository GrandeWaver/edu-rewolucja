
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
     },

     pushToschedule(availability, selected_day){
      let last_index = Object.keys(availability[selected_day][0].schedule).length
      if(last_index == 0){
          availability[selected_day][0].schedule.push(
          {
              start: 11,
              end: 16
          }
          )
          return availability
      }
      // let last_hour_start = parseInt(_this.availability[selected_day][0].schedule[last_index-1].start)
      let last_hour_end = parseInt(availability[selected_day][0].schedule[last_index-1].end)
      // walidacja 24 godzin
      if(last_hour_end >= 24){
          return availability
      }
      else{
          if(last_hour_end + 3 > 24){
          last_hour_end = 24
          availability[selected_day][0].schedule.push(
              {
              start: last_hour_end - 1,
              end: last_hour_end
              }
          )
          }
          else{
          availability[selected_day][0].schedule.push(
              {
              start: last_hour_end + 1,
              end: last_hour_end + 3
              }
          )
          }
      }
      return availability
      }
}

export default utils