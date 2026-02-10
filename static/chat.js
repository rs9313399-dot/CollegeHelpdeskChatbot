function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (message === "") return;

    const chatBody = document.querySelector(".chat-body");

    // USER MESSAGE
    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerHTML = `
        ${message}
        <div class="time">${getTime()}</div>
    `;
    chatBody.appendChild(userDiv);

    input.value = ""; // ✅ input clear
    chatBody.scrollTop = chatBody.scrollHeight;

    // BOT TYPING...
    const typingDiv = document.createElement("div");
    typingDiv.className = "bot-msg typing";
    typingDiv.innerText = "Bot is typing...";
    chatBody.appendChild(typingDiv);
    chatBody.scrollTop = chatBody.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        setTimeout(() => {
            typingDiv.remove();

            const botDiv = document.createElement("div");
            botDiv.className = "bot-msg";
            botDiv.innerHTML = `
                ${data.reply}
                <div class="time">${getTime()}</div>
            `;
            chatBody.appendChild(botDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 1000); // ⏳ AI feel delay
    })
    .catch(err => {
        typingDiv.remove();
        const errorDiv = document.createElement("div");
        errorDiv.className = "bot-msg";
        errorDiv.innerText = "Error aa gaya bc 😵‍💫";
        chatBody.appendChild(errorDiv);
    });
}

// ENTER key support
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");

    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

// Quick buttons
function quickSend(text) {
    const input = document.getElementById("userInput");
    input.value = text;
    sendMessage();
}

// Clear chat
function clearChat() {
    const chatBody = document.querySelector(".chat-body");
    chatBody.innerHTML = `
        <div class="bot-msg">
            Hi  How can I help you?
            <div class="time">${getTime()}</div>
        </div>
    `;
}

// Time function
function getTime() {
    const now = new Date();
    return now.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}
