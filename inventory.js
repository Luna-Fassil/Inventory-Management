//! TEMP Just until backend is done
let next_id = 0;
let inventory = [];

let filters = {};

function addItem(options) {
  const item = {
    id: next_id,
    name: options.name,
    quantity: options.quantity,
    price: options.price,
    color: options.color,
  };
  next_id += 1;

  // TODO: send the request to the server instead of inventory
  inventory.push(item);

  updateResults();
}

function deleteItem(id) {
  //TODO: send the request to the server to update there
  let item_index = inventory.find((item) => item.id === id);
  inventory.splice(item_index, 1);

  updateResults();
}

function modifyItem(options = {}) {
  let index = inventory.findIndex((item) => item.id === id);
  inventory[index].name = name;
  inventory[index].quantity = quantity;
  inventory[index].price = price;

  // TODO: send the request to the server to update there

  updateResults();
}

function fetchResults() {
  // TODO: Do this on the server instead of here

  console.log("Inventory: ", inventory);
  let results = inventory.slice();
  console.log("Results: ", results);

  if (filters.maxPrice) {
    results = results.filter((item) => item.price > filters.maxPrice);
    console.log(results);
  }

  if (filters.minPrice) {
    results = results.filter((item) => item.price < filters.maxPrice);
    console.log(results);
  }

  if (filters.maxQuantity) {
    console.log("testb");
    results = results.filter((item) => item.price > filters.maxQuantity);
  }

  if (filters.minQuantity) {
    console.log("testc");
    results = results.filter((item) => item.price < filters.minQuantity);
  }

  return results.slice(0, 20);
}

function updateResults() {
  let table = document.querySelector("table > tbody");
  table.innerHTML = "";

  // TODO: Come up with a more complete set of data headers
  // Add items to the table
  let results = fetchResults();

  console.log(results);

  results.forEach((item) => {
    let row = document.createElement("tr");
    row.innerHTML = `
              <td>${item.id}</td>
              <td>${item.name}</td>
              <td>${item.quantity}</td>
              <td>${item.price}</td>
              <td>${item.color}</td>
              <td>
              <button class="edit-button" onclick="openEditPopup()">Edit</button>
              <td>
            `;
    table.appendChild(row);
  });
}

function openEditPopup(id) {
  let edit_popup = document.querySelector("#edit-popup");
  edit_popup.style.visibility = "visible";

  // TODO: send the request to the server to update there
}

window.onload = () => {
  updateResults();

  // Add Form
  let add_popup = document.querySelector("#add-popup");
  let addItemForm = document.querySelector("#add-item-form");

  add_popup.querySelector(".close").addEventListener("click", () => {
    add_popup.style.visibility = "hidden";
  });

  addItemForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const newItem = {
      name: document.querySelector("#product-name").value,
      quantity: parseInt(document.querySelector("#quantity").value),
      price: parseFloat(document.querySelector("#price").value),
      color: document.querySelector("#color").value,
    };

    addItem(newItem);
    add_popup.style.visibility = "hidden";
    addItemForm.reset();
  });

  let addItemButton = document.querySelector("#add-item-button");
  addItemButton.addEventListener("click", () => {
    add_popup.style.visibility = "visible";
  });

  // Edit Popup
  let edit_popup = document.querySelector("#edit-popup");
  edit_popup.querySelector(".close").addEventListener("click", () => {
    edit_popup.style.visibility = "hidden";
  });

  let editButtons = document.querySelectorAll(".edit-button");
  editButtons.forEach((button) => {
    button.addEventListener("click", (index) => {
      openEditPopup(index);
    });
  });

  // Filters
  const filtersForm = document.querySelector("#filters-form");
  filtersForm.addEventListener("submit", (e) => {
    e.preventDefault();

    filters = {
      search: document.querySelector("#search").value,
      minPrice:
        parseFloat(document.querySelector("input[name='min-price']").value) ||
        undefined,
      maxPrice:
        parseFloat(document.querySelector("input[name='max-price']").value) ||
        undefined,
      minQuantity:
        parseInt(document.querySelector("input[name='min-quantity']").value) ||
        undefined,
      maxQuantity:
        parseInt(document.querySelector("input[name='max-quantity']").value) ||
        undefined,
      color: document.querySelector("#color").value,
    };

    updateResults();
  });
};
