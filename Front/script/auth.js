window.login = async (email, senha) => {
  const response = await api("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, senha })
  });

  if (!response.ok) throw new Error(await getApiError(response, "E-mail ou senha inválidos."));

  const data = await response.json();
  sessionStorage.setItem("token", data.access_token);
  return data;
};
