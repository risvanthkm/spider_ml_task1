const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatWindow = document.getElementById('chat-window');
const loading = document.getElementById('loading')


chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value;
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';

	try{
        show_loading()
        const response = await fetch("http://127.0.0.1:8000/query",
            { 
                method : "POST",
                headers:{
                    "Content-type":"application/json"
                },
                body:JSON.stringify({
                    query:message
                })
            }
        );
        
        const data = await response.json();
        
        addMessage(data.text, "bot");
        clearDynamicContent();
        renderImages(data.images);
        renderTables(data.tables);
        renderSource(data.sources);
    }
    catch(err){
        addMessage(`Fetch failed .. ${err}`, "bot");
    }

    finally{
        hide_loading()
    }
    
});

function show_loading(){
    loading.style.display = "block";
    chatForm.disabled = true;
    userInput.disabled = true;
}

function hide_loading(){
    loading.style.display = "none";
    chatForm.disabled = false;
    userInput.disabled = false;
}

function clearDynamicContent(){
	document.getElementById("tables-container").innerHTML="";
	document.getElementById("images-container").innerHTML="";
    document.getElementById("source").innerHTML = "";
}

function renderImages(images){
	const container = document.getElementById("images-container");
	
	images.forEach(img64=>{
	
		const img = document.createElement("img")
		img.src = `data:image/png;base64,${img64}`;
		img.style.maxWidth = "300px";
        img.style.height="500px";
		container.appendChild(img);
	
	}); 
}

function renderTables(tables){
    const container = document.getElementById("tables-container");

    tables.forEach(table=>{
        const wrapper = document.createElement("div");
        wrapper.className = "table-wrapper";

        wrapper.innerHTML = table
        container.appendChild(wrapper);

    });

}

function renderSource(sources){
    const container = document.getElementById("source");

    container.innerHTML ="";
    sources.forEach(src=>{
        const card = document.createElement("div");
        card.className = "source-card";

        const link = document.createElement('a');
        const basename = src.split(/[/\\]/).pop();
        link.innerText = basename;
        // might be different for windows 
        link.href = `../data/${basename}`;

        card.appendChild(link)
        container.appendChild(card)
    });
    
}


function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('msg', sender);
    
    div.innerHTML = marked.parse(text); 
    
    chatWindow.appendChild(div);
    MathJax.typesetPromise([div]);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
