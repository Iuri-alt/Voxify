(() => {
  const input = document.querySelector("#fileInput");
  const area = document.querySelector("[data-upload-area]");
  const button = document.querySelector("[data-file-button]");
  const message = document.querySelector("[data-upload-message]");
  const allowed = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/x-m4a", "audio/mp4"];

  const setMessage = (text) => { message.textContent = text; };
  const submitFile = async (file) => {
    if (!file) return;
    if (!allowed.includes(file.type) && !/\.(mp3|wav|m4a)$/i.test(file.name)) return setMessage("Selecione um arquivo MP3, WAV ou M4A.");
    if (file.size > 100 * 1024 * 1024) return setMessage("O arquivo deve ter no máximo 100 MB.");

    const formData = new FormData();
    formData.append("arquivo", file);
    button.disabled = true;
    setMessage("Enviando e transcrevendo o áudio...");
    try {
      const response = await api("/arquivos/upload", { method: "POST", body: formData });
      if (!response.ok) throw new Error(await getApiError(response, "Não foi possível enviar o áudio."));
      const data = await response.json();
      setMessage("Áudio processado com sucesso.");
      if (data.texto) {
        const textArea = document.querySelector("#texto");
        textArea.value = data.texto;
        textArea.dispatchEvent(new Event("input"));
      }
      await carregarArquivos();
    } catch (error) {
      setMessage(error.message);
    } finally {
      button.disabled = false;
      input.value = "";
    }
  };

  button?.addEventListener("click", (event) => { event.stopPropagation(); input.click(); });
  area?.addEventListener("click", () => input.click());
  area?.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") { event.preventDefault(); input.click(); }
  });
  input?.addEventListener("change", () => submitFile(input.files[0]));
  ["dragenter", "dragover"].forEach((type) => area?.addEventListener(type, (event) => { event.preventDefault(); area.classList.add("dragover"); }));
  ["dragleave", "drop"].forEach((type) => area?.addEventListener(type, (event) => { event.preventDefault(); area.classList.remove("dragover"); }));
  area?.addEventListener("drop", (event) => submitFile(event.dataTransfer.files[0]));
})();
