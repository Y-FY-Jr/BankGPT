<template>
  <div class="container">
    <div class="chat-section">
      <!-- chat arae -->
      <div class="messages">
        <!-- messages showing area -->
        <div v-for="(message, index) in messages" :key="index" class="message" :class="{'user-message': message.source == 'User', 'ai-message': message.source == 'AI'}">
          <!-- display avatar based on message source -->
          <div class="message-container">
            <img v-if="message.source === 'User'" src="./marple.png" class="avatar">
            <img v-if="message.source === 'AI'" src="./poirot.png" class="avatar">
            <div class="text">{{ message.text }}</div>
          </div>
        </div>
      </div>
      <div class="message-input">
        <input type="text" v-model="newMessage" placeholder="Type a message..." @keyup.enter="sendMessage">
        <button @click="sendMessage">Send</button>
      </div>
    </div>
    
    <div class="buttons-section">
      <button @click="showProducts('Fund')">
        <img src="./fund.jpeg" alt="Image Description">Fund
      </button>
      <button @click="showProducts('Debenture')">
        <img src="./debenture.webp" alt="Image Description">Debenture
      </button>
      <button @click="showProducts('Insurance')">
        <img src="./insurance.webp" alt="Image Description">Insurance
      </button>
        <div class="button-explain">
          <button @click="showExplanation">Explanation</button>
        </div>
    </div>
  </div>

  <div v-if="showModalF" class="modal" :style="{ display: showModalF ? 'block' : 'none' }">
  <div class="modal-content">
    <span class="close" @click="closeModal">&times;</span>
    <h2>Fund List</h2>
    <p></p>
    <p></p>
    <table class="fund-table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Product Type</th>
          <th>Suggested Payment Up-limit</th>
        </tr>
      </thead>
      <tbody v-if="funds && funds.length">
        <tr v-for="fund in funds" :key="fund[0]">
          <td>{{ fund[0] }}</td>
          <td>{{ fund[1] }}</td>
          <td>{{ fund[2] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

  <div v-if="showModalD" class="modal" :style="{ display: showModalD ? 'block' : 'none' }">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>Debenture List</h2>
      <p></p>
      <p></p>
      <table class="debenture-table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Product Type</th>
          <th>Suggested Payment Up-limit</th>
        </tr>
      </thead>
      <tbody v-if="debentures && debentures.length">
        <tr v-for="debenture in debentures" :key="debenture[0]">
          <td>{{ debenture[0] }}</td>
          <td>{{ debenture[1] }}</td>
          <td>{{ debenture[2] }}</td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>

  <div v-if="showModalI" class="modal" :style="{ display: showModalI ? 'block' : 'none' }">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>Insurance List</h2>
      <p></p>
      <p></p>
      <table class="insurance-table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Product Type</th>
          <th>Suggested Payment Up-limit</th>
        </tr>
      </thead>
      <tbody v-if="insurances && insurances.length">
        <tr v-for="insurance in insurances" :key="insurance[0]">
          <td>{{ insurance[0] }}</td>
          <td>{{ insurance[1] }}</td>
          <td>{{ insurance[2] }}</td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>

  <div v-if="showModalE" class="modal" :style="{ display: showModalE ? 'block' : 'none' }">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <p>This software helps users interact with a chatbot for banking services...</p>
      <p></p>
      <p></p>
      <p>【Products】 page:</p>
      <p>Type in the textfield and you could chat with AI assistant. Or click buttons 'Fund' 'Debenture' 'Insurance' to see current bank products on the market.</p>
      <p></p>
      <p></p>
      <p>【My Account】 page:</p>
      <p>Check you account information and property situation.</p>
    </div>
  </div>
</template>

<script>
//import productsData from '../../../backend/products.json';
export default {
  data() {
    return {
      ws: null,   // Web Socket Instance (I try to combine two backends for PC and phone into one, now do not use it yet)
      newMessage: '',
      messages: [],
      // info of products
      products: [],
      showModalF: false,
      showModalD: false,
      showModalI: false,
      showModalE: false,
    };
  },
  created() {
  //this.connect();
  fetch('/products_list.json')
    .then(response => response.json())
    .then(data => {
      // flat the arrays
      this.products = data.flat(1);
    })
    .catch(error => console.error('Error fetching products:', error));
},
computed: {
  funds() {
    return this.products.filter(product => product[1].includes('Fund'));
  },
  debentures() {
    return this.products.filter(product => product[1].includes('Debenture'));
  },
  insurances() {
    return this.products.filter(product => product[1].includes('Insurance'));
  }
},

  methods: {
    /*
    connect() {
      this.ws = new WebSocket('ws://localhost:5001');   // connect to server
      
      // listen to server
      this.ws.onmessage = (event) => {
        this.messages.push('You: ' + this.newMessage);
        // receive and show the response from the model
        this.messages.push('AI: ' + data.reply);
      };

      // can listen to other WebSocket events (open, error, close, ...
      this.ws.onopen = () => console.log('Connected to the server');
      this.ws.onerror = (error) => console.error('WebSocket error:', error);
      this.ws.onclose = () => console.log('Disconnected from the server');
    },*/

    sendMessage() {
      
      if (this.newMessage.trim() !== '') {
        // show user message immediately
        this.messages.push({
          text: this.newMessage,
          source: 'User'
        });

        // create data sending to backend
        const postData = {message: this.newMessage};
        this.newMessage = '';   // clear the input area
        
        // use fetch API to send request
        fetch('http://localhost:5000/chat', {
          // match the URL with the Flask application
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(postData),
        })
        .then(response => response.json())
        .then(data => {
          // Add AI response when it arrives
          this.messages.push({
            text: data.reply,
            source: 'AI'
          });
        })
        .catch((error) => {
          console.error('Error:', error);
        });

    }

    /*
    // send message to Server via WebSocket connection
    if (this.ws && this.message) {
        this.ws.send(this.message);
        this.message = '';          // clear input texts
    }*/
  },

  beforeDestroy() {
    if (this.ws) {
      this.ws.close();
    }
  },

    showProducts(type) {
      switch (type) {
        case 'Fund':
          this.showModalF = true;
          break;
        case 'Debenture':
          this.showModalD = true;
          break;
        case 'Insurance':
          this.showModalI = true;
          break;
      }
      //alert('Showing products for: ' + type + '\n' + this.products[type].join('\n'));
    },
    showExplanation() {
      this.showModalE = true;
    },
    closeModal() {
      this.showModalE = false;
      this.showModalF = false;
      this.showModalD = false;
      this.showModalI = false;
    }
  }
};
</script>

<style scoped>
  .container {
    display: flex;
    /*justify-content: center;    /* paralise centre */
    /*align-items: center;        /* vertical centre */
    /*height: 80vh;          /* modify according to need */
    padding: 20px;
    align-items: flex-start;  /* assure sub items at same top */
  }

  .chat-section {
    /* keep sum of all section flex = 100% */
    width: 60%;
    flex: 60%;
    border-right: 2px solid #ddd;
    padding-right: 150px;
    display: flex;
    flex-direction: column;
  }
  .chat-section .message-input {
    display: flex;
    margin-top: 10px;
  }
  .chat-section .message-input input[type="text"] {
    flex-grow: 1;
    border: 2px solid #ddd;
    padding: 10px;
    margin-right: 10px;
    height: 100px;
    white-space: pre-wrap;       /* allow to change to next line automatically */
    overflow-wrap: break-word;   /* change to next line inside the long word or URL */
  }
  .chat-section .message-input button {
    padding: 10px 20px;
    font-size: 20px;
    background-color: #45a5ff;
    color: white;
    border: 2px solid #ddd;
    cursor: pointer;
    height: 60px;
  }
  .chat-section .message-input button:hover {
    background-color: #3ec5be;
  }

  .buttons-section {
    flex: 20%;
    padding-left: 150px;
    display: flex;
    flex-direction: column; /* stock elements virtically */
    align-items: center;    /* keep elements at the same horizon and center axis virtically */
  }
  .buttons-section button {
    margin-bottom: 15px;
    background-color: #4CAF50;
    color: white;       /* color of words */
    padding: 15px 32px;     /* size of button */
    border: none;
    border-radius: 4px;
    cursor: pointer;      /* shape of cursor when on the button */
    font-size: 24px;
    font-family: Arial, sans-serif;
  }
  .buttons-section button:hover {
    background-color: #45a049;  /* change color when mouse cursor move to here */
  }
  .buttons-section img {
    height: 150px;
    width: 280px;
    margin-right: 5px;  /* distance between img and words */
    margin-bottom: 10px;
  }
  .buttons-section .button-explain button {
    margin-bottom: 15px;
    margin: 15px;
    width: 320px;
    background-color: #c57914;
    color: white;       /* color of words */
    padding: 15px 32px;     /* size of button */
    border: none;
    border-radius: 4px;
    cursor: pointer;      /* shape of cursor when on the button */
    font-size: 30px;
    font-weight: bold;
    font-family: 'Consolas', sans-serif;
  }
  .buttons-section .button-explain button:hover {
    background-color: #ccb97c;
  }

  .message {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  .message-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;  /* make image round */
    object-fit: cover;
    margin-left: 15px;
    margin-right: 15px;
  }

  .messages {
    width: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(253, 251, 246, 0.979);
    height: 620px;
    overflow-y: auto;   /* have scroll when messages history overflow */
    border: 2px solid #3b0808;
    padding: 10px;              /* inner margin */

    margin: 30px 0;           /* up & down margin */
    font-size: 24px; /* Increased font size */
    font-family: 'Arial', sans-serif; /* Changed font family */
    
  }

  .message-input input[type="text"] {
    flex-grow: 1;
    border: 2px solid #ccc;
    padding: 15px; /* Increased padding */
    margin-right: 10px;
    font-size: 24px; /* Increased font size */
    font-family: 'Roboto', sans-serif; /* Changed font family */
  }

  .message-input button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
  }
  .message-input button:hover {
    background-color: #45a049;
  }

  .user-message {
    /* background-color: #DCF8C6; */
    justify-content: flex-end;
    text-align: right;
  }
  .ai-message {
    /* background-color: #ECECEC; */
    justify-content: flex-start;
    text-align: left;
  }
  .user-message .message-container {
    flex-direction: row-reverse;
  }
  .ai-message .message-container {
    flex-direction: row;
  }
  .user-message .text {
  background-color: #DCF8C6;
}
  .ai-message .text {
    background-color: #ECECEC;
  }

  .text {
    padding: 10px;
    background-color: #f1f1f1;
    border-radius: 10px;
    max-width: 70%;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }

  .modal {
    display: none;
    position: fixed;
    z-index: 1;
    padding-top: 100px;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0,0,0);
    background-color: rgba(0,0,0,0.4);
  }

  .modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    font-size: 24px;
  }

  .close {
    position: absolute;
    right: 10px; /* Modify accoring to your design */
    top: 10px;
    color: #aaaaaa;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }
  .close:hover,
  .close:focus {
    color: #000;
    text-decoration: none;
  }
</style>
