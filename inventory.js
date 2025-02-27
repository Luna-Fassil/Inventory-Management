//! TEMP Just until backend is done
let inventory = [
  {
    id: 1,
    name: "Shirt",
    quantity: 1,
    price: 100,
    color: "blue",
  },
  {
    id: 2,
    name: "Pants",
    quantity: 2,
    price: 200,
    color: "red",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
    color: "green",
  },
];

function addItem(options) {
  item = {
    id: Math.random * 100,
    name: options.name,
    quantity: options.quantity,
    price: options.price,
  };
  inventory.push(item);

  // TODO: send the request to the server to update there

  renderResults();
}

function deleteItem(id) {
  let index = inventory.find((item) => item.id === id);
  inventory.splice(index, 1);

  // TODO: send the request to the server to update there

  renderResults();
}

function modifyItem(options) {
  let index = inventory.findIndex((item) => item.id === id);
  inventory[index].name = name;
  inventory[index].quantity = quantity;
  inventory[index].price = price;

  // TODO: send the request to the server to update there

  renderResults();
}

function fetchResults(page, sort, filters) {
  // TODO: send the request to the server to update there

  return inventory;
}

function openEditPopup(id) {
  let edit_popup = document.querySelector("#edit-popup");
  edit_popup.style.visibility = "visible";

  // TODO: send the request to the server to update there
}

function renderResults() {
  let table = document.querySelector("table > tbody");
  table.innerHTML = "";

  // TODO: Come up with a more complete set of data headers
  // Add items to the table
  let results = fetchResults();
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

window.onload = () => {
  renderResults();

  let add_popup = document.querySelector("#add-popup");
  add_popup.querySelector(".close").addEventListener("click", () => {
    add_popup.style.visibility = "hidden";
  });

  let addItemButton = document.querySelector("#add-item-button");
  addItemButton.addEventListener("click", () => {
    add_popup.style.visibility = "visible";
  });

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
};
