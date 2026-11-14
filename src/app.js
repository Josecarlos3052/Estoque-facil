import { SAMPLE_PRODUCTS, createProduct, updateProduct, moveStock, getMetrics, searchProducts, toCSV } from "./stock.js";

const STORE_KEY = "estoquefacil-v1";
const $ = selector => document.querySelector(selector);
const formatMoney = value => new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
const escapeHTML = value => String(value).replace(/[&<>"']/g, function (char) {
  return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
});
const uid = () => (globalThis.crypto && globalThis.crypto.randomUUID)
  ? globalThis.crypto.randomUUID()
  : String(Date.now()) + "-" + Math.random().toString(16).slice(2);

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

let data;
try {
  const saved = JSON.parse(localStorage.getItem(STORE_KEY));
  data = saved && Array.isArray(saved.products) && Array.isArray(saved.history)
    ? saved
    : { products: clone(SAMPLE_PRODUCTS), history: [] };
} catch (error) {
  data = { products: clone(SAMPLE_PRODUCTS), history: [] };
}

let editingId = null;
let toastTimer = null;

function persist() {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(data));
  } catch (error) {
    toast("Não foi possível salvar os dados neste navegador.");
  }
}

function toast(message) {
  const element = $("#toast");
  if (!element) return;
  element.textContent = message;
  element.classList.add("show");
  if (toastTimer) window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(function () {
    element.classList.remove("show");
  }, 2700);
}

function setView(view) {
  const titles = {
    overview: ["PAINEL / VISÃO GERAL", "Acompanhe os indicadores e as atividades do estoque."],
    products: ["PAINEL / PRODUTOS", "Cadastre, consulte e atualize os produtos."],
    movements: ["PAINEL / MOVIMENTAÇÕES", "Registre entradas e saídas e consulte o histórico."]
  };
  if (!titles[view]) return;

  document.querySelectorAll("[data-view-panel]").forEach(function (panel) {
    panel.hidden = panel.dataset.viewPanel !== view;
  });

  document.querySelectorAll(".nav-link[data-view]").forEach(function (button) {
    const selected = button.dataset.view === view;
    button.classList.toggle("selected", selected);
    if (selected) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });

  $("#viewCrumb").textContent = titles[view][0];
  $("#viewSubtitle").textContent = titles[view][1];

  if (view === "products") renderProducts();
  if (view === "movements") renderMovements();
}

function renderHistoryRow(movement) {
  const isEntry = movement.type === "ENTRADA";
  const date = new Date(movement.date);
  const dateText = Number.isNaN(date.getTime())
    ? "Data não informada"
    : date.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });

  return '<div class="history-row">' +
    '<span class="history-type ' + (isEntry ? "" : "out") + '">' + (isEntry ? "+" : "−") + '</span>' +
    '<div><strong>' + escapeHTML(movement.productName) + '</strong>' +
    '<small>' + (isEntry ? "Entrada" : "Saída") + " · " + dateText + '</small></div>' +
    '<b class="' + (isEntry ? "in" : "out") + '">' + (isEntry ? "+" : "−") + movement.quantity + ' un.</b>' +
    '</div>';
}

function renderOverview() {
  const metrics = getMetrics(data.products);
  $("#metricProducts").textContent = metrics.products;
  $("#metricUnits").textContent = metrics.units;
  $("#metricLow").textContent = metrics.low;
  $("#metricValue").textContent = formatMoney(metrics.inventoryValue);

  const lowProducts = data.products.filter(function (product) {
    return product.stock <= product.minimum;
  });

  $("#lowStockList").innerHTML = lowProducts.length
    ? lowProducts.map(function (product) {
        return '<div class="overview-row"><div><strong>' + escapeHTML(product.name) +
          '</strong><small>' + escapeHTML(product.sku) + " · mínimo " + product.minimum +
          ' un.</small></div><span class="badge low">' + product.stock + ' un.</span></div>';
      }).join("")
    : '<div class="history-empty">Nenhum produto com estoque baixo.</div>';

  $("#recentHistoryList").innerHTML = data.history.length
    ? data.history.slice(0, 5).map(renderHistoryRow).join("")
    : '<div class="history-empty">Nenhuma movimentação registrada.</div>';
}

function renderProducts() {
  const filtered = searchProducts(data.products, $("#searchInput").value, $("#onlyLow").checked);

  $("#productRows").innerHTML = filtered.map(function (product) {
    return '<tr>' +
      '<td><div class="product-name">' + escapeHTML(product.name) + '</div><div class="product-category">' + escapeHTML(product.category) + '</div></td>' +
      '<td>' + escapeHTML(product.sku) + '</td>' +
      '<td>' + formatMoney(product.price) + '</td>' +
      '<td class="stock-number">' + product.stock + ' un.</td>' +
      '<td><span class="badge ' + (product.stock <= product.minimum ? "low" : "regular") + '">' +
        (product.stock <= product.minimum ? "Estoque baixo" : "Regular") + '</span></td>' +
      '<td><div class="actions">' +
        '<button class="action-btn" type="button" data-action="move" data-id="' + escapeHTML(product.id) + '">Movimentar</button>' +
        '<button class="action-btn" type="button" data-action="edit" data-id="' + escapeHTML(product.id) + '">Editar</button>' +
        '<button class="action-btn danger" type="button" data-action="delete" data-id="' + escapeHTML(product.id) + '">Excluir</button>' +
      '</div></td></tr>';
  }).join("");

  $("#emptyState").hidden = filtered.length > 0;
  $("#itemCount").textContent = filtered.length + " de " + data.products.length + " produto(s)";
}

function renderMovements() {
  const term = $("#movementSearch").value.trim().toLocaleLowerCase("pt-BR");
  const type = $("#movementTypeFilter").value;

  const filtered = data.history.filter(function (movement) {
    const name = String(movement.productName || "").toLocaleLowerCase("pt-BR");
    const sku = String(movement.sku || "").toLocaleLowerCase("pt-BR");
    const matchesTerm = !term || name.includes(term) || sku.includes(term);
    return matchesTerm && (type === "TODAS" || movement.type === type);
  });

  $("#movementRows").innerHTML = filtered.map(function (movement) {
    const date = new Date(movement.date);
    const dateText = Number.isNaN(date.getTime())
      ? "—"
      : date.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
    const isEntry = movement.type === "ENTRADA";

    return '<tr><td>' + dateText + '</td>' +
      '<td><div class="product-name">' + escapeHTML(movement.productName) + '</div></td>' +
      '<td>' + escapeHTML(movement.sku || "—") + '</td>' +
      '<td><span class="badge ' + (isEntry ? "regular" : "low") + '">' + (isEntry ? "Entrada" : "Saída") + '</span></td>' +
      '<td class="stock-number">' + (isEntry ? "+" : "−") + movement.quantity + ' un.</td></tr>';
  }).join("");

  $("#movementEmpty").hidden = filtered.length > 0;
  $("#movementCount").textContent = filtered.length + " de " + data.history.length + " movimentação(ões)";
}

function render() {
  renderOverview();
  renderProducts();
  renderMovements();
}

function openProduct(id) {
  editingId = id || null;
  const form = $("#productForm");
  form.reset();
  $("#productError").textContent = "";

  const current = data.products.find(function (product) {
    return product.id === editingId;
  });

  $("#productDialogTitle").textContent = current ? "Editar produto" : "Novo produto";
  $("#initialStockLabel").hidden = Boolean(current);
  form.elements.stock.required = !current;

  if (current) {
    ["name", "sku", "category", "price", "minimum"].forEach(function (key) {
      form.elements[key].value = current[key];
    });
  } else {
    form.elements.stock.value = "0";
    form.elements.minimum.value = "5";
  }

  $("#productDialog").showModal();
}

function openMovement(productId) {
  if (!data.products.length) {
    toast("Cadastre um produto antes de registrar uma movimentação.");
    setView("products");
    return;
  }

  const select = $("#moveProductSelect");
  select.innerHTML = data.products.map(function (product) {
    return '<option value="' + escapeHTML(product.id) + '">' + escapeHTML(product.name) +
      " · " + escapeHTML(product.sku) + " (saldo: " + product.stock + ")</option>";
  }).join("");

  $("#moveForm").reset();
  if (productId && data.products.some(function (product) { return product.id === productId; })) {
    select.value = productId;
  }
  $("#moveError").textContent = "";
  updateMovementBalance();
  $("#moveDialog").showModal();
}

function updateMovementBalance() {
  const product = data.products.find(function (item) {
    return item.id === $("#moveProductSelect").value;
  });
  $("#moveProductName").textContent = product ? "Saldo disponível: " + product.stock + " unidade(s)" : "";
}

function deleteProduct(id) {
  const product = data.products.find(function (item) {
    return item.id === id;
  });
  if (!product) return;

  if (!window.confirm('Deseja excluir o produto "' + product.name + '"? O histórico será mantido.')) return;

  data.products = data.products.filter(function (item) {
    return item.id !== id;
  });
  persist();
  render();
  toast("Produto excluído.");
}

document.querySelectorAll(".nav-link[data-view]").forEach(function (button) {
  button.addEventListener("click", function () {
    setView(button.dataset.view);
  });
});

document.querySelectorAll("[data-go-view]").forEach(function (button) {
  button.addEventListener("click", function () {
    setView(button.dataset.goView);
  });
});

$("#quickAddProduct").addEventListener("click", function () {
  setView("products");
  openProduct();
});
$("#addProduct").addEventListener("click", function () { openProduct(); });
$("#newMovement").addEventListener("click", function () { openMovement(); });
$("#searchInput").addEventListener("input", renderProducts);
$("#onlyLow").addEventListener("change", renderProducts);
$("#movementSearch").addEventListener("input", renderMovements);
$("#movementTypeFilter").addEventListener("change", renderMovements);
$("#moveProductSelect").addEventListener("change", updateMovementBalance);

$("#productRows").addEventListener("click", function (event) {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const product = data.products.find(function (item) {
    return item.id === button.dataset.id;
  });
  if (!product) return;

  if (button.dataset.action === "edit") openProduct(product.id);
  if (button.dataset.action === "move") openMovement(product.id);
  if (button.dataset.action === "delete") deleteProduct(product.id);
});

document.querySelectorAll("[data-close]").forEach(function (button) {
  button.addEventListener("click", function () {
    $("#" + button.dataset.close).close();
  });
});

$("#productForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());

  try {
    if (editingId) {
      data.products = updateProduct(data.products, editingId, payload);
    } else {
      data.products.unshift(createProduct(payload, data.products, uid()));
    }

    persist();
    render();
    $("#productDialog").close();
    toast(editingId ? "Produto atualizado com sucesso." : "Produto cadastrado com sucesso.");
  } catch (error) {
    $("#productError").textContent = error.message;
  }
});

$("#moveForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form).entries());

  try {
    const result = moveStock(data.products, values.productId, values.type, values.quantity, uid());
    data.products = result.products;
    data.history.unshift(result.movement);
    persist();
    render();
    $("#moveDialog").close();
    toast((values.type === "ENTRADA" ? "Entrada" : "Saída") + " registrada com sucesso.");
    setView("movements");
  } catch (error) {
    $("#moveError").textContent = error.message;
  }
});

$("#exportCSV").addEventListener("click", function () {
  const url = URL.createObjectURL(new Blob([toCSV(data.products)], { type: "text/csv;charset=utf-8;" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "estoque-facil.csv";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  toast("Relatório CSV exportado.");
});

persist();
render();
setView("overview");
