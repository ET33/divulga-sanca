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

function getEvents(){
	var db = firebase.database();

	var leadsRef = db.ref('events');
	leadsRef.on('value', function(snapshot) {
		snapshot.forEach(function(childSnapshot) {
		  var childData = childSnapshot.val();
		});
	});

	leadsRef.on('child_added', function(snapshot) {
        parseEvent(JSON.parse(snapshot._e.T));
	});
}

function parseEvent(json){
    var card = document.createElement('div');
    card.href = json['href'];
    card.target = "_blank";
    card.classList.add('card');

    var img = document.createElement('img');
    img.src = json['img'];
    card.appendChild(img);

    var title = document.createElement('h2');
    title.textContent = json['title'];
    card.appendChild(title);
    title.classList.add('title');

    var date = document.createElement('p');
    date.textContent = json['date'];
    card.appendChild(date);

    var tags = document.createElement('p');
    tags.textContent = "tags: " + json['tags'];
    card.appendChild(tags);

    document.querySelector('#wrapper').appendChild(card);
}

function setup(){
    configFirebase();
    getEvents();
}

window.onload = setup;