// Select elements from the DOM
const chatMessages = document.getElementById("chat-messages"); // Chat message container
const userInput = document.getElementById("user-input"); // Input field for user message
const sendButton = document.getElementById("send-button"); // Send button

// Function to append a message to the chat
function appendMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender === "User" ? "user-message" : "ai-message";
    messageDiv.textContent = `${sender}: ${message}`;
    chatMessages.appendChild(messageDiv);

    // Auto-scroll to the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send a message to the Flask API
async function sendMessage() {
    const userMessage = userInput.value.trim(); // Get user input and trim whitespace
    if (!userMessage) return; // Prevent sending empty messages

    // Display user message in the chat
    appendMessage("User", userMessage);
    userInput.value = ""; // Clear the input field

    try {
        // Make an API call to the Flask backend
        const response = await fetch("http://127.0.0.1:5000/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userMessage }), // Send user message as JSON
        });

        if (response.ok) {
            const data = await response.json();
            appendMessage("AI", data.reply); // Display AI's reply in the chat
        } else {
            appendMessage("AI", "Sorry, something went wrong."); // Handle server-side errors
        }
    } catch (error) {
        appendMessage("AI", "Error connecting to the server."); // Handle network errors
    }
}

// Attach event listener to the send button
sendButton.addEventListener("click", sendMessage);

// Allow pressing Enter key to send a message
userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});