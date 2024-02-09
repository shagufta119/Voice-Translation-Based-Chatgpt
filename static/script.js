
if (window.SpeechRecognition || window.webkitSpeechRecognition) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    const voiceButton = document.getElementById('voice-button');
    const searchInput = document.getElementById('user_input');

    recognition.continuous = false;
    recognition.lang = "en-US";

    voiceButton.addEventListener("click", () => {
        recognition.start();
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        searchInput.value = transcript;
        
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
    };
} else {
    
    voiceButton.style.display = "none";
}




function performSearch(event) {
  console.log("Performing search...");

 
 

  var searchInput = document.getElementById('user_input').value.trim();
  console.log("Search input:", searchInput);

  if (searchInput !== "") {
    console.log("Search input is not empty. Performing search...");
    addToHistory(searchInput);
    saveHistoryToLocalStorage();
  } else {
    console.log("Search input is empty. Skipping search...");
  }
}
function toggleChatHistory() {
  const searchHistory = document.getElementById("search-history");
  
  // Check if the screen width is less than or equal to 600px (adjust as needed)
  const isSmallScreen = window.innerWidth <= 600;

  // Toggle the class based on screen size
  if (isSmallScreen) {
    searchHistory.classList.toggle("show-sidebar");
  }
}


function clearHistory() {
  let historyList = document.getElementById('history-list');
 
  historyList.innerHTML = '';
  
  saveHistoryToLocalStorage(); 
}
function addToHistory(searchTerm) {
  let historyList = document.getElementById('history-list');
  let listItem = document.createElement('li');
  listItem.textContent = searchTerm;

  
  let deleteButton = document.createElement('button');
  deleteButton.className = 'delete-history';
  
  deleteButton.addEventListener('click', function () {
    
    historyList.removeChild(listItem);
    
  });

  
  listItem.appendChild(deleteButton);

  historyList.appendChild(listItem);
}

    function openNewChat() {
        // Redirect to the root route
        window.location.href = '/';

}    

document.addEventListener('DOMContentLoaded', function () {
  loadHistoryFromLocalStorage();
  
});

function saveHistoryToLocalStorage() {
  let historyItems = Array.from(document.querySelectorAll('#history-list li')).map(item => item.textContent);
  localStorage.setItem('searchHistory', JSON.stringify(historyItems));
}

function loadHistoryFromLocalStorage() {
  let historyList = document.getElementById('history-list');
  historyList.innerHTML = '';

  let storedHistory = localStorage.getItem('searchHistory');

  if (storedHistory) {
    let historyItems = JSON.parse(storedHistory);
    historyItems.forEach(item => {
      let listItem = document.createElement('li');
      listItem.textContent = item;

      let deleteButton = document.createElement('button');
      deleteButton.className = 'delete-history';
      //deleteButton.textContent = 'Delete';

      deleteButton.addEventListener('click', function () {
        historyList.removeChild(listItem);
        saveHistoryToLocalStorage();
      });

      listItem.appendChild(deleteButton);
      historyList.appendChild(listItem);
    });
  }
}
document.addEventListener("DOMContentLoaded", function () {
  // Wait for the DOM to be fully loaded before trying to access elements

  // Add event listener to all elements with the class "delete-button"
  document.querySelectorAll('.delete-button').forEach(function(button) {
      button.addEventListener('click', function(event) {
          // Prevent the default form submission behavior
          event.preventDefault();

          // Log to check if the event listener is triggered
          console.log('Button clicked');

          // Get the response ID from the "data-response-id" attribute
          var responseId = this.getAttribute('data-response-id');

          // Call the deleteResponse function with the response ID
          deleteResponse(responseId);
      });
  });
});

function deleteResponse(responseId) {
  // Send an asynchronous request to delete the response
  fetch(`/delete_response/${responseId}`, {
      method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
      // Handle the response as needed
      console.log(data);

      // Optionally, update the UI or remove the deleted element
      if (data.status === 'success') {
          document.querySelector(`.delete-button[data-response-id="${responseId}"]`).closest('li').remove();
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  
})

function handleResponse() {
    // Assuming you have some condition to determine when to hide the elements
    var shouldHideElements = true;

    if (shouldHideElements) {
        document.getElementById('aiContainer').classList.add('hidden');
        document.getElementById('voiceContainer').classList.add('hidden');
        document.getElementById('languageContainer').classList.add('hidden');
        document.getElementById('historyContainer').classList.add('hidden');
    }


 
 setTimeout(handleResponse, 3000);
  }
  




function openAppPy() {
   
    window.open('/website', '_blank');
  }

function openNewChat() {
    // Open a new tab or window with the app.py file
    window.open('/index', '_blank');
  }


