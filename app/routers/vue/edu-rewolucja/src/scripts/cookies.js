var cookies = {
getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  },
  
  createUserCookie(email){
    var expire_date = new Date(new Date().getTime()+60*60*1000*8765).toGMTString(); // 1 year
    document.cookie = "userCookie="+email+"; expires="+expire_date+"; path=/";
  },
  
  deleteCookie(name) {
      if( cookies.getCookie(name)){
        document.cookie = name + "= o_O ;expires=Thu, 01 Jan 1970 00:00:01 GMT";
      }
    }
}


export default cookies