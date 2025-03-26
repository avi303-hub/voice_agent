document.addEventListener("DOMContentLoaded", function () {
  const recordBtn = document.getElementById("recordBtn");
  const statusText = document.getElementById("status");
  const audioPlayer = document.getElementById("audioPlayer");

  let mediaRecorder;
  let audioChunks = [];

  // Check if browser supports audio recording
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          audioChunks = [];
          uploadAudio(audioBlob);
        };
      })
      .catch((error) => {
        console.error("Microphone access denied:", error);
        statusText.textContent = "Microphone access denied!";
      });
  } else {
    statusText.textContent = "Audio recording not supported in this browser.";
  }

  // Start / Stop Recording
  recordBtn.addEventListener("click", function () {
    if (mediaRecorder.state === "inactive") {
      mediaRecorder.start();
      recordBtn.textContent = "Stop Recording";
      statusText.textContent = "Recording...";
    } else {
      mediaRecorder.stop();
      recordBtn.textContent = "Start Recording";
      statusText.textContent = "Processing...";
    }
  });

  // Upload audio file to API
  function uploadAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "voice_query.wav");

    fetch("/api/ask/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.audio_file) {
          statusText.textContent = "Response received!";
          audioPlayer.src = data.audio_file;
          audioPlayer.style.display = "block";
        } else {
          statusText.textContent = "Error processing your request.";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        statusText.textContent = "Failed to connect to the server.";
      });
  }
});
