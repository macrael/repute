//need to gather info from the current page, then hit that url. then cleanup.
// rooturl:{{ root_url }}
// url:    {{ url }}
// title:  {{ title }}
// author: {{ author }}

function send_info() {
    console.log("STARTING SEND");
    
    doc = document;
    durl = doc.location;
    dtitle = doc.title;

    //http://localhost:8000/add?url=http://daringfireball.net/2011/03/something_big&vote=-1&title=Something%20Big&pub_date=2010-07-4
    
    display = document.createElement('iframe');
    display.name = 'display_frame';
    display.id = 'display_frame';

    display.style.position = 'fixed';
    display.style.top = '40px';
    display.style.left = '45px'
    display.style.margin = '0';
    display.style.backgroundColor = 'lightgray';
    display.style.webkitBorderRadius = "20px";
    display.style.borderWidth = "3px";
    display.style.borderColor = "darkgray";
    display.style.borderStyle = "solid";
    display.style.webkitBoxShadow = "5px 5px 5px #222";

    document.body.appendChild(display);

    window['display_frame'].document.write('<html><body><form action="{{ root_url }}add" method="get"><input type="hidden" name="url" value="' + document.location + '"><label for="title">Title: </label><input type="text" value="{{ title }}" name="title" id="title"><br><label for="author">Author: </label><input type="text" name="author_name" value="{{ author }}" id="author"><br><label for="vote">Vote: </label><select name="vote" id="vote"> <option value="-1">bad</option> <option selected value="0">meh</option><option value="1">good</option></select><br><input type="submit" value="Did Read"></form></body></html>');

    console.log("ENDING SEND");
}

send_info();
