(() => {
  const form = document.querySelector("[data-login-form]");
  const message = document.querySelector(".mensagem-formulario");

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = form.querySelector("button[type='submit']");
    message.textContent = "";
    button.disabled = true;
    button.textContent = "Entrando...";

    try {
      await login(document.querySelector("#email").value.trim(), document.querySelector("#senha").value);
      window.location.assign("Dashboard.html");
    } catch (error) {
      message.textContent = error.message;
    } finally {
      button.disabled = false;
      button.textContent = "Entrar";
    }
  });
})();
