var id = 0;
var zaznam = -1;

function presmerovanie( url, method,id=-1,){
    if(id === 0){
        window.location.replace(url);
    }
    else {
        if(method === "GET"){
            window.location.replace(url + "?id=" + id);
        }
        if(method === "DELETE"){
            window.location.replace(url + "?delete=True&id=" + this.id);
        }
        if(method === "PUT"){
            if(url === '/revizia'){
                if( id === -1){
                    window.location.replace(url + "?put=True&id=" + this.id);
                    return;
                }
                 window.location.replace(url + "?put=True&id=" + id);
                 return;
            }
             var id = window.location.toString();
             var sub = id.substr(0, id.indexOf("?") );
            id = id.replace(sub, "");

            window.location.replace(url + "?put=True&id=" + id.replace("?id=", "") + "&list="  + zaznam);
            zaznam = -1;
        }
    }
}
function vymaz(id) {
    var modal = document.getElementById("vymaz");
    modal.style.display = "block";
    this.id = id;

}
function vykonajRevizuOkno(id) {
    var modal = document.getElementById("vykonaj");
    modal.style.display = "block";
    this.id = id;

}

function zmen(id){
    var button = document.getElementById("potvrd");
    if(document.getElementById(id.toString()).checked === false){
        zaznam = -1;
        button.disabled = true;
    }
    else if(zaznam !== -1){
        document.getElementById(id.toString()).checked = false;
    }
    else{
        button.disabled = false;
        zaznam = id;
    }

}

function skontroluj_vyplnenie_pri_vyrieseni(){
    if(document.getElementById("id_vyriesena").checked === true){
        if(document.getElementById("id_opatrenia") !== null){
            return false;
        }
        return true;
    }
    if(document.getElementById("id_opatrenia") !== null){
            return true;
    }

    return false;
}
