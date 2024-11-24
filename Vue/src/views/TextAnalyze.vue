<template>
    <div class="container main-block">
        <div class="row">
            <div class="col-12">
                <div class="mb-3">
                    <span class="badge text-bg-success">News Analysis</span>
                    <div class="dropdown dropdown_inline">
                        <button class="btn btn-success dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Condition
                        </button>
                        <ul class="dropdown-menu">
                            <li><button class="dropdown-item" @click="change_condition('Business')">Business</button></li>
                            <li><button class="dropdown-item" @click="change_condition('Government')">Government</button></li>
                            <li><button class="dropdown-item" @click="change_condition('Security Forces')">Security Forces</button></li>
                            <li><button class="dropdown-item" @click="change_condition('Various Perspectives')">Various Perspectives</button></li>
                        </ul>
                        <input class="form-control" type="text" v-model="input">
                    </div>
                    <div class="cond">What is passed to ChatGPT: <i>Provide me with a detailed analysis of this news from a {{ this.condition }} perspective</i></div>
                    <div class="spinner-border text-success" role="status" id="load-circle">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div for="Textarea2" class="form-label">Input:</div>
                    <textarea class="form-control" id="Textarea1" rows="10"></textarea>
                    <button type="button" class="btn btn-success btn-control" @click="push_news">Start</button>
                    <button type="button" class="btn btn-success btn-control" style="margin-left: 10px;" @click="clear">Clear</button>
                </div>
                <div class="mb-3">
                    <label for="Textarea2" class="form-label">Output:</label>
                    <textarea class="form-control" id="Textarea2" rows="10"></textarea>
                </div>
                <button type="button" class="btn btn-info btn-help" data-bs-toggle="modal" data-bs-target="#exampleModal">
                    Information and Explanation
                </button>
                <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">News Analysis</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            News analysis is a tool that allows you to get a detailed analysis of the news from an Artificial Intelligence perspective. You provide an expression - a request: <b>"Provide me with a detailed analysis of this news from a + {{ this.condition }} perspective"</b> In the <b>"Condition"</b> tab, you can choose a perspective.
                            <br><br>
                            "Business" - from a business perspective.<br>
                            "Government" - from a government perspective.<br>
                            "Security Forces" - from the perspective of security forces.<br>
                            "Various Perspectives" - from various perspectives.
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
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
                condition: "",
                input: ""
            }
        },
        methods: {
            clear() {
                const textArea = document.getElementById("Textarea1")
                textArea.value = ""
            },
            change_condition(statement) {
                if (statement == "Business") {this.condition = "from a Business perspective"} 
                if (statement == "Government") {this.condition = "from a Government perspective"} 
                if (statement == "Security Forces") {this.condition = "from a Security Forces perspective"} 
                if (statement == "Various Perspectives") {this.condition = "from Various Perspectives"} 
            },
            async push_news() {
                if (this.input.length > 0) {
                    this.condition = this.input
                    console.log(this.input)
                }

                if (this.condition == "") {
                    alert("Attention! You have not selected a condition!")
                    return 0
                }
                const textArea = document.getElementById("Textarea1")
                let temp = textArea.value

                if (temp == "") {
                    alert("Attention! You have not entered text!")
                    return 0
                }
                
                if (this.input.length > 0) {
                    this.condition = this.input
                }

                const load_elem = document.getElementById("load-circle")
                load_elem.style.display = "inline-block"
                const textArea2 = document.getElementById("Textarea2")

                const completion = await openai.createChatCompletion({
                    model: "gpt-3.5-turbo",
                    messages: [
                        {'role': 'system', 'content': 'You are an assistant for the monitoring system. You must give your own analysis of the presented news.'},
                        {'role': 'user', 'content': 'Provide me with a detailed analysis of this news. ' + this.condition},
                        {'role': 'user', 'content': 'The presented news: ' + temp}
                    ],
                });
                textArea2.value = completion.data.choices[0].message.content
                load_elem.style.display = "none"
            },
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
.cond {
    display: inline-block;
    margin-left: 15px;
}
.dropdown_inline {
    margin-left: 10px;
    display: inline-block;
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
