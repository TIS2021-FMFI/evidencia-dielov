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

//zmazanie zaznamov
function vymaz(id) {
    var modal = document.getElementById("vymaz");
    modal.style.display = "block";
    this.id = id;

}

//naozaj chcete vykonat reviziu
function vykonajRevizuOkno(id) {
    var modal = document.getElementById("vykonaj");
    modal.style.display = "block";
    this.id = id;

}

//pri reviziach
function nastavDatumNasledujucej(){
    const posledna = document.getElementById('datum_poslednej')
    const nasledujuca = document.getElementById('datum_nasledujucej')
    const exspiracia = document.getElementById('exspiracia')
    const datum = new Date(posledna.value)
    datum.setDate(datum.getDate() + Number(exspiracia.value))

    nasledujuca.valueAsDate = datum
  
}

// ak datum alebo cas vyriesenia nie je zadefinovany tak nastavi momentalny datum + cas
function updateDate() {
    const datum_vyriesenia = document.getElementById('id_vyriesenie');
    const cas_vyriesenia = document.getElementById('id_vyriesenie_cas');
    if(document.getElementById("id_vyriesena").checked === true){
        //ak datum nie je zadany tak nastav na momentalny

        // console.log('datum vyriesenia',datum_vyriesenia.value)
        // console.log('cas vyriesenia',cas_vyriesenia.value)
        // console.log('kontrola','')

        //skontroluj ci je datum/cas vyriesenia uz zadany ak je tak nemen
        if (datum_vyriesenia.value && cas_vyriesenia.value) {
            return
        }


        var date = new Date();

        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();

        if (month < 10) month = "0" + month;
        if (day < 10) day = "0" + day;

        var today = year + "-" + month + "-" + day;

        datum_vyriesenia.value = today

        let hour = date.getHours()
        let minute = date.getMinutes()
        let second = date.getSeconds()
        if (hour < 10) hour = "0" + hour;
        if (minute < 10) minute = "0" + minute;
        if (second < 10) second = "0" + second;

        const now = hour + ":" + minute + ':' + second

        console.log(now)
        cas_vyriesenia.value = now

    } else {
        //vymaz nastaveny cas
        // datum_vyriesenia.value = undefined
        // cas_vyriesenia.value = undefined
    }
}

function updateRequired() {
    const popis = document.getElementById("id_popis");
    const dovod = document.getElementById("id_dovod");
    const opatrenie = document.getElementById("id_opatrenia");
    const datum_vyriesenia = document.getElementById("id_vyriesenie");
    const cas_vyriesenia = document.getElementById("id_vyriesenie_cas");

    if(document.getElementById("id_vyriesena").checked === true){
        //checkbox zapnuty
        popis.required = true;
        dovod.required = true;
        opatrenie.required = true;
        datum_vyriesenia.required = true;
        cas_vyriesenia.required = true;
    } else {
        //checkbox vypnuty
        dovod.required = false;
        opatrenie.required = false;
        datum_vyriesenia.required = false;
        cas_vyriesenia.required = false;
    }
}

function onReviziaCheckboxToggle() {
    updateDate();
    updateRequired();
}
