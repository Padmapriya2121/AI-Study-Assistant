
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

let conversationId = null;

// Display messages in the chat window
function addMessage(text, className) {
    const message = document.createElement("div");

    message.classList.add("message", className);
    message.textContent = text;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;

    return message;
}

// Send message to the backend
async function sendMessage() {
    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    // Display user's message
    addMessage(message, "user-message");

    userInput.value = "";
    sendBtn.disabled = true;

    const loadingMessage = addMessage(
        "Thinking...",
        "bot-message"
    );

    try {
        // Send request to FastAPI
        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });

        const data = await response.json();

        loadingMessage.remove();

        if (!response.ok) {
            throw new Error(
                data.detail || "Something went wrong."
            );
        }

        // Save conversation ID for future messages
        conversationId = data.conversation_id;

        // Display Gemini's response
        addMessage(data.response, "bot-message");

    } catch (error) {
        loadingMessage.remove();

        addMessage(
            "Error: " + error.message,
            "bot-message"
        );

    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Send message when button is clicked
sendBtn.addEventListener("click", sendMessage);

// Send message when Enter is pressed
userInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
