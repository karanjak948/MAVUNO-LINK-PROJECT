// =====================
// CSRF Helper
// =====================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const c = cookies[i].trim();
      if (c.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(c.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const box = document.getElementById("chatBox");
  const csrftoken = getCookie("csrftoken");

  // ✅ Paste your exact Postman-tested URL here
  const API_URL = "http://127.0.0.1:8000/chatbot/get-response/";

  // =====================
  // Load previous chat
  // =====================
  let history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
  history.forEach((msg) => appendMessage(msg.text, msg.who));

  // =====================
  // Append message to chat
  // =====================
  function appendMessage(text, who = "bot") {
    const el = document.createElement("div");
    el.className =
      who === "bot"
        ? "mb-2 p-2 bg-light rounded"
        : "mb-2 p-2 bg-success text-white rounded";
    el.style.whiteSpace = "pre-wrap";
    el.textContent = (who === "user" ? "You: " : "Bot: ") + text;
    box.appendChild(el);
    box.scrollTop = box.scrollHeight;

    history.push({ text, who });
    localStorage.setItem("chatHistory", JSON.stringify(history));
  }

  // =====================
  // Send message to backend
  // =====================
  async function sendMessage(message) {
    appendMessage(message, "user");
    input.value = "";
    appendMessage("…thinking", "bot");

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken, // needed if same-domain
        },
        body: JSON.stringify({ message }),
      });

      // Debugging aid: log request + response
      console.log("Request to:", API_URL);
      console.log("Payload:", { message });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      console.log("Response:", data);

      // remove "…thinking"
      const children = box.children;
      if (children.length) {
        const last = children[children.length - 1];
        if (last && last.textContent === "Bot: …thinking") last.remove();
      }

      appendMessage(data.response || "⚠️ No response from server.", "bot");
    } catch (err) {
      console.error("Chatbot error:", err);

      const children = box.children;
      if (children.length) {
        const last = children[children.length - 1];
        if (last && last.textContent === "Bot: …thinking") last.remove();
      }

      appendMessage("⚠️ Error contacting server. Please try again.", "bot");
    }
  }

  // =====================
  // Form submission
  // =====================
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const message = input.value.trim();
    if (message) sendMessage(message);
  });
});
