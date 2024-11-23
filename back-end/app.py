from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, GPT2Config, GPT2LMHeadModel
import os, socket
from flask_cors import CORS
from threading import Thread


""" This is the backend for the user interface at the PC terminal. 
Use Flask to realize communication. """

app = Flask(__name__)
CORS(app)  # allow  request across domains


# get the absolute path of this program
current_script_path = os.path.abspath(__file__)
chatbot_path = os.path.join(current_script_path, '..', 'model_chatbot')
sandbox_path = os.path.join(current_script_path, '..', 'model_sandbox')
print(chatbot_path)



def response(data):
    tokenizer_chatbot = AutoTokenizer.from_pretrained(chatbot_path, padding_side='left')
    model_chatbot = AutoModelForCausalLM.from_pretrained(chatbot_path)

    # encode each query as a token ID, add a sign <EOS>, output is a PyTorch tensor
    bot_input_ids = tokenizer_chatbot.encode(data + tokenizer_chatbot.eos_token, return_tensors='pt')
    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model_chatbot.generate(
        bot_input_ids, max_length=100,
        pad_token_id=tokenizer_chatbot.eos_token_id,
        no_repeat_ngram_size=3,       
        do_sample=True, 
        top_k=10, 
        top_p=0.7,
        temperature = 0.8
    )
    # decode the response stored in 'chat_history_ids' into readable text, skip 'beginning','ending',...
    reply = tokenizer_chatbot.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    #inputs = tokenizer.encode(data['message'], return_tensors='pt')
    #outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    #reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #reply = 'here'
    return reply


'''
def response(data):
    tokenizer_sandbox = AutoTokenizer.from_pretrained(sandbox_path, padding_side='left', vocab_file=sandbox_path+'/vocab.json')
    model_sandbox = AutoModelForCausalLM.from_pretrained(sandbox_path)
    # encode each query as a token ID, add a sign <EOS>, output is a PyTorch tensor
    bot_input_ids = tokenizer_sandbox.encode(data + tokenizer_sandbox.eos_token, return_tensors='pt')
    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model_sandbox.generate(
        bot_input_ids, max_length=200,
        pad_token_id=tokenizer_sandbox.eos_token_id,
        no_repeat_ngram_size=3,       
        do_sample=True, 
        top_k=10, 
        top_p=0.7,
        temperature = 0.8
    )

    # decode the response stored in 'chat_history_ids' into readable text, skip 'beginning','ending',...
    reply = tokenizer_sandbox.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    if reply == '&&&&':
        return 'Sorry, but there might be something sensitive in your words. Please avoid using suspicious meaning.'
    elif reply == '****':
        return 'Attention, I think you are leaking out personal privacy by mistake. Please avoid doing that.'
    return reply
'''


'''
def response(data):
    # firstly let sandbox to check
    bot_input_ids = tokenizer_sandbox.encode(data + tokenizer_sandbox.eos_token, return_tensors='pt')
    chat_history_ids = model_sandbox.generate(
      bot_input_ids, max_length=100,
      pad_token_id=tokenizer_sandbox.eos_token_id,
      no_repeat_ngram_size=3,       
      do_sample=True, 
      top_k=10, 
      top_p=0.7,
      temperature = 0.8
    )
    reply = tokenizer_sandbox.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    if reply == '&&&&':
        return 'Sorry, but there might be something sensitive in your words. Please avoid using suspicious meaning.'
    elif reply == '****':
        return 'Attention, I think you are leaking out personal privacy by mistake. Please avoid doing that.'
    else:
        # encode each query as a token ID, add a sign <EOS>, output is a PyTorch tensor
        bot_input_ids = tokenizer_chatbot.encode(data + tokenizer_chatbot.eos_token, return_tensors='pt')
        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model_chatbot.generate(
            bot_input_ids, max_length=100,
            pad_token_id=tokenizer_chatbot.eos_token_id,
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=10, 
            top_p=0.7,
            temperature = 0.8
        )
        # decode the response stored in 'chat_history_ids' into readable text, skip 'beginning','ending',...
        reply = tokenizer_chatbot.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        #inputs = tokenizer.encode(data['message'], return_tensors='pt')
        #outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
        #reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        #reply = 'here'
        return reply
        '''

@app.route('/')
def hello_world():
    app.logger.info()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # print(data):   {'message': 'texts of user'}
    print('message:', data['message'])
    reply = response(data['message'])
    print('reply:', reply)
    return jsonify({'reply': reply})


def start_socket_server():
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Listening on {host}:{port}...')

    while True:
        client_socket, address = server_socket.accept()
        print(f'Accepted connection from {address}')
        message = client_socket.recv(1024).decode('utf-8')
        print('message:', message)
        reply = response(message)
        print('reply:', reply)
        client_socket.sendall(reply.encode('utf-8'))
        client_socket.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
