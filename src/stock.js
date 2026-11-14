/** Regras de negócio puras do EstoqueFácil. */
export const CATEGORIES = ["Panelas", "Frigideiras", "Utensílios", "Outros"];

export function validateProduct(input, products = [], editingId = null) {
  const name = String(input.name ?? "").trim();
  const sku = String(input.sku ?? "").trim().toUpperCase();
  const category = String(input.category ?? "").trim();
  const price = Number(input.price);
  const stock = Number(input.stock);
  const minimum = Number(input.minimum);
  if (name.length < 3) throw new Error("Informe um nome com pelo menos 3 caracteres.");
  if (!/^[A-Z0-9-]{3,20}$/.test(sku)) throw new Error("SKU deve ter de 3 a 20 letras, números ou hífens.");
  if (!CATEGORIES.includes(category)) throw new Error("Selecione uma categoria válida.");
  if (!Number.isFinite(price) || price < 0) throw new Error("Preço deve ser um valor válido e não negativo.");
  if (!Number.isInteger(stock) || stock < 0) throw new Error("Estoque inicial deve ser inteiro e não negativo.");
  if (!Number.isInteger(minimum) || minimum < 0) throw new Error("Estoque mínimo deve ser inteiro e não negativo.");
  if (products.some(p => p.sku === sku && p.id !== editingId)) throw new Error("Já existe um produto com este SKU.");
  return { name, sku, category, price, stock, minimum };
}

export function createProduct(input, products, id) {
  const payload = validateProduct(input, products);
  return { id, ...payload, createdAt: new Date().toISOString() };
}

export function updateProduct(products, id, input) {
  const existing = products.find(p => p.id === id);
  if (!existing) throw new Error("Produto não encontrado.");
  const validated = validateProduct({ ...input, stock: existing.stock }, products, id);
  return products.map(p => p.id === id ? { ...p, ...validated, stock: existing.stock } : p);
}

export function moveStock(products, id, type, quantity, movementId, date = new Date().toISOString()) {
  const product = products.find(p => p.id === id);
  if (!product) throw new Error("Produto não encontrado.");
  if (!["ENTRADA", "SAÍDA"].includes(type)) throw new Error("Tipo de movimentação inválido.");
  const amount = Number(quantity);
  if (!Number.isInteger(amount) || amount <= 0) throw new Error("A quantidade deve ser um inteiro maior que zero.");
  if (type === "SAÍDA" && amount > product.stock) throw new Error("Saldo insuficiente para registrar a saída.");
  const delta = type === "ENTRADA" ? amount : -amount;
  const updated = products.map(p => p.id === id ? { ...p, stock: p.stock + delta } : p);
  const movement = { id: movementId, productId: id, productName: product.name, sku: product.sku, type, quantity: amount, date };
  return { products: updated, movement };
}

export function getMetrics(products) {
  return {
    products: products.length,
    units: products.reduce((total, p) => total + p.stock, 0),
    low: products.filter(p => p.stock <= p.minimum).length,
    inventoryValue: products.reduce((total, p) => total + p.stock * p.price, 0)
  };
}

export function searchProducts(products, term = "", onlyLow = false) {
  const normalized = String(term).trim().toLocaleLowerCase("pt-BR");
  return products.filter(p => (!onlyLow || p.stock <= p.minimum) &&
    (!normalized || [p.name, p.sku, p.category].some(value => value.toLocaleLowerCase("pt-BR").includes(normalized))));
}

export function toCSV(products) {
  const rows = [["SKU", "Produto", "Categoria", "Preço (R$)", "Estoque", "Mínimo", "Situação"]];
  for (const p of products) rows.push([p.sku, p.name, p.category, p.price.toFixed(2).replace(".", ","), p.stock, p.minimum, p.stock <= p.minimum ? "Baixo" : "Regular"]);
  const escaped = rows.map(row => row.map(item => `"${String(item).replaceAll('"', '""')}"`).join(";")).join("\r\n");
  return "\uFEFF" + escaped;
}

export const SAMPLE_PRODUCTS = [
  { id: "p-101", sku: "PAN-024", name: "Panela antiaderente 24 cm", category: "Panelas", price: 89.90, stock: 18, minimum: 5, createdAt: "2026-11-01T10:00:00.000Z" },
  { id: "p-102", sku: "PRE-045", name: "Panela de pressão 4,5 L", category: "Panelas", price: 119.90, stock: 3, minimum: 5, createdAt: "2026-11-01T10:00:00.000Z" },
  { id: "p-103", sku: "FRI-020", name: "Frigideira antiaderente 20 cm", category: "Frigideiras", price: 59.90, stock: 12, minimum: 4, createdAt: "2026-11-01T10:00:00.000Z" },
  { id: "p-104", sku: "UTE-006", name: "Conjunto de utensílios 6 peças", category: "Utensílios", price: 34.90, stock: 7, minimum: 3, createdAt: "2026-11-01T10:00:00.000Z" }
];
