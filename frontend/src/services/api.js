const BASE_URL = "http://127.0.0.1:5000/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) {
    const message = data.details ? JSON.stringify(data.details) : data.error || "Something went wrong";
    throw new Error(message);
  }
  return data;
}

export const api = {
  getTransactions: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/transactions/${query ? `?${query}` : ""}`);
  },
  createTransaction: (body) => request("/transactions/", { method: "POST", body: JSON.stringify(body) }),
  deleteTransaction: (id) => request(`/transactions/${id}`, { method: "DELETE" }),
  getCategories: () => request("/categories/"),
  createCategory: (body) => request("/categories/", { method: "POST", body: JSON.stringify(body) }),
  getSummary: () => request("/summary/"),
};
