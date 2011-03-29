function didread() {
//shamelessly stolen from instapaper. Probably should indicate that. 

var doc = document;
var title = document.title;
var url = document.location;

js_el = doc.createElement('scr'+'ipt'),

body = doc.body;

try {
    if(!body) throw(0);
    //at some point, need to have a user id in here.
    js_el.setAttribute('src','{{ root_url }}initial_add.js?url=' + url + '&title=' + title);
    body.appendChild(js_el);

    }catch(e){
        alert('Please wait until the page has loaded.');
    }
}

didread();

void(0)
