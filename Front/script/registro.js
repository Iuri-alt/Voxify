(() => {
  const form = document.querySelector("[data-register-form]");
  const message = form?.querySelector(".mensagem-formulario");

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const password = document.querySelector("#senha-registro").value;
    const confirmation = document.querySelector("#confirmar-senha").value;
    const button = form.querySelector("button[type='submit']");
    message.textContent = "";

    if (password !== confirmation) {
      message.textContent = "As senhas precisam ser iguais.";
      document.querySelector("#confirmar-senha").focus();
      return;
    }

    button.disabled = true;
    button.textContent = "Criando conta...";
    try {
      await registrar(
        document.querySelector("#nome").value.trim(),
        document.querySelector("#email-registro").value.trim(),
        password
      );
      window.location.assign("login.html");
    } catch (error) {
      message.textContent = error.message;
    } finally {
      button.disabled = false;
      button.textContent = "Criar conta";
    }
  });
})();
