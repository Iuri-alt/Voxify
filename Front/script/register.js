window.registrar = async (nome, email, senha) => {
  const response = await api("/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, email, senha })
  });

  if (!response.ok) throw new Error(await getApiError(response, "Não foi possível criar a conta."));
  return response.json();
};
