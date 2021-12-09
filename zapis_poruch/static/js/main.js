function presmerovanie(id, url, method){
    if(id === null){
        window.location.replace(url);
    }
    else {
        if(method === "GET"){
            window.location.replace(url + "?id=" + id);
        }
        if(method === "DELETE"){
            window.location.replace(url + "?delete=True&id=" + id);
        }
        if(method === "PUT"){
            window.location.replace(url + "?put=True&id=" + id);
        }
    }
}