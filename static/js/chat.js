const loader = {'content':`<span class='loader'><span class='loader__dot'></span><span class='loader__dot'></span><span class='loader__dot'></span></span>`,'buttons':false};
const errorMessage = "My apologies, I'm not available at the moment. =^.^=";
const urlPattern = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
const loadingDelay = 700;
const aiReplyDelay = 1800;

const $document = document;
const $chatbot = $document.querySelector(".chatbot");
const $chatbotMessageWindow = $document.querySelector(
  ".chatbot__message-window"
);
const $chatbotHeader = $document.querySelector(".chatbot__header");
const $chatbotMessages = $document.querySelector(".chatbot__messages");
const $chatbotInput = $document.querySelector(".chatbot__input");
const $chatbotSubmit = $document.querySelector(".chatbot__submit");


document.addEventListener(
  "keypress",
  event => {
    if (event.which == 13) {
      validateMessage();
    }
  },
  false
);

$chatbotHeader.addEventListener(
  "click",
  () => {
    var element =                 document.getElementsByClassName("chatbot");
      element[0].style.display = "none";
     document.getElementById("chat-circle").style.display="block";
  },
  false
);

$chatbotSubmit.addEventListener(
  "click",
  () => {
    validateMessage();
  },
  false
);

document.getElementById("chat-circle").addEventListener(
  "click",
  () => {
    // Hit Start Conversation Endpoint
    fetch('startConversation',)
    .then(response => response.json())
    .then(data => 
      {
        console.log('Success:', data);

        // Show Chat Inteface
        var element = document.getElementsByClassName("chatbot");
        element[0].classList.remove("chatbot--closed");
        element[0].style.display = "block";
        $chatbotInput.focus();
        console.log(this);
        document.getElementById("chat-circle").style.display="none"; 
    })
    .catch((error) => 
    {
        console.error('Error:', error);
    }); 
}
);


// Functions
const toggle = (element, klass) => {
  const classes = element.className.match(/\S+/g) || [],
    index = classes.indexOf(klass);
  index >= 0 ? classes.splice(index, 1) : classes.push(klass);
  element.className = classes.join(" ");
};

const userMessage = content => {
  $chatbotMessages.innerHTML += `<li class='is-user animation'>
      <p class='chatbot__message'>
        ${content}
      </p>
      <span class='chatbot__arrow chatbot__arrow--right'></span>
    </li>`;
};

const aiMessage = (content, isLoading = false, delay = 0) => {
  setTimeout(() => {
    removeLoader();
    if (content.buttons){
      $chatbotMessages.innerHTML += `<li 
      class='is-ai animation' 
      id='${isLoading ? "is-loading" : ""}'>
        <span class='chatbot__arrow chatbot__arrow--left'></span>
        <div class='row' style="background-color:#ffffff;margin-left:50px; overflow-x: auto;padding-top: 8px; flex:auto;">
          ${content.content}
        </div>
      </li>`;
    }
    else{
      $chatbotMessages.innerHTML += `<li 
      class='is-ai animation' 
      id='${isLoading ? "is-loading" : ""}'>
        <div class="is-ai__profile-picture">
          <svg class="icon-avatar" viewBox="0 0 32 32">
            <use xlink:href="#avatar" />
          </svg>
        </div>
        <span class='chatbot__arrow chatbot__arrow--left'></span>
        <div class='chatbot__message' >
          ${content.content}
        </div>
      </li>`;
    }
    

    
    scrollDown();
  }, delay);
};

const removeLoader = () => {
  let loadingElem = document.getElementById("is-loading");
  if (loadingElem) {
    $chatbotMessages.removeChild(loadingElem);
  }
};

const escapeScript = unsafe => {
  const safeString = unsafe
    .replace(/</g, " ")
    .replace(/>/g, " ")
    .replace(/&/g, " ")
    .replace(/"/g, " ")
    .replace(/\\/, " ")
    .replace(/\s+/g, " ");
  return safeString.trim();
};

const validateMessage = () => {
  const text = $chatbotInput.value;
  const safeText = text ? escapeScript(text) : "";
  if (safeText.length && safeText !== " ") {
    resetInputField();
    userMessage(safeText);
    send(safeText);
  }
  scrollDown();
  return;
};

const multiChoiceAnswer = (value, title ) => {
  userMessage(title);
  send(value);
  scrollDown();
  return;
};

const processResponse = (val, type ) => {
  removeLoader();
  switch (type) {

    // 0 response is text
    case 0:
      output = {'buttons':false, 'content':val}
      break;

    // 1 response a is button list
    case 1:
      let buttons = ''
      for (let i = 0; i < val.length; i++) {
        let title = val[i].title;
        let value = val[i].payload;
        console.log(val[i])
        console.log(val[i].title)
        console.log(val[i].payload)
        
        buttons += `<button onclick='multiChoiceAnswer("${value}", "${title}")' value=${value}>${title}</button>`;
      }
      output = {'buttons':true, 'content':buttons};
      break;

    // 2 response is speech
    case 2:
      let speech = ''
      speech += `<audio style="max-width: 226px;"
          controls  controlsList="nodownload"
          src="${val}">
              Your browser does not support the
              <code>audio</code> element.
      </audio>`;
      output = {'buttons':false, 'content':speech}
      break;

    // 3 response is image - TODO
    case 3:
      console.log('response is image - TODO')
      break;
  }

    return output;
};

const setResponse = (val, delay = 0, type = 0 ) => {
  setTimeout(() => {
    aiMessage(processResponse(val, type));
  }, delay);
};

const resetInputField = () => {
  $chatbotInput.value = "";
};

const scrollDown = () => {
  const distanceToScroll =
    $chatbotMessageWindow.scrollHeight -
    ($chatbotMessages.lastChild.offsetHeight + 60);
  $chatbotMessageWindow.scrollTop = distanceToScroll;
  return false;
};

const send = (text = "") => {
  fetch(`/sendMessage?text=${text}`, {
    method: "GET",
    dataType: "json",
  })
    .then(response => response.json())
    .then(res => {

      console.log(res)
      if (res.status < 200 || res.status >= 300) {
        let error = new Error(res.statusText);
        throw error;
      }
      return res;
    })
    .then(res => {
      // extracting bot message from API response
      for (i = 0; i < res.TextResponse.length ;i++){
        setResponse(res.TextResponse[i], loadingDelay + aiReplyDelay, 0);
      }
      return res
    })
    .then(res => {
      // If response has buttons
      if (res.Buttons.length > 0){
        setResponse(res.Buttons, loadingDelay + aiReplyDelay + 10, 1);
      }

      // If response has speech
      if (res.SpeechResponseURL){
        setResponse(res.SpeechResponseURL, loadingDelay + aiReplyDelay + 10, 2);
      }
      return res
    })
    .catch(error => {
      setResponse(errorMessage, loadingDelay + aiReplyDelay);
      resetInputField();
      console.log(error);
    });

  aiMessage(loader, true, loadingDelay);
};
