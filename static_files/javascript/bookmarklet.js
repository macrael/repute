function didread() {
//shamelessly stolen from instapaper. Probably should indicate that. 

var doc = document,

js_el = doc.createElement('scr'+'ipt'),

body = doc.body;

try {
    if(!body) throw(0);

    js_el.setAttribute('src','http://localhost:8000/javascript/add_article.js');
    body.appendChild(js_el);

    }catch(e){
        alert('Please wait until the page has loaded.');
    }
}

didread();

void(0)
