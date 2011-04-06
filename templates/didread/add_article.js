//need to gather info from the current page, then hit that url. then cleanup.
// rooturl:{{ root_url }}
//
// url:    {{ url }}
// title:  {{ title }}
// author: {{ author }}
// frame_contents: {{ frame_contents }}

function send_info(finfo) {

    console.log("SENDINGININININ");

    console.log(finfo);

    console.log(finfo.title.value);
    console.log(finfo.author_name.value);
    console.log(finfo.vote.value);


    var title = finfo.title.value;
    var author_name = finfo.author_name.value;
    var vote = finfo.vote.value;
    var url = document.location;

    var request = "?url=" + escape(url) + "&title="+ escape(title) + "&author_name=" + escape(author_name) + "&vote=" + escape(vote);

    request = "{{ root_url }}add" + request;

    console.log(request);



    var js_el = document.createElement('scr'+'ipt');
    js_el.setAttribute('src', request);
    document.body.appendChild(js_el);


    console.log("DONENENENNENEE");
    
    

    return false;
}

function setup_form() {
    console.log("STARTING SEND");
    
    var durl = document.location;
    var dtitle = document.title;

    //http://localhost:8000/add?url=http://daringfireball.net/2011/03/something_big&vote=-1&title=Something%20Big&pub_date=2010-07-4
    
    var display = document.createElement('div');
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
    display.style.padding = "10px";

    document.body.appendChild(display);

    display.innerHTML = '{{ frame_contents|safe }}';

    document.getElementById("did_read_title").value = '{{ title }}';
    document.getElementById("did_read_author").value = '{{ author }}';

    console.log("ENDING SEND");
}

setup_form();
