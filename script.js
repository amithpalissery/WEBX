const userInput = document.getElementById('user-query');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', () => {
  // Simulate receiving a response from Bard (replace with your logic)
  const userMessage = userInput.value;
  userInput.value = ''; // Clear input field after sending

  const responseDiv = document.createElement('div');
  responseDiv.classList.add('bard-message');
  responseDiv.innerHTML = `Processing your request...`;

  const chatContainer = document.querySelector('.chat-container');
  chatContainer.appendChild(responseDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to bottom

  // Replace this with actual logic to process the user query and generate a response
  setTimeout(() => {
    responseDiv.innerHTML = `Bard: I'm still under development, but I'm getting better at answering your questions. Here's what I found based on the web...`;
  }, 1000); // Simulate processing time
});
