document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("chatbot-toggle");
    const chatbotWindow = document.getElementById("chatbot-window");
    const closeBtn = document.getElementById("chatbot-close");
    const sendBtn = document.getElementById("chatbot-send");
    const inputField = document.getElementById("chatbot-input");
    const chatbotBody = document.getElementById("chatbot-body");

    // Toggle chatbot window
    toggleBtn?.addEventListener("click", () => {
        chatbotWindow.classList.toggle("hidden");
    });

    closeBtn?.addEventListener("click", () => {
        chatbotWindow.classList.add("hidden");
    });

    // Send message on button click or Enter key
    sendBtn?.addEventListener("click", sendMessage);
    inputField?.addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage();
    });

    // Append message to chat
    function appendMessage(sender, text) {
        const msg = document.createElement("p");
        msg.textContent = `${sender}: ${text}`;
        chatbotBody.appendChild(msg);
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }

    // Get Django CSRF token
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = cookie.substring("csrftoken=".length);
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Send message to Django backend
    function sendMessage() {
        const msg = inputField.value.trim();
        if (!msg) return;

        appendMessage("You", msg);
        inputField.value = "";

        fetch("/chatbot/api/", { // ✅ Backend endpoint
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(), // ✅ CSRF for Django
            },
            body: JSON.stringify({ message: msg }),
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            appendMessage("Bot", data.response || "No reply from server.");
        })
        .catch(err => {
            console.error("Chatbot error:", err);
            appendMessage("Bot", "⚠️ Error connecting to server.");
        });
    }
});
