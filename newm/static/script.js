document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const languageSelector = document.getElementById('language');

    sendBtn.addEventListener('click', function () {
        const message = userInput.value.trim();
        const selectedLanguage = languageSelector.value;
        if (message) {
            addUserMessage(message);
            sendMessage(message, selectedLanguage);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });

    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message user';
        messageElement.innerText = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function addBotMessage(message, screenshot = null) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message bot';
        messageElement.innerHTML = message;
        chatBox.appendChild(messageElement);

        if (screenshot) {
            const imgElement = document.createElement('img');
            imgElement.src = screenshot;
            imgElement.style.maxWidth = '100%';
            imgElement.style.marginTop = '10px';
            chatBox.appendChild(imgElement);
        }

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage(message, language) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message, language: language })
        })
        .then(response => response.json())
        .then(data => {
            addBotMessage(data.response, data.screenshot);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
