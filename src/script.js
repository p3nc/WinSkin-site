document.getElementById("loginForm").addEventListener("submit", function(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username === "admin" && password === "password123") {
    alert("Вхід успішний!");
    window.location.href = "dashboard.html";
  } else {
    alert("Неправильний логін або пароль");
  }
});
