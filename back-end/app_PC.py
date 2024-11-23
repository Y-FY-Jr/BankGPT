from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import multiprocessing
from multiprocessing import Process, Queue
from flask_cors import CORS

app = Flask(__name__)
CORS(app)               # allow inter-domains request

# get the absolute path of this program
current_script_path = os.path.abspath(__file__)
chatbot_path = os.path.join(current_script_path, '..', 'model_chatbot')
sandbox_path = os.path.join(current_script_path, '..', 'model_sandbox')


def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side='left')
    model = AutoModelForCausalLM.from_pretrained(model_path)
    return tokenizer, model


def model_handler(model_path, input_queue, output_queue):
    tokenizer, model = load_model(model_path)
    while True:
        message = input_queue.get()
        if message == "shutdown":
            break
        encoded_input = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
        outputs = model.generate(encoded_input, max_length=200)
        reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        output_queue.put(reply)


def start_model_process(model_path):
    input_queue = Queue()
    output_queue = Queue()
    process = Process(target=model_handler, args=(model_path, input_queue, output_queue))
    process.start()
    return input_queue, output_queue, process


def get_reply(input_queues, output_queues, message):
    input_queues['sandbox'].put(message)
    intermediate_reply = output_queues['sandbox'].get()

    if intermediate_reply in ['&&&&', '****']:
        return intermediate_reply

    input_queues['chatbot'].put(message)
    final_reply = output_queues['chatbot'].get()
    return final_reply


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    reply = get_reply(input_queues, output_queues, data['message'])
    return jsonify({'reply': reply})


if __name__ == '__main__':
    input_queues = {}
    output_queues = {}
    processes = {}

    for model_name, model_path in [('chatbot', chatbot_path), ('sandbox', sandbox_path)]:
        input_queue, output_queue, process = start_model_process(model_path)
        input_queues[model_name] = input_queue
        output_queues[model_name] = output_queue
        processes[model_name] = process

    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Clean up: send shutdown signal to processes
        for queue in input_queues.values():
            queue.put("shutdown")
        for process in processes.values():
            process.join()
