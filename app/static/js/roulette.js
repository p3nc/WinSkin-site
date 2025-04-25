const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const spinButton = document.getElementById('spin-button');
const resultMessage = document.getElementById('result-message');
let currentCaseId = 'case1';
const SPIN_COST = 100;

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

const caseImages = {
    'case1': '/static/images/Case1_Revolution/Case1.png',
    'case2': '/static/images/Case2_Rebellion/case-image.png',
    'case3': '/static/images/Case3_Retaliation/case-image.png'
};

const caseCollections = {
    'case1': 'Revolution',
    'case2': 'Rebellion',
    'case3': 'Retaliation'
};

async function loadSkinsForCase(caseId) {
    try {
        const collection = caseCollections[caseId];
        const response = await fetch(`/roulette/get_skins/${collection}`);
        const data = await response.json();
        return data.skins;
    } catch (error) {
        console.error('Error loading skins:', error);
        return [];
    }
}

function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    const difference = end - start;

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const currentValue = Math.floor(start + difference * progress);
        element.textContent = currentValue;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

spinButton.addEventListener('click', async () => {
    try {
        const response = await fetch('/roulette/spin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Помилка при крутінні рулетки');
            return;
        }

        const balanceElement = document.querySelector('.balance-amount');
        if (balanceElement) {
            const currentBalance = parseInt(balanceElement.textContent.replace(/\D/g, ''));
            const newBalance = currentBalance - SPIN_COST;

            balanceElement.style.transition = 'color 0.3s ease';
            balanceElement.style.color = '#ff4444';

            animateNumber(balanceElement, currentBalance, newBalance, 500);

            setTimeout(() => {
                balanceElement.style.color = '';
            }, 300);
        }

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

    } catch (error) {
        console.error('Error:', error);
        alert('Помилка при крутінні рулетки');
    }
});

async function determineWinner(angle) {
    angle = 360 - angle;
    let winningSegment = null;

    for (let { start, end, segment } of segmentAngles) {
        if (angle >= start && angle < end) {
            winningSegment = segment;
            break;
        }
    }

    const skins = await loadSkinsForCase(currentCaseId);
    const matchingSkins = skins.filter(skin =>
        skin.rarity.toLowerCase() === winningSegment.color.toLowerCase()
    );
    const randomSkin = matchingSkins[Math.floor(Math.random() * matchingSkins.length)];

    resultMessage.textContent = `Вітаю! Ви отримали скін "${randomSkin.name}"`;

    const skinImageDiv = document.getElementById('won-skin-image');
    skinImageDiv.innerHTML = `
        <img src="${randomSkin.photo}"
             alt="${randomSkin.name}"
             style="max-width: 200px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); margin-top: 10px;">
    `;

    try {
        await fetch('/roulette/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: randomSkin.name,
                rarity: randomSkin.rarity,
                image: randomSkin.photo
            })
        });
    } catch (error) {
        console.error('Error saving won skin:', error);
    }
}

async function showCaseSkins(caseId) {
    currentCaseId = caseId;
    document.getElementById('case-image').src = caseImages[caseId];

    const skinsTable = document.getElementById('skins-table');
    skinsTable.innerHTML = '';

    const skins = await loadSkinsForCase(caseId);
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
                cell.innerHTML = `
                    <div style="padding: 10px;">
                        <img src="${skin.photo}" alt="${skin.name}">
                        <div class="skin-name">${skin.name}</div>
                    </div>
                `;
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    showCaseSkins('case1');
    spinButton.textContent = `Spin (${SPIN_COST} ₮)`;
});
