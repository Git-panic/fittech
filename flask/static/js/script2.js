// static/script.js

document.addEventListener("DOMContentLoaded", function () {
    // 웹캠을 켜고 비디오를 가져오는 함수
    function startCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                // 비디오 엘리먼트에 스트림 연결
                let video = document.getElementById("video");
                video.srcObject = stream;

                // Flask 백엔드로 비디오 프레임 전송
                setInterval(function () {
                    sendFrame(stream);
                }, 1000 / 30);
            })
            .catch(function (error) {
                console.log("Error accessing the camera: ", error);
            });
    }

    // 비디오 프레임을 Flask 백엔드로 전송하는 함수
    function sendFrame(stream) {
        let video = document.getElementById("video");
        let canvas = document.createElement('canvas');
        let context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 캔버스 이미지 데이터를 Base64로 인코딩
        let imageData = canvas.toDataURL('image/jpeg');

        // Flask 백엔드로 POST 요청
        fetch("/upload", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: imageData }),
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error("Error sending frame:", error));
    }

    // 웹캠 켜기
    startCamera();
});