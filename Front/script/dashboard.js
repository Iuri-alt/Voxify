(() => {
  const list = document.querySelector("[data-audio-list]");
  const textArea = document.querySelector("#texto");
  const counter = document.querySelector("#contador");

  const updateCounter = () => {
    const count = textArea.value.length;
    counter.textContent = `${count} ${count === 1 ? "caractere" : "caracteres"}`;
  };

  const renderFiles = (files) => {
    list.replaceChildren();
    if (!files.length) {
      const empty = document.createElement("p");
      empty.className = "lista-vazia";
      empty.textContent = "Nenhum áudio enviado ainda.";
      list.append(empty);
      return;
    }

    files.forEach((file) => {
      const row = document.createElement("div");
      row.className = "audio_item";
      const name = document.createElement("span");
      name.className = "nome_audio";
      name.textContent = file.nome_do_audio;
      const button = document.createElement("button");
      button.className = "botao_reproduzir";
      button.type = "button";
      button.textContent = "Ver transcrição";
      button.addEventListener("click", () => loadTranscription(file.id));
      row.append(name, button);
      list.append(row);
    });
  };

  window.carregarArquivos = async () => {
    try {
      const response = await api("/arquivos/");
      if (!response.ok) throw new Error(await getApiError(response, "Não foi possível carregar os arquivos."));
      renderFiles(await response.json());
    } catch (error) {
      list.textContent = error.message;
      list.classList.add("lista-vazia");
    }
  };

  const loadTranscription = async (fileId) => {
    try {
      const response = await api(`/arquivos/${fileId}/transcricao`);
      if (!response.ok) throw new Error(await getApiError(response, "Transcrição ainda não disponível."));
      const data = await response.json();
      textArea.value = data.texto || "Transcrição vazia.";
      updateCounter();
      textArea.focus();
    } catch (error) {
      window.alert(error.message);
    }
  };

  document.querySelector("[data-clear-text]")?.addEventListener("click", () => {
    textArea.value = "";
    updateCounter();
    textArea.focus();
  });
  document.querySelector("[data-download-text]")?.addEventListener("click", () => {
    if (!textArea.value.trim()) return window.alert("Adicione algum texto antes de baixar.");
    const blob = new Blob([textArea.value], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "transcricao-voxify.txt";
    link.click();
    setTimeout(() => URL.revokeObjectURL(link.href), 0);
  });
  document.querySelector("[data-logout]")?.addEventListener("click", () => {
    sessionStorage.removeItem("token");
    window.location.assign("login.html");
  });
  textArea?.addEventListener("input", updateCounter);

  if (!sessionStorage.getItem("token")) window.location.replace("login.html");
  else {
    updateCounter();
    carregarArquivos();
  }
})();
