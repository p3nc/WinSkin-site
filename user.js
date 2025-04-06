document.getElementById("enter-btn").addEventListener("click", () => {
  const entrance = document.querySelector(".entrance");
  entrance.classList.add("open");

  setTimeout(() => {
    window.location.href = "user.html";
  }, 1200); // Після завершення анімації
});