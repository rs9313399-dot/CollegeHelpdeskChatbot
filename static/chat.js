const STORAGE_KEY = "collegeHelpdeskChat_v1";

function saveChat() {
    const chatBody = document.querySelector(".chat-body");
    localStorage.setItem(STORAGE_KEY, chatBody.innerHTML);
}

function loadChat() {
    const chatBody = document.querySelector(".chat-body");
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && saved.trim()) {
        chatBody.innerHTML = saved;
        chatBody.scrollTop = chatBody.scrollHeight;
    }
}

function escapeHtml(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll("\"", "&quot;")
        .replaceAll("'", "&#039;");
}

function renderSuggestions(suggestions) {
    if (!Array.isArray(suggestions) || suggestions.length === 0) return "";
    const buttons = suggestions
        .map(t => `<button class="chip" onclick="quickSend('${escapeHtml(t)}')">${escapeHtml(t)}</button>`)
        .join("");
    return `<div class="suggestions">${buttons}</div>`;
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (message === "") return;

    const chatBody = document.querySelector(".chat-body");

    // USER MESSAGE
    const userDiv = document.createElement("div");
    userDiv.className = "user-msg";
    userDiv.innerHTML = `
        ${escapeHtml(message)}
        <div class="time">${getTime()}</div>
    `;
    chatBody.appendChild(userDiv);

    input.value = ""; // ✅ input clear
    chatBody.scrollTop = chatBody.scrollHeight;
    saveChat();

    // BOT TYPING...
    const typingDiv = document.createElement("div");
    typingDiv.className = "bot-msg typing";
    typingDiv.innerText = "Bot is typing...";
    chatBody.appendChild(typingDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
    saveChat();

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
                ${escapeHtml(data.reply)}
                <div class="time">${getTime()}</div>
                ${renderSuggestions(data.suggestions)}
            `;
            chatBody.appendChild(botDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
            saveChat();
        }, 1000); // ⏳ AI feel delay
    })
    .catch(err => {
        typingDiv.remove();
        const errorDiv = document.createElement("div");
        errorDiv.className = "bot-msg";
        errorDiv.innerText = "Error aa gaya 😵‍💫";
        chatBody.appendChild(errorDiv);
        saveChat();
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

    loadChat();
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
    saveChat();
}

// Time function
function getTime() {
    const now = new Date();
    return now.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}
