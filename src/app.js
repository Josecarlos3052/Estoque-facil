import { SAMPLE_PRODUCTS, createProduct, updateProduct, moveStock, getMetrics, searchProducts, toCSV } from "./stock.js";
const STORE_KEY = "estoquefacil-v1";
const $ = selector => document.querySelector(selector);
const formatMoney = value => new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[char]));
const uid = () => (globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`);
let data;
try {
  const saved = JSON.parse(localStorage.getItem(STORE_KEY));
  data = saved && Array.isArray(saved.products) && Array.isArray(saved.history) ? saved : { products: structuredClone(SAMPLE_PRODUCTS), history: [] };
} catch { data = { products: structuredClone(SAMPLE_PRODUCTS), history: [] }; }
let editingId = null;
let movingId = null;
let toastTimer;
function persist() { localStorage.setItem(STORE_KEY, JSON.stringify(data)); }
function toast(message) { const el = $("#toast"); el.textContent = message; el.classList.add("show"); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove("show"), 2700); }
function render() {
  const metrics = getMetrics(data.products);
  $("#metricProducts").textContent = metrics.products;
  $("#metricUnits").textContent = metrics.units;
  $("#metricLow").textContent = metrics.low;
  $("#metricValue").textContent = formatMoney(metrics.inventoryValue);
  const filtered = searchProducts(data.products, $("#searchInput").value, $("#onlyLow").checked);
  $("#productRows").innerHTML = filtered.map(product => `<tr><td><div class="product-name">${escapeHTML(product.name)}</div><div class="product-category">${escapeHTML(product.category)}</div></td><td>${escapeHTML(product.sku)}</td><td>${formatMoney(product.price)}</td><td class="stock-number">${product.stock} un.</td><td><span class="badge ${product.stock <= product.minimum ? "low" : "regular"}">${product.stock <= product.minimum ? "Estoque baixo" : "Regular"}</span></td><td><div class="actions"><button class="action-btn" data-action="move" data-id="${escapeHTML(product.id)}">↔ Movimentar</button><button class="action-btn" data-action="edit" data-id="${escapeHTML(product.id)}">Editar</button></div></td></tr>`).join("");
  $("#emptyState").hidden = filtered.length > 0;
  $("#itemCount").textContent = `${filtered.length} de ${data.products.length} produto(s)`;
  $("#historyList").innerHTML = data.history.length ? data.history.slice(0, 5).map(m => `<div class="history-row"><span class="history-type ${m.type === "SAÍDA" ? "out" : ""}">${m.type === "ENTRADA" ? "+" : "−"}</span><div><strong>${escapeHTML(m.productName)}</strong><small>${m.type === "ENTRADA" ? "Entrada" : "Saída"} • ${new Date(m.date).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}</small></div><b class="${m.type === "ENTRADA" ? "in" : "out"}">${m.type === "ENTRADA" ? "+" : "−"}${m.quantity} un.</b></div>`).join("") : '<div class="history-empty">Nenhuma movimentação registrada ainda. Clique em “Movimentar” para começar.</div>';
}
function openProduct(id = null) {
  editingId = id;
  const form = $("#productForm"); form.reset(); $("#productError").textContent = "";
  const current = data.products.find(p => p.id === id);
  $("#productDialogTitle").textContent = current ? "Editar produto" : "Novo produto";
  $("#initialStockLabel").hidden = !!current;
  form.elements.stock.required = !current;
  if (current) for (const key of ["name","sku","category","price","minimum"]) form.elements[key].value = current[key];
  else {form.elements.stock.value = "0"; form.elements.minimum.value = "5";}
  $("#productDialog").showModal();
}
$("#addProduct").addEventListener("click", () => openProduct());
$("#searchInput").addEventListener("input", render);
$("#onlyLow").addEventListener("change", render);
$("#productRows").addEventListener("click", event => {
  const btn = event.target.closest("button[data-action]"); if (!btn) return;
  const product = data.products.find(p => p.id === btn.dataset.id); if (!product) return;
  if (btn.dataset.action === "edit") return openProduct(product.id);
  movingId = product.id; $("#moveForm").reset(); $("#moveError").textContent = "";
  $("#moveProductName").textContent = `${product.name} • Saldo disponível: ${product.stock} unidade(s)`;
  $("#moveDialog").showModal();
});
document.querySelectorAll("[data-close]").forEach(btn => btn.addEventListener("click", () => $("#" + btn.dataset.close).close()));
$("#productForm").addEventListener("submit", event => {
  event.preventDefault(); const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  try {
    if (editingId) data.products = updateProduct(data.products, editingId, payload);
    else data.products.unshift(createProduct(payload, data.products, uid()));
    persist(); render(); $("#productDialog").close(); toast(editingId ? "Produto atualizado com sucesso." : "Produto cadastrado com sucesso.");
  } catch(error) { $("#productError").textContent = error.message; }
});
$("#moveForm").addEventListener("submit", event => {
  event.preventDefault(); const form = event.currentTarget;
  const {type, quantity} = Object.fromEntries(new FormData(form).entries());
  try {
    const result = moveStock(data.products, movingId, type, quantity, uid());
    data.products = result.products; data.history.unshift(result.movement);
    persist(); render(); $("#moveDialog").close(); toast(`${type === "ENTRADA" ? "Entrada" : "Saída"} registrada com sucesso.`);
  } catch(error) { $("#moveError").textContent = error.message; }
});
$("#exportCSV").addEventListener("click", () => {
  const url = URL.createObjectURL(new Blob([toCSV(data.products)], {type:"text/csv;charset=utf-8;"}));
  const a = document.createElement("a"); a.href = url; a.download = "estoque-facil.csv"; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  toast("Relatório CSV exportado.");
});
persist(); render();
