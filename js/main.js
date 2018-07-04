// Objeto para configuração do firebase, padrão da framework
function configFirebase(){
	var config = {
		apiKey: "AIzaSyC85BRgXdhXnpFkqPzzA1K4PdM4Q4ApvT4",
		authDomain: "eng-soft-f1c51.firebaseapp.com",
		databaseURL: "https://eng-soft-f1c51.firebaseio.com",
		projectId: "eng-soft-f1c51",
		storageBucket: "eng-soft-f1c51.appspot.com",
		messagingSenderId: "1041024483165"
	};

	firebase.initializeApp(config);
}

/* 
Pega os nós contidos no nó 'events' do firebase 
e roda a função parseEvent para cada um deles
*/

	
function getEvents(){
	var db = firebase.database();

    // Pega a referência do /events no firebase
	var leadsRef = db.ref('events');
	
    /*
    Eu não lembro o porque dessa coisa estar aqui, vou deixar
    comentado pois pode ser útil no futuro 
    */

    /*
    leadsRef.on('value', function(snapshot) {
		snapshot.forEach(function(childSnapshot) {
		  var childData = childSnapshot.val();
		});
	});
    */
	
	/*
    // Quando carregar um nó filho do firebase
	leadsRef.on('child_added', function(snapshot) {
        // Faz parse para JSON e processa a bagaça
        parseEvent(JSON.parse(snapshot._e.T));
	});*/
	
	firebase.database().ref('/events').on('child_added', function(snapshot) {
<<<<<<< HEAD
		var algo = JSON.stringify(snapshot.val());
		algo = JSON.parse(algo);
		for (x in algo) {
			console.log(algo[x]);
			parseEvent(algo[x]);
=======
		var addedEvent = JSON.stringify(snapshot.val());
		addedEvent = JSON.parse(addedEvent);
		for (key in addedEvent) {
			console.log(addedEvent[key]);
			parseEvent(addedEvent[key]);
>>>>>>> master
		}
	});
}

/*
    Pega o JSON retornado do firebase e cria um HTML node a partir dele.
    Dá append no nó #wrapper contido na página
*/

function parseEvent(json){
    var card = document.createElement('div');

    // Link do evento
    card.href = json['href'];
    card.target = "_blank";
    card.classList.add('card');

    // Imagem do evento
    var img = document.createElement('img');
    img.src = json['img'];
    card.appendChild(img);

    // Título
    var title = document.createElement('h2');
    title.textContent = json['title'];
    card.appendChild(title);
    title.classList.add('title');

    // Data
    // * Precisa fazer um parsing disso depois
    var date = document.createElement('p');
    date.textContent = json['date'];
    card.appendChild(date);

    // Tags do evento
    var tags = document.createElement('p');
    tags.textContent = "tags: " + json['tags'];
    card.appendChild(tags);

    // Enfia no HTML
    document.querySelector('#wrapper').appendChild(card);
}


/* Função de setup que configura o firebase e pega os eventos */
function setup(){
    configFirebase();
    getEvents();
}

// Só roda essa função quando a página estiver carregada
window.onload = setup;