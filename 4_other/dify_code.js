function main() {
  const container = document.createElement("div");
  const message = document.createElement("p");
  message.textContent =
    "Olá! Ao utilizar este chat, você concorda com os termos do Aviso Legal";
  const agreeButton = document.createElement("button");
  agreeButton.textContent = "Concordo";
  const disagreeButton = document.createElement("button");
  disagreeButton.textContent = "Não concordo";
  container.appendChild(message);
  container.appendChild(agreeButton);
  container.appendChild(disagreeButton);
  document.body.appendChild(container);

  agreeButton.addEventListener("click", function () {
    container.style.display = "none";
    // Code to enable chat interaction goes here
  });

  disagreeButton.addEventListener("click", function () {
    container.style.display = "none";
    alert("Você deve concordar com os termos para usar o chat.");
  });

  return {
    result: "UI created",
  };
}
