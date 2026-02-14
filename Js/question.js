const mockQuestions = [
    "Ваш персонаж реальный человек?",
    "Ваш персонаж мужчина?",
    "Ваш персонаж связан с наукой?",
    "У вашего персонажа есть канал на YouTube?"
];



if (questionTitle) {
    if (currentStep >= mockQuestions.length) {
        window.location.href = 'answer.html';
    } else {
        questionTitle.innerText = mockQuestions[currentStep];
    }

    const buttons = document.querySelectorAll('.answer-btn'); 
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            currentStep++;
            sessionStorage.setItem('akinatorStep', currentStep);
            window.location.reload();
        });
    });
}