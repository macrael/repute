//need to gather info from the current page, then hit that url. then cleanup.

function send_info() {
    console.log("STARTING SEND");
    
    doc = document;
    durl = doc.location;
    dtitle = doc.title;

    //this probably won't work because of origin.
    //xhr = new XMLHttpRequest();
    //xhr.open("GET",'http://macrael.com/draft');
    //xhr.send(null);

    //http://localhost:8000/add?url=http://daringfireball.net/2011/03/something_big&vote=-1&title=Something%20Big&pub_date=2010-07-4

    sc = doc.createElement('scr'+'ipt');
    url = "http://localhost:8000/add?"
    url += "url=" + durl + "&"
    url += "title=" + dtitle + "&"

    sc.setAttribute('src',url);
    doc.body.appendChild(sc);

    console.log("ENDING SEND");
}

send_info();
