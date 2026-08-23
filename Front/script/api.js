window.api = async (endpoint, options = {}) => {
  const token = sessionStorage.getItem("token");
  const headers = new Headers(options.headers || {});

  if (token) headers.set("Authorization", `Bearer ${token}`);

  try {
    const response = await fetch(`${window.VOXIFY_API_URL}${endpoint}`, { ...options, headers });
    if (response.status === 401) {
      sessionStorage.removeItem("token");
      window.location.href = "/login.html";
      return response;
    }
    return response;
  } catch {
    throw new Error("Não foi possível conectar à API. Verifique se o servidor está em execução.");
  }
};

window.getApiError = async (response, fallback = "Não foi possível concluir a operação.") => {
  try {
    const data = await response.json();
    return data.detail || data.mensagem || fallback;
  } catch {
    return fallback;
  }
};
