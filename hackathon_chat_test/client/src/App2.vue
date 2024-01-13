<template>
  <div class="aufgabenansicht-4">
    <div class="header">
      <div class="header-inner" id="groupContainer">
        <div class="vector-parent">
          <img class="frame-child" alt="" src="/ellipse-3.svg" />
          <img class="image-19-icon" alt="" src="/image-19@2x.png" />
        </div>
      </div>
      <div class="star-button-parent">
        <div class="star-button" id="starButtonContainer">
          <div class="vector-parent">
            <div class="frame-item"></div>
            <img
              class="image-16-icon"
              alt=""
              src="/image-16@2x.png"
              />
          </div>
        </div>
        <div class="profil-button">
          <div class="profil-button-child"></div>
          <div class="ellipse-group" id="groupContainer1">
            <div class="group-child"></div>
            <img
              class="image-98-icon"
              alt=""
              src="/image-98@2x.png"
              />
          </div>
        </div>
      </div>
      <div class="zurck-button" id="zurckButtonContainer">
        <img class="zurck-button-child" alt="" src="/ellipse-3.svg" />
        <img class="image-83-icon" alt="" src="/image-83@2x.png" />
      </div>
    </div>
 
    <div id="chatContainer">
    <div class="chatBody">
      <div class="messages" v-for="message in messages" :key="message.id">
        <div class="messageRow user" v-if="message.id % 2 == 0">
          <div class="message user">
            <p>{{ message.message }}</p>
          </div>
        </div>
        <div class="messageRow bot" v-else>
          <div class="message bot">
            <p>{{ message.message }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="chatFooter">
      <form @submit.prevent="sendMessage()">
        <input v-model="messageContent" id="createMessage" />
        <input type="submit" />
      </form>
    </div>
  </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";

export default {
  name: "App",
  setup() {
    const messages = ref([]);
    const messageContent = ref("");
    const chatHistory = ref([]);

    // Sends the message on form submit
    function sendMessage() {
      if (messageContent.value === "") return;
      createMessage(messageContent.value);

      // Pass chat_history to the backend with each POST request
      getResponse(messageContent.value, chatHistory.value);

      messageContent.value = "";
    }

    // Create a message
    function createMessage(message) {
      let id = 0;
      if (messages.value[messages.value.length - 1]) {
        id = messages.value[messages.value.length - 1].id + 1;
      }
      messages.value.push({
        id: id,
        message: message,
      });
    }

    // Get response from the backend
    async function getResponse(message, chatHistory) {
      const postData = {
        message: message,
        chat_history: chatHistory,
      };
      
      try {
        const { data } = await axios.post("http://127.0.0.1:5000/chat", postData);
        const { response, updatedChatHistory } = data;
        
        // Update the local chat_history with the one received from the backend
        chatHistory.value = updatedChatHistory;

        // Create a message from the response
        createMessage(response);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }

    return { messages, messageContent, sendMessage };
  },
};
</script>



<style>

.rechnen-mit-greren-zahlen-parent{
  color:white;
}

#chatContainer {

  height: 700px;
  width: 100vw;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  position: fixed; /* Positioned relative to the #parentContainer */
  bottom: 0; /* This keeps #chatContainer at the bottom of #parentContainer */
  left: 0;
  right: 0;
}
.chatHeader {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  color: white;
  margin-left: 5%;
}
.chatFooter {
  position: absolute;
  bottom: 0px;
  width: 100%;
}
.chatFooter form {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 95%;
  margin: 0 auto;
}
.chatBody {
  overflow-y: scroll;
  height: 85%;
}
#createMessage {
  width: 90%;
  margin-bottom: 12px;
}
input:not(#createMessage) {
  background-color: #AF05FF;
  border: 0;
  color: white;
  padding: 8px;
  margin-bottom: 12px;
  opacity: 0.8;
}
input:not(#createMessage):hover {
  opacity: 0.5;
}
.messageRow {
  display: flex;
  justify-content: flex-end;
}
.messageRow.bot {
  justify-content: flex-start;
}
.message p {
  color: white;
  padding: 0px 15px 0px 15px;
}
.message {
  border-radius: 50px;
  text-align: center;
  margin: 10px;
}
.messageRow.user .message {
  background-color: blue;
}
.messageRow.bot .message {
  background-color: #43cc47;
}
.chatBody::-webkit-scrollbar {
  width: 0px;
  height: 100%;
}
.frame-child {
  position: relative;
  width: 128px;
  height: 124px;
  z-index: 0;
}
.image-19-icon {
  position: absolute;
  margin: 0 !important;
  top: 22px;
  left: 18px;
  width: 91px;
  height: 80px;
  object-fit: cover;
  z-index: 1;
}
.vector-parent {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: var(--gap-3xs);
}
.frame-item,
.header-inner {
  position: relative;
  width: 128px;
  height: 124px;
  z-index: 0;
}
.header-inner {
  cursor: pointer;
}
.frame-item {
  border-radius: 50%;
  background-color: #25bbeb;
}
.image-16-icon {
  position: absolute;
  margin: 0 !important;
  top: 25px;
  left: 27px;
  width: 74px;
  height: 74px;
  object-fit: cover;
  z-index: 1;
}
.star-button {
  position: relative;
  width: 128px;
  height: 124px;
  cursor: pointer;
}
.group-child,
.profil-button-child {
  position: absolute;
  top: 0;
  left: 0;
}
.group-child {
  border-radius: 50%;
  background-color: var(--color-white);
  width: 128px;
  height: 124px;
}
.image-98-icon {
  position: absolute;
  top: 21px;
  left: 30px;
  width: 67px;
  height: 81px;
  object-fit: cover;
}
.ellipse-group {
  position: absolute;
  top: 0;
  left: 0;
  width: 128px;
  height: 124px;
  cursor: pointer;
}
.profil-button {
  position: relative;
  width: 128px;
  height: 124px;
}
.star-button-parent {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 25px;
  z-index: 1;
}
.image-83-icon,
.zurck-button-child {
  position: absolute;
  top: 0;
  left: 0;
  width: 128px;
  height: 124px;
}
.image-83-icon {
  top: 22px;
  left: 23px;
  width: 81px;
  height: 80px;
  object-fit: cover;
}
.zurck-button {
  position: absolute;
  margin: 0 !important;
  top: 19px;
  left: 175px;
  width: 128px;
  height: 124px;
  cursor: pointer;
  z-index: 2;
}
.header {
  position: absolute;
  top: 0;
  left: 0;
  width: 1440px;
  overflow: hidden;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 19px 25px;
  box-sizing: border-box;
}
.aufgabe-inner,
.group-item {
  position: absolute;
  left: 0;
  width: 1188.4px;
  height: 328px;
}
.group-item {
  top: 0;
  border-radius: 48.83px;
  border: 7.3px solid #af05ff;
  box-sizing: border-box;
}
.aufgabe-inner {
  top: 55px;
}
.level-4-1-zutaten {
  position: relative;
  line-height: 120%;
  white-space: pre-wrap;
}
.das-rezept-erfordert {
  position: relative;
  line-height: 120%;
  display: inline-block;
  width: 556px;
  height: 91px;
  flex-shrink: 0;
}
.aufgabenstellung {
  color:white;
  position: absolute;
  top: 110px;
  left: 88px;
  border-radius: 9.5px;
  width: 605px;
  height: 225px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 31.66867446899414px;
  box-sizing: border-box;
  gap: 15.83px;
}
.rechnen-mit-greren {
  position: absolute;
  top: 8px;
  left: calc(50% - 227px);
  line-height: 89.46%;
  display: inline-block;
  width: 505px;
  height: 45px;
}
.image-84-icon {
  position: absolute;
  top: 0;
  left: 0;
  width: 39px;
  height: 37px;
  object-fit: cover;
}
.aufgabe-child,
.rechnen-mit-greren-zahlen-parent {
  position: absolute;
  top: 0;
  left: calc(50% - 278px);
  width: 556px;
  height: 53px;
}
.aufgabe-child {
  left: calc(50% - 242.2px);
  font-size: 36px;
  font-family: var(--font-outfit);
}
.cup-1-icon {
  position: absolute;
  top: 157px;
  left: 779px;
  width: 75px;
  height: 63px;
  object-fit: cover;
}
.cup-1-1,
.mortar-1-icon {
  position: absolute;
  top: 142px;
  left: 868px;
  width: 194px;
  height: 194px;
  object-fit: contain;
}
.cup-1-1 {
  top: 99px;
  left: 830px;
  width: 63px;
  height: 63px;
  object-fit: cover;
}
.aufgabe {
  position: absolute;
  top: 163px;
  left: 51px;
  width: 1188.4px;
  height: 383px;
}
.aufgabenansicht-4-child {
  position: absolute;
  top: 494px;
  left: 1328px;
  width: 112.2px;
  height: 493px;
}
.aufgabenansicht-4 {
  position: relative;
  background-color: #020142;
  width: 100%;
  height: 1024px;
  overflow: hidden;
  text-align: left;
  font-size: var(--font-size-xl-6);
  color: var(--color-white);
  font-family: var(--font-inter);
}
</style>