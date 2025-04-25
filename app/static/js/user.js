document.addEventListener('DOMContentLoaded', function() {
    const enterBtn = document.getElementById('enter-btn');
    const entrance = document.querySelector('.entrance');
    const addTugriksForm = document.getElementById('addTugriksForm');
    const showAddTugriksBtn = document.getElementById('showAddTugriksForm');
    const closeAddTugriksBtn = document.getElementById('closeAddTugriksForm');

    if (enterBtn && entrance) {
        enterBtn.addEventListener('click', function() {
            entrance.classList.add('open');
            createShatterEffect(enterBtn);

            enterBtn.style.opacity = '0';
            setTimeout(() => enterBtn.style.display = 'none', 300);
        });
    }

    if (showAddTugriksBtn && addTugriksForm && closeAddTugriksBtn) {
        showAddTugriksBtn.addEventListener('click', function() {
            addTugriksForm.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });

        closeAddTugriksBtn.addEventListener('click', function() {
            addTugriksForm.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        addTugriksForm.addEventListener('click', function(e) {
            if (e.target === addTugriksForm) {
                addTugriksForm.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }
});

function createShatterEffect(button) {
    const rect = button.getBoundingClientRect();
    const pieces = 8;
    const rows = 4;
    const pieceWidth = rect.width / pieces;
    const pieceHeight = rect.height / rows;

    const style = window.getComputedStyle(button);
    const backgroundColor = style.backgroundColor;

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < pieces; j++) {
            const piece = document.createElement('div');
            piece.className = 'button-piece';

            piece.style.position = 'fixed';
            piece.style.left = (rect.left + j * pieceWidth) + 'px';
            piece.style.top = (rect.top + i * pieceHeight) + 'px';
            piece.style.width = pieceWidth + 'px';
            piece.style.height = pieceHeight + 'px';
            piece.style.backgroundColor = backgroundColor;
            piece.style.transition = 'all 1.5s cubic-bezier(0.4, 0.0, 0.2, 1)';

            document.body.appendChild(piece);

            const randomX = (Math.random() - 0.5) * 500;
            const randomY = (Math.random() - 0.5) * 500;
            const randomRotate = (Math.random() - 0.5) * 1080;

            setTimeout(() => {
                piece.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${randomRotate}deg)`;
                piece.style.opacity = '0';
            }, Math.random() * 300);

            setTimeout(() => piece.remove(), 2000);
        }
    }
}