let helpIndex = 0;
const helpMessages = [
  'Щоб перестати бути гостем і відкрити весь функціонал сайту, перейдіть на вкладку "Реєстрація"',
  'Для перегляду облікового запису та поповнення балансу перейдіть у вкладку "Пентхаус"',
  'Для початку гри перейдіть у вкладку "Рулетка"'
];

function showHelp() {
  const helpDiv = document.getElementById('helpMessage');
  helpDiv.innerText = helpMessages[helpIndex];
  helpIndex = (helpIndex + 1) % helpMessages.length;
}

function placeOrder() {
  const orders = [
    { name: 'Ось ваш Найт-сіті', img: '/static/images/Night-city.png' },
    { name: 'Ось ваш Лас-Вегас', img: '/static/images/Las-vegas.png' },
    { name: 'Ось ваш Сингапур', img: '/static/images/Singapoure.png' },
    { name: 'Ось ваша Вежа', img: '/static/images/Tower.png' }
  ];
  const result = orders[Math.floor(Math.random() * orders.length)];
  const orderDiv = document.getElementById('orderResult');
  orderDiv.innerHTML = `<p>${result.name}</p><img src="${result.img}" alt="${result.name}" style="width:200px; border-radius:10px;">`;
}