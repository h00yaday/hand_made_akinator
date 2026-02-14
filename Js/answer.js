const mockResult = {
    name: "Илон Маск",
    description: "Миллиардер, инженер, филантроп",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg/220px-Elon_Musk_Royal_Society_%28crop2%29.jpg"
};

if (answerTitle) {
    // 1. Выводим имя
    answerTitle.innerText = "Я думаю, это... " + mockResult.name;
    
    // 2. Выводим фото
    // Ищем наш новый тег <img> по id
    const photoElement = document.getElementById('character-photo');
    
    if (photoElement) {
        // Записываем ссылку из "базы" в атрибут src картинки
        photoElement.src = mockResult.image;
        photoElement.alt = mockResult.name;
    }

    // Сброс игры при уходе
    sessionStorage.setItem('akinatorStep', 0);
}