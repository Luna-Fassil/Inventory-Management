//! TEMP Just until backend is done
let next_id = 0;
let inventory = [
  {
    color: "red",
    id: 0,
    name: "aoeu",
    price: 123,
    quantity: 123,
  },
];

let filters = {};

function addItem(options) {
  console.log(options);
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

  updateTable();
}

function deleteItem(id) {
  //TODO: send the request to the server to update there
  let item_index = inventory.find((item) => item.id === id);
  inventory.splice(item_index, 1);

  updateTable();
}

function modifyItem(options = {}) {
  let index = inventory.findIndex((item) => item.id === id);
  inventory[index].name = name;
  inventory[index].quantity = quantity;
  inventory[index].price = price;

  // TODO: send the request to the server to update there

  updateTable();
}

function fetchResults() {
  // TODO: Do this on the server instead of here

  console.log("Inventory: ", inventory);
  let results = inventory.slice();
  console.log("Results: ", results);

  if (filters.search) {
    results = results.filter(
      (item) => item.name.includes(filters.search) || item.id == filters.search
    );
  }

  if (filters.maxPrice) {
    results = results.filter((item) => item.price < filters.maxPrice);
  }

  if (filters.minPrice) {
    results = results.filter((item) => item.price > filters.minPrice);
  }

  if (filters.maxQuantity) {
    results = results.filter((item) => item.quantity < filters.maxQuantity);
  }

  if (filters.minQuantity) {
    results = results.filter((item) => item.quantity > filters.minQuantity);
  }

  console.log("Filters:", filters);

  if (filters.color) {
    results = results.filter((item) => item.color == filters.color);
  }

  return results.slice(0, 20);
}

function updateTable() {
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
              <button class="edit-button" onclick="openEditPopup()"><img style="width: 1rem" src="./icons/edit.svg"></button>
              <td>
            `;
    table.appendChild(row);
  });
}

function initalizeAddPopup() {
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
}

function initalizeEditPopup() {
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
}

function initalizeFilters() {
  const filtersForm = document.querySelector("#filters-form");

  // Submit Behaviour
  filtersForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let searchQuery = document.querySelector("#search").value;
    let inputMinPrice =
      parseFloat(document.querySelector("input[name='min-price']").value) ||
      undefined;
    let inputMaxPrice =
      parseFloat(document.querySelector("input[name='max-price']").value) ||
      undefined;
    let inputMinQuantity =
      parseInt(document.querySelector("input[name='min-quantity']").value) ||
      undefined;
    let inputMaxQuantity =
      parseInt(document.querySelector("input[name='max-quantity']").value) ||
      undefined;
    let inputColor = document.querySelector("#filter-color").value;

    filters = {
      search: searchQuery,
      minPrice: inputMinPrice,
      maxPrice: inputMaxPrice,
      minQuantity: inputMinQuantity,
      maxQuantity: inputMaxQuantity,
      color: inputColor === "any" ? undefined : inputColor,
    };

    updateTable();
  });
}

window.onload = () => {
  initalizeAddPopup();
  initalizeEditPopup();
  initalizeFilters();

  updateTable();
};
