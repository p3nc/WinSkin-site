const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const spinButton = document.getElementById('spin-button');
const resultMessage = document.getElementById('result-message');

let currentCaseId = 'case1';

const segments = [
    { color: 'blue', text: '', probability: 50 },
    { color: 'green', text: '', probability: 20 },
    { color: 'purple', text: '', probability: 15 },
    { color: 'pink', text: '', probability: 10 },
    { color: 'red', text: '', probability: 4 },
    { color: 'yellow', text: '', probability: 1 }
];

let totalAngle = 0;
let segmentAngles = [];

segments.forEach(segment => {
    const angle = (segment.probability / 100) * 360;
    drawSegment(totalAngle, totalAngle + angle, segment.color, segment.text);
    segmentAngles.push({ start: totalAngle, end: totalAngle + angle, segment });
    totalAngle += angle;
});

function drawSegment(startAngle, endAngle, color, label) {
    const cx = 200, cy = 200, radius = 200;
    const start = degToRad(startAngle);
    const end = degToRad(endAngle);

    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, start, end);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.stroke();
    ctx.closePath();

    const midAngle = (startAngle + endAngle) / 2;
    const textAngle = degToRad(midAngle);
    const textX = cx + Math.cos(textAngle) * 140;
    const textY = cy + Math.sin(textAngle) * 140;

    ctx.save();
    ctx.translate(textX, textY);
    ctx.rotate(textAngle);
    ctx.fillStyle = 'white';
    ctx.font = '16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(label, 0, 0);
    ctx.restore();
}


function degToRad(deg) {
    return deg * (Math.PI / 180);
}
spinButton.addEventListener('click', () => {
    const totalTime = 5000;
    let startTime = performance.now();
    let currentAngle = Math.random() * 360;
    let speed = 7.2;

    function animate(currentTime) {
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / totalTime, 1);
        speed = 7.2 * (1 - progress);
        currentAngle += (speed / 1000) * (currentTime - startTime);
        currentAngle %= 360;
        canvas.style.transform = `rotate(${currentAngle}deg)`;

        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            determineWinner(currentAngle);
        }
    }

    requestAnimationFrame(animate);
});


function determineWinner(angle) {
    angle = 360 - angle;
    let winningSegment = null;

    for (let { start, end, segment } of segmentAngles) {
        if (angle >= start && angle < end) {
            winningSegment = segment;
            break;
        }
    }

    const allSkins = skinsData[currentCaseId];
    const matchingSkins = allSkins.filter(skin => skin.rarity === winningSegment.color);
    const randomSkin = matchingSkins[Math.floor(Math.random() * matchingSkins.length)];

    resultMessage.textContent = `Вітаю! Ви отримали скин "${randomSkin.name}"`;

    const skinImageDiv = document.getElementById('won-skin-image');
    skinImageDiv.innerHTML = `<img src="${randomSkin.image}" alt="${randomSkin.name}" style="max-width: 200px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); margin-top: 10px;">`;
}


const caseImages = {
    'case1': '/static/images/Case1_Revolution/Case1.png',
    'case2': '/static/images/Case2_Rebellion/case-image.png',
    'case3': '/static/images/Case3_Retaliation/case-image.png'
};


const skinsData = {
    'case1': [
        { rarity: 'blue', image: '/static/images/Case1_Revolution/SkinBlue1.png', name: 'Cyberforce' },
        { rarity: 'blue', image: '/static/images/Case1_Revolution/SkinBlue2.png', name: 'Fragments' },
        { rarity: 'blue', image: '/static/images/Case1_Revolution/SkinBlue3.png', name: 'Insomnia' },
        { rarity: 'blue', image: '/static/images/Case1_Revolution/SkinBlue4.png', name: 'Re.built' },
        { rarity: 'blue', image: '/static/images/Case1_Revolution/SkinBlue5.png', name: 'Rebel' },
        { rarity: 'green', image: '/static/images/Case1_Revolution/SkinGreen6.png', name: 'Featherweight' },
        { rarity: 'green', image: '/static/images/Case1_Revolution/SkinGreen7.png', name: 'Liquidation' },
        { rarity: 'green', image: '/static/images/Case1_Revolution/SkinGreen8.png', name: 'Sakkaku' },
        { rarity: 'purple', image: '/static/images/Case1_Revolution/SkinPurple9.png', name: 'Neoqueen' },
        { rarity: 'purple', image: '/static/images/Case1_Revolution/SkinPurple10.png', name: 'Umbral Rabbit' },
        { rarity: 'pink', image: '/static/images/Case1_Revolution/SkinPink11.png', name: 'Banana Cannon' },
        { rarity: 'pink', image: '/static/images/Case1_Revolution/SkinPink12.png', name: 'Emphorosaur-S' },
        { rarity: 'red', image: '/static/images/Case1_Revolution/SkinRed13.png', name: 'Duality' },
        { rarity: 'red', image: '/static/images/Case1_Revolution/SkinRed14.png', name: 'Head Shot' },
        { rarity: 'yellow', image: '/static/images/Case1_Revolution/SkinYellow15.png', name: 'Sport Gloves' }
    ],
    'case2': [
        { rarity: 'blue', image: 'path/to/case2/skin1.jpg' },
        { rarity: 'blue', image: 'path/to/case2/skin2.jpg' },
        { rarity: 'blue', image: 'path/to/case2/skin3.jpg' },
        { rarity: 'blue', image: 'path/to/case2/skin4.jpg' },
        { rarity: 'blue', image: 'path/to/case2/skin5.jpg' },
        { rarity: 'green', image: 'path/to/case2/skin6.jpg' },
        { rarity: 'green', image: 'path/to/case2/skin7.jpg' },
        { rarity: 'green', image: 'path/to/case2/skin8.jpg' },
        { rarity: 'purple', image: 'path/to/case2/skin9.jpg' },
        { rarity: 'purple', image: 'path/to/case2/skin10.jpg' },
        { rarity: 'pink', image: 'path/to/case2/skin11.jpg' },
        { rarity: 'pink', image: 'path/to/case2/skin12.jpg' },
        { rarity: 'red', image: 'path/to/case2/skin13.jpg' },
        { rarity: 'red', image: 'path/to/case2/skin14.jpg' },
        { rarity: 'yellow', image: 'path/to/case2/skin15.jpg' }
    ],
    'case3': [
        { rarity: 'blue', image: 'path/to/case3/skin1.jpg' },
        { rarity: 'blue', image: 'path/to/case3/skin2.jpg' },
        { rarity: 'blue', image: 'path/to/case3/skin3.jpg' },
        { rarity: 'blue', image: 'path/to/case3/skin4.jpg' },
        { rarity: 'blue', image: 'path/to/case3/skin5.jpg' },
        { rarity: 'green', image: 'path/to/case3/skin6.jpg' },
        { rarity: 'green', image: 'path/to/case3/skin7.jpg' },
        { rarity: 'green', image: 'path/to/case3/skin8.jpg' },
        { rarity: 'purple', image: 'path/to/case3/skin9.jpg' },
        { rarity: 'purple', image: 'path/to/case3/skin10.jpg' },
        { rarity: 'pink', image: 'path/to/case3/skin11.jpg' },
        { rarity: 'pink', image: 'path/to/case3/skin12.jpg' },
        { rarity: 'red', image: 'path/to/case3/skin13.jpg' },
        { rarity: 'red', image: 'path/to/case3/skin14.jpg' },
        { rarity: 'yellow', image: 'path/to/case3/skin15.jpg' }
    ]
};


function showCaseSkins(caseId) {
    currentCaseId = caseId;

    document.getElementById('case-image').src = caseImages[caseId];

    const skinsTable = document.getElementById('skins-table');
    skinsTable.innerHTML = '';

    const skins = skinsData[caseId];
    const columns = 3;
    const rows = 5;

    for (let rowIndex = 0; rowIndex < rows; rowIndex++) {
        const row = skinsTable.insertRow();
        for (let colIndex = 0; colIndex < columns; colIndex++) {
            const skinIndex = rowIndex + colIndex * rows;
            const skin = skins[skinIndex];
            const cell = row.insertCell();

            if (skin) {
                cell.style.backgroundColor = skin.rarity;
                cell.innerHTML = `<img src="${skin.image}" alt="${skin.rarity} skin">`;
            } else {
                cell.innerHTML = '';
            }
        }
    }
}



