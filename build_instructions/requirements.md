This is a code based of an LLM based customer support agent for Doordash. It will handle customer support cases when the customers did not get their orders, so called "Never Delviered" issue, A.K.A "ND". The customer support agent will call OpenAI APIs using the gpt-4o model through an LLM prompt. 

The process is like the following: 
1. greet the user with a welcome message 
2. ingest user input message and combine the input with previous conversation history, send to openAI LLM API, the API will also have function calls 
3. analyze the LLM response and determine what message and API call to run
4. after API call is completed, send LLM another message as assistant containing the API call results 
5. send all LLM responded messages to the user

The system have the following components: 
1. a GUI with input boxes, see details in interface.md 
2. APIs for LLM, see tools.md
3. an LLM prompt, see prompt.md 
 
Required capabilities: 
1. when the LLM determines which function(s) to call in the response, the system will call the function(s)
2. the system will log the session context, and allows users the manually modify the context and set it by clicking the button
3. the system will show which API did the LLM call in the GUI, show API responses as well



