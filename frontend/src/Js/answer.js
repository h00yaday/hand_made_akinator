const mockResult = {
    name: "Илон Маск",
    description: "Миллиардер, инженер, филантроп",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/220px-Elon_Musk_Royal_Society_%28crop2%29.jpg"
};

if (answerTitle) {
    answerTitle.innerText = "Я думаю, это... " + mockResult.name;
    
    const photoElement = document.getElementById('character-photo');
    
    if (photoElement) {
        photoElement.src = mockResult.image;
        photoElement.alt = mockResult.name;
    }

    sessionStorage.setItem('akinatorStep', 0);
}