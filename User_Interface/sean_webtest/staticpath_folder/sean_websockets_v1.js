//static 

var websocket = null;
var localhost = "";

// Initialize the websocket
function init() {
	if(window.location.hostname != "") {
		localhost = window.location.hostname;
	}
    
    writeToScreen("Connecting to ws://" + localhost + ":81/ ...");
//    websocket = new WebSocket("ws://" + localhost + ":81/");
    websocket = new WebSocket("ws://localhost:81/ws"); //see: r/ws in py script. need to hit the right endpoint in order for the handshake to work
    
    websocket.onopen = function(evt) {
        onOpen(evt)
    };
    websocket.onclose = function(evt) {
        onClose(evt)
    };
    websocket.onmessage = function(evt) {
        onMessage(evt)
    };
    websocket.onerror = function(evt) {
        onError(evt)
    }
}

function onOpen(evt) { // when handshake is complete:
	writeToScreen("Connected.");
}

function onClose(evt) { // when socket is closed:
    writeToScreen("Disconnected. Error: " + evt);    
}

/* function onMessage(msg) {
    var byteArray = new Uint8Array(msg.data);

    var blob = new Blob([byteArray], {type: 'image/jpeg'});

    // Get the image just taken from WiFi chip's RAM.
    var image = document.getElementById('goal_image');
    var reader = new FileReader();
    reader.onload = function(e) {
        image.src = e.target.result;
    };
    reader.readAsDataURL(blob);
} */

function onMessage(msg) {
    //previously: was used to take data sent from the webcam and plot the image
    var byteCharacters = atob(msg.data);
    var byteNumbers = new Array(byteCharacters.length);
    for (var i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    var byteArray = new Uint8Array(byteNumbers);

    var blob = new Blob([byteArray], {type: 'image/jpeg'});

    // Get the image just taken from WiFi chip's RAM.
	var image = document.getElementById('goal_image');
	var reader = new FileReader();
	reader.onload = function(e) {
		var img_test = new Image();
		img_test.onload = function(){image.src = e.target.result;};
		img_test.onerror = function(){;};
		img_test.src = e.target.result;
	};
	reader.readAsDataURL(blob);
}

function onError(evt) { // when an error occurs
	websocket.close();
	writeToScreen("Websocket error");
}


// Function to display to the message box
 function writeToScreen(message)
  {
	document.getElementById("msg").innerHTML += message + "\n";
	document.getElementById("msg").scrollTop = document.getElementById("msg").scrollHeight;
  }

// Open Websocket as soon as page loads
window.addEventListener("load", init, false);


//-----------------------------OLD CONTENT FROM GPT-------------------------------------------//

