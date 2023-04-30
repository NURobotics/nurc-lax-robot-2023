// Create a new WebSocket object
const socket = new WebSocket('wss://your-websocket-url');
//ws://<ip address>:8888/websocket

// When the socket is open
socket.addEventListener('open', (event) => {
    console.log('WebSocket is open.');

    // Send a message to the server to request the PNG image
    socket.send('get-png-image');
});

// When the socket receives a message
socket.addEventListener('message', (event) => {
    console.log('WebSocket message received.');

    // Check if the message is a PNG image
    if (event.data instanceof Blob && event.data.type === 'image/png') {
        // Create a new FileReader object to read the PNG image data
        const reader = new FileReader();
        reader.onload = (e) => {
            // Create a new Image object and set its source to the PNG image data
            const image = new Image();
            image.src = e.target.result;

            // Set the source of the image with id "myimage" to the PNG image data
            const myImage = document.getElementById('myimage');
            myImage.src = e.target.result;
        };

        // Read the PNG image data
        reader.readAsDataURL(event.data);
    }
});

// When the socket is closed
socket.addEventListener('close', (event) => {
    console.log('WebSocket is closed.');
});
