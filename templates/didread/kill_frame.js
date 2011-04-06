//This javascript is loaded after we have submitted stuff
//It can eventually note errors, but for now it will just kill the iframe.

function kill_display_frame(){

    display = document.getElementById('display_frame');

    console.log(display);

    display.parentElement.removeChild(display);

}

kill_display_frame();
