//! TEMP Just until backend finished
let inventory = [
  {
    id: 1,
    name: "Shirt",
    quantity: 1,
    price: 100,
  },
  {
    id: 2,
    name: "Pants",
    quantity: 2,
    price: 200,
  },
  {
    id: 3,
    name: "Socks",
    quantity: 3,
    price: 300,
  },
];
//! TEMP

function addItem(name, quantity, price) {
  //! TEMP: Just until backend finished
  item = {
    id: inventory.length + 1,
    name: name,
    quantity: quantity,
    price: price,
  };
  inventory.push(item);
  //! TEMP

  // TODO: send the request to the server

  renderResults();
}

function deleteItem(id) {
  //! TEMP: Just until backend finished
  let index = inventory.find((item) => item.id === id);
  inventory.splice(index, 1);
  //! TEMP

  // TODO: send the request to the server

  renderResults();
}

function modifyItem(id, name, quantity, price) {
  //! TEMP: Just until backend finished
  let index = inventory.findIndex((item) => item.id === id);
  inventory[index].name = name;
  inventory[index].quantity = quantity;
  inventory[index].price = price;
  //! TEMP

  // TODO: send the request to the server

  renderResults();
}

function fetchResults(page, sort, filters) {
  // TODO: fetch results from the server

  return inventory;
}

function openEditPopup(id) {
  let edit_popup = document.querySelector("#edit-popup");
  edit_popup.style.visibility = "visible";

  // TODO: Set the values of the inputs based on the item existing info
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
