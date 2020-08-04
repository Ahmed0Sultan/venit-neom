class VoiceRecorder {
	constructor() {
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			console.log("getUserMedia supported")
		} else {
			console.log("getUserMedia is not supported on your browser!")
		}

		this.mediaRecorder
		this.stream
		this.chunks = []
		this.isRecording = false

        this.recorderRef = document.querySelector("#recorder")
        this.canvas = document.querySelector('canvas');
        this.canvasCtx = this.canvas.getContext("2d");
        this.visualSelect = document.querySelector('#visSelect');
        // this.playerRef = document.querySelector("#player")

		// this.startRef = document.querySelector("#start")
		// this.stopRef = document.querySelector("#stop")
		
		// this.startRef.onclick = this.startRecording.bind(this)
        // this.stopRef.onclick = this.stopRecording.bind(this)
        
        this.visual = this.visualize.bind(this)

        $('#button').on('mousedown touchstart', this.startRecording.bind(this));

        

        $('#button').on('touchend mouseup', this.stopRecording.bind(this));

		this.constraints = {
			audio: true,
			video: false
		}
		
	}

	handleSuccess(stream) {
		this.stream = stream
		this.stream.oninactive = () => {
			console.log("Stream ended!")
		};
		this.recorderRef.srcObject = this.stream
		this.mediaRecorder = new MediaRecorder(this.stream)
		console.log(this.mediaRecorder)
		this.mediaRecorder.ondataavailable = this.onMediaRecorderDataAvailable.bind(this)
		this.mediaRecorder.onstop = this.onMediaRecorderStop.bind(this)
		this.recorderRef.play()
		this.mediaRecorder.start()
	}

	handleError(error) {
		console.log("navigator.getUserMedia error: ", error)
	}
	
	onMediaRecorderDataAvailable(e) { this.chunks.push(e.data) }
	
	onMediaRecorderStop(e) { 
			const blob = new Blob(this.chunks, { 'type': 'audio/ogg; codecs=opus' })
            const audioURL = window.URL.createObjectURL(blob)
            console.log(blob)
            console.log(audioURL)
            var httpRequest = new XMLHttpRequest();
            httpRequest.open("POST", "http://localhost:5000/", true);
            httpRequest.send(blob);
			this.chunks = []
			this.stream.getAudioTracks().forEach(track => track.stop())
			this.stream = null
	}

	startRecording() {
		if (this.isRecording) return
        this.isRecording = true
        console.log("visualSetting");
        this.visual().call()
        console.log("visualSetting");
		navigator.mediaDevices
			.getUserMedia(this.constraints)
			.then(this.handleSuccess.bind(this))
            .catch(this.handleError.bind(this))
        
	}
	
	stopRecording() {
		if (!this.isRecording) return
		this.isRecording = false
		this.recorderRef.pause()
		this.mediaRecorder.stop()
    }
    
    visualize() {
        let visualSetting = "sinewave";
        let WIDTH = this.canvas.width;
        let HEIGHT = this.canvas.height;
        let CENTERX = this.canvas.width / 2;
        let CENTERY = this.canvas.height / 2;
        // if (!analyser) return;
    
        if(visualSetting === "sinewave") {
          analyser.fftSize = 2048;
          var bufferLength = analyser.fftSize;
          console.log(bufferLength);
          var dataArray = new Uint8Array(bufferLength);
    
          this.canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);
    
          var draw = function() {
    
            drawVisual = requestAnimationFrame(draw);
    
            analyser.getByteTimeDomainData(dataArray);
    
            this.canvasCtx.fillStyle = 'rgb(200, 200, 200)';
            this.canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);
    
            this.canvasCtx.lineWidth = 2;
            this.canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
    
            this.canvasCtx.beginPath();
    
            var sliceWidth = WIDTH * 1.0 / bufferLength;
            var x = 0;
    
            for(var i = 0; i < bufferLength; i++) {
    
              var v = dataArray[i] / 128.0;
              var y = v * HEIGHT/2;
    
              if(i === 0) {
                this.canvasCtx.moveTo(x, y);
              } else {
                this.canvasCtx.lineTo(x, y);
              }
    
              x += sliceWidth;
            }
    
            this.canvasCtx.lineTo(this.canvas.width, this.canvas.height/2);
            this.canvasCtx.stroke();
          };
    
          draw();
    
        }
    
      }
	
}

window.voiceRecorder = new VoiceRecorder()