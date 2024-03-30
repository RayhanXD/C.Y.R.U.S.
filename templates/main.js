<script>
    let mediaRecorder;
    let recordedChunks = [];
  
    var socket = io.connect('http://' + document.domain + ':' + location.port);
  
    socket.on('user_text', function(msg) {
          console.log('Received user_text: ', msg.data);
          const chatExchanges = document.querySelectorAll('.chat-exchange');
          const lastExchange = chatExchanges[chatExchanges.length - 1];
          const output = lastExchange.querySelector('.user-text');
          output.innerHTML += msg.data + " ";
          chatOutput.scrollTop = chatOutput.scrollHeight; // Added to scroll down to the latest message
    });
    
    socket.on('chatbot_text', function(msg) {
          console.log('Received chatbot_text: ', msg.data);
          const chatExchanges = document.querySelectorAll('.chat-exchange');
          const lastExchange = chatExchanges[chatExchanges.length - 1];
          const output = lastExchange.querySelector('.chatbot-text');
          output.innerHTML += msg.data;
          chatOutput.scrollTop = chatOutput.scrollHeight; // Added to scroll down to the latest message
  
    });
  
    const recordButton = document.getElementById('recordButton');
    const chatOutput = document.querySelector('.chat-messages'); // Updated to select the new chat-messages div
    const removeButton = document.getElementById('removeButton');
  
    var svgText = document.getElementById('svgText');
  
    // Added event listener to the recordButton to start/stop recording when clicked
    recordButton.addEventListener('click', function() {
  
      if(mediaRecorder && mediaRecorder.state == 'recording') {
      stopRecording();
      recordButton.classList.remove('recording');
      } else {
      startRecording();
      recordButton.classList.add('recording');
    }
    svgText.classList.remove('high-opacity');
    svgText.classList.add('low-opacity');
    });
  
    removeButton.addEventListener('click', function()
    {
      removeAllDivs();
      svgText.classList.remove('low-opacity');
      svgText.classList.add('high-opacity');
  });
    
    function startRecording() {
      recordedChunks = [];
      addUserDiv();
  
      navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          mediaRecorder.addEventListener('dataavailable', function(e) {
              recordedChunks.push(e.data);
          });
      });
    }
    function stopRecording() {
      addChatbotDiv();
      mediaRecorder.addEventListener('stop', function() {
          const audioBlob = new Blob(recordedChunks);
          const formData = new FormData();
          formData.append('file', audioBlob);
          fetch('/upload', {
              method:'POST',
              body: formData
          })
          .then(data => {
              //addPlaceholderDivs();
          })
      });
      mediaRecorder.stop();
    }
  
    function addUserDiv() {
      const messageDiv = document.createElement('div');
      messageDiv.className = 'message chat-exchange';
  
      const userDiv = document.createElement('div');
      userDiv.className = 'user-text';
      userDiv.textContent = 'User: ';
      const userIcon = document.createElement('span');
      userIcon.className = 'material-icons message-icon';
      userIcon.textContent = 'account_circle';
      userDiv.appendChild(userIcon);
      messageDiv.appendChild(userDiv);
  
      chatOutput.appendChild(messageDiv);
      chatOutput.scrollTop = chatOutput.scrollHeight; // Added to scroll down to the latest message
    }
  
    function addChatbotDiv() {
      const chatExchanges = document.querySelectorAll('.chat-exchange');
      const lastExchange = chatExchanges[chatExchanges.length - 1];
  
      const chatbotDiv = document.createElement('div');
      chatbotDiv.className = 'chatbot-text';
      chatbotDiv.textContent = 'Chatbot: ';
      const chatbotIcon = document.createElement('span');
      chatbotIcon.className = 'material-icons message-icon';
      chatbotIcon.textContent = 'chat';
    chatbotDiv.appendChild(chatbotIcon);
    lastExchange.appendChild(chatbotDiv);

    chatOutput.scrollTop = chatOutput.scrollHeight; // Added to scroll down to the latest message
  }

  function removeAllDivs() {
    const messageDivs = document.querySelectorAll('.message');
    messageDivs.forEach(div => div.remove());
  }
  setTimeout(() => {
  chatOutput.scrollTop = chatOutput.scrollHeight;
}, 0);

let showBrect = false;

const brectButton = document.getElementById('brectButton');
brectButton.addEventListener('click', function() {
    showBrect = !showBrect;
    fetch('/update_showBrect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `showBrect=${showBrect}`,
    });
});

let showInfo = false;

const infoButton = document.getElementById('infoText');
infoButton.addEventListener('click', function() {
    showInfo = !showInfo;
    fetch('/update_showInfo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `showInfo=${showInfo}`,
    });
});

let drawPoint = true;

const drawPoints = document.getElementById('drawPoint');
drawPoints.addEventListener('click', function() {
    drawPoint = !drawPoint;
    fetch('/update_drawPoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `drawPoint=${drawPoint}`,
    });
});

let drawLine = false;

const drawLines = document.getElementById('drawLine');
drawLines.addEventListener('click', function() {
    drawLine = !drawLine;
    fetch('/update_drawLine', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `drawLine=${drawLine}`,
    });
});
</script>