# BankGPT

A chatbot app demo for recommend bank products. Basically it contains 3 parts:

· Back-end LLM fine-tuned. (Folder: back-end)

· Front-end user interface on personal computer,implemented by Vue3 framework. (Folder: Vue)

· Front-end user interface on smart phone, implemented by Android application framework. (Folder: PhoneInterface)

## Back-end

Take DialoGPT (an dialogue style extension of GPT-2) as the target model to be trained.

##### DialoGPT_finetuning_Chatbot.ipynb: 
The program for fine-tuning and testing model, referred the project [0xrushi/DialoGPT-Finetune](https://github.com/0xrushi/DialoGPT-Finetune), which originally train LLM to answer medical-related questions; and the [Nathan Cooper finetuning Dialogflow](https://nathancooper.io/i-am-a-nerd/chatbot/deep-learning/gpt2/2020/05/12/chatbot-part-1.html), which contains more explanations.

The program was run via 

## Front-end

Panels and chatting box displayed for the user to view and type things to interact with the chatbot.

### PC terminal

Based on Vue3 (via VSCode), the layout and components referred the project [Tsk-Andrey078/gptVue](https://github.com/Tsk-Andrey078/gptVue).

More information about how to implement Vue could be find in the relevant parts in both the reference and this repository.

### Android phone terminal

(Could work on phone with Harmony OS as well.)

