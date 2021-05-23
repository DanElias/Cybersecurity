// https://medium.com/swlh/how-to-access-webcam-and-take-picture-with-javascript-b9116a983d78
let picture;
let webcam;
let webcamElement;
let canvasElement;
let snapButtonElement;
let startButtonElement;

function initialize() {
    webcamElement = document.getElementById('webcam');
    canvasElement = document.getElementById('canvas');
    webcam = new Webcam(webcamElement, 'user', canvasElement);
    snapButtonElement = document.getElementById('capture');
    startButtonElement = document.getElementById('retake');
}

function start() {
    canvasElement.style.display = "none";
    webcamElement.style.display = "block";
    snapButtonElement.style.display = "block";
    startButtonElement.style.display = "none";

    webcam.start()
    .then(result => {
        console.log("result");
    })
    .catch(err => {
        alert(err);
        console.log(err);
    });
}

function snap() {
    picture = webcam.snap();
    webcamElement.style.display = "none";
    canvasElement.style.display = "block";
    snapButtonElement.style.display = "none";
    startButtonElement.style.display = "block";
    webcam.stop();
    alert("Your picture has been taken!");
}

initialize();
start();