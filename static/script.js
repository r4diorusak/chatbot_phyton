const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

// Remove welcome message on first interaction
let isFirstMessage = true;

// Send message on button click
sendBtn.addEventListener('click', sendMessage);

// Send message on Enter (Shift+Enter for new line)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Reset chat
resetBtn.addEventListener('click', resetChat);

async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Remove welcome message on first interaction
    if (isFirstMessage) {
        const welcomeMessage = chatContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        isFirstMessage = false;
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Disable send button
    sendBtn.disabled = true;
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    try {
        // Send message to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        typingIndicator.remove();
        
        if (data.status === 'success') {
            // Add bot response to chat
            addMessage(data.response, 'bot');
        } else {
            addMessage('Maaf, terjadi kesalahan: ' + data.error, 'bot');
        }
    } catch (error) {
        typingIndicator.remove();
        addMessage('Maaf, tidak dapat terhubung ke server.', 'bot');
    }
    
    // Enable send button
    sendBtn.disabled = false;
    messageInput.focus();
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message-content';
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    messageDiv.appendChild(typingDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return messageDiv;
}

async function resetChat() {
    if (!confirm('Yakin ingin menghapus riwayat chat?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Clear chat container
            chatContainer.innerHTML = `
                <div class="welcome-message">
                    <h2>Selamat datang! 👋</h2>
                    <p>Saya adalah AI assistant yang siap membantu Anda. Silakan tanyakan apapun!</p>
                </div>
            `;
            isFirstMessage = true;
        }
    } catch (error) {
        alert('Gagal mereset chat.');
    }
}

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 150) + 'px';
});
