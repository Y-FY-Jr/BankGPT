<template>
    <div class="container main-block">
        <div class="row">
            <div class="col-3">
                <ul v-for="(item, index) in news" class="list-group">
                    <li class="list-group-item">{{ index }} -  {{ item.substring(0, 20) }}</li>
                </ul>
            </div>
            <div class="col-9">
                
                <div class="mb-3">
                    <span class="badge text-bg-success">Overview</span>
                    <div class="spinner-border text-success" role="status" id="load-circle">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div style="display: inline-block">What is passed to ChatGPT: <i>Provide me with the main points of the news in 3-4 sentences and highlight key individuals, players, companies, etc. in the news</i></div>
                    <div for="Textarea2" class="form-label">Input:</div>
                    <textarea class="form-control" id="Textarea1" rows="10"></textarea>
                    <button type="button" class="btn btn-success btn-control" @click="add_text">Add news</button>
                    <button type="button" class="btn btn-success btn-control" style="margin-left: 10px;" @click="clear">Clear:</button>
                </div>
                <div class="mb-3">
                    <label for="Textarea2" class="form-label">Output:</label>
                    <textarea class="form-control" id="Textarea2" rows="10"></textarea>
                    <button type="button" class="btn btn-success btn-control" @click="prepare_data">Run</button>
                </div>
            </div>
            <button type="button" class="btn btn-info btn-help" data-bs-toggle="modal" data-bs-target="#exampleModal">
                Information & Explanation
            </button>
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Summary</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Overview - is a tool with which you can highlight the main points in your news and extract key figures from the text (if possible). The input for the GPT language model is a special query expression: <b>"Provide me with the main points of the news in 3-4 sentences and highlight key figures, players, companies, etc. in the news."</b> Which is applied to each entered news. <br>
                        The list of news can be observed on the left panel.
                        <br><br>
                        The "Input" field is intended for entering the text of the news. <br>
                        The "Add News" button adds the text of the news to the list.<br>
                        The "Clear" button clears the list of news and the input field. <br>
                        The "Run" button will send your news to GPT and generate a response.
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    
    import { Configuration, OpenAIApi } from "openai"
    const configuration = new Configuration({
        apiKey: "",
    });
    let prepared_data = ""
    const openai = new OpenAIApi(configuration);

    export default{
        data() {
            return {
                news: [
                ]
            }
        },
        methods: {
            clear() {
                const textArea = document.getElementById("Textarea1")
                textArea.value = ""
                this.news = []
            },
            add_text() {
                const textArea = document.getElementById("Textarea1")
                let temp = textArea.value
                if (temp == "") {
                    alert("Attention! You haven't entered any text!")
                    return 0
                }
                this.news.push(temp)
                textArea.value = ""
            },
            async prepare_data() {
                if (this.news.length == 0) {
                    alert("Attention! You haven't added any news!")
                    return 0
                }
                prepared_data = "\n"
                const load_elem = document.getElementById("load-circle")
                load_elem.style.display = "inline-block"
                for(let element of this.news) {
                    const completion = await openai.createChatCompletion({
                        model: "gpt-3.5-turbo",
                        messages: [
                            {'role': 'system', 'content': 'You are an assistant for the monitoring system. You must highlight the main thing from the provided news and state it in 3-4 sentences and highlight key persons, players, companies, etc. from the news. Output format - SUMMARY: , KEY_PERSONS_AND_COMPANYS: . Output make on English language'},
                            {'role': 'user', 'content': 'Provide me with the main points of the news in 3-4 sentences and highlight key individuals, players, companies, etc. in the news.'},
                            {'role': 'user', 'content': 'The presented news: ' + element}
                        ],
                    });
                    console.log(completion.data.choices[0].message.content)
                    prepared_data = prepared_data + "\n\n" + completion.data.choices[0].message.content + "\n\n================================"
                }
                load_elem.style.display = "none"
                const textArea2 = document.getElementById("Textarea2")
                textArea2.value = prepared_data
            }
        },
        mounted() {
            
        },
    }
</script>

<style>
.btn-help {
    margin: 0 auto;
    margin-top: 30px;
    max-width: 20%;
}
#load-circle {
    display: none;
}
.main-block {
    margin-top: 50px;
}
.btn-control {
    margin-top: 20px;
}
</style>