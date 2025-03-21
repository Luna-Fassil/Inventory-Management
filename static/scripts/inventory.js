// Global variables to store inventory data, filters, and the ID of the item being edited
let inventory = []; // Stores the list of inventory items
let filters = {}; // Stores the current filter settings
let editingId = -1; // Tracks the ID of the item being edited

async function addItem(options) {
  const response = await fetch("http://127.0.0.1:5000/api/inventory/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("sessionToken"),
      ...options,
    }),
  });

  console.log(await response);

  const data = await response.json();

  if (!response.ok || data.error) {
    alert(`Error: Failed to add item ${data.error}`);
    return false;
  }

  await updateTable();
  return true;
}

async function deleteItem(id) {
  let response = await fetch("http://127.0.0.1:5000/api/inventory/remove", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("sessionToken"),
      id: id,
    }),
  });

  let data = await response.json();

  if (!response.ok || data.error) {
    alert(`Error: Failed to delete item ${data.error}`);
    return false;
  }

  await updateTable();
}

async function modifyItem(id, options = {}) {
  let response = await fetch("http://127.0.0.1:5000/api/inventory/edit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("sessionToken"),
      id: id,
      ...options,
    }),
  });

  let data = await response.json();

  if (!response.ok || data.error) {
    alert(`Error: Failed to edit item ${data.error}`);
    return false;
  }

  await updateTable();
}

async function updateTable() {
  // Convert filters object to JSON string
  const amount = 100;
  const skip = 0;

  // Fetch inventory from Flask with filters
  const response = await fetch("/api/inventory", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("sessionToken"),
      filters: filters,
      amount: amount,
      skip: skip,
    }),
  });

  if (response.status === 401) {
    alert("User is not authenticated");
    window.location.href = "/";
    return;
  }

  const data = await response.json();
  inventory = data;

  let table = document.querySelector("table > tbody");
  table.innerHTML = ""; // Clear existing table data
  for (let item of data) {
    //Insert each item into the table
    let row = document.createElement("tr");
    row.innerHTML = `
        <td>${item.id}</td>
          <td>${item.name}</td>
          <td>${item.quantity}</td>
          <td>${item.price}</td>
          <td>${item.brand.charAt(0).toUpperCase() + item.brand.slice(1)}</td>
          <td>${item.season.charAt(0).toUpperCase() + item.season.slice(1)}</td>
          <td>${item.color.charAt(0).toUpperCase() + item.color.slice(1)}</td>
          <td>
          <button class="edit-button" onclick="openEditPopup(${item.id})">
            <img style="width: 1rem" src="/static/icons/edit.svg"">
          </button>
          <button class="delete" onclick="deleteItem(${item.id})">
            <img style="width: 1rem" src="./static/icons/trash.svg"">
          </button>
          </td>
        `;
    table.appendChild(row); //add this row to table
  }
}

function initializeAddPopup() {
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
      brand: document.querySelector("#brand").value,
      season: document.querySelector("#season").value,
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

function openEditPopup(id) {
  let edit_popup = document.querySelector("#edit-popup");
  editingId = id; // Set the global editingId variable

  // Find the item in the inventory
  let item = inventory.find((item) => item.id == id);

  // Populate the form with the item's current data
  document.querySelector("#edit-popup #product-name").value = item.name;
  document.querySelector("#edit-popup #quantity").value = item.quantity;
  document.querySelector("#edit-popup #price").value = item.price;
  document.querySelector("#edit-popup #brand").value = item.brand;
  document.querySelector("#edit-popup #season").value = item.season;
  document.querySelector("#edit-popup #color").value = item.color;

  // Show the edit popup
  edit_popup.style.visibility = "visible";
}

function initializeEditPopup() {
  let edit_popup = document.querySelector("#edit-popup");

  // Close the popup when the close button is clicked
  edit_popup.querySelector(".close").addEventListener("click", () => {
    edit_popup.style.visibility = "hidden";
  });

  // Reset the form and close the popup when the form is reset
  edit_popup.addEventListener("reset", (e) => {
    edit_popup.style.visibility = "hidden";
  });

  // Handle form submission
  edit_popup.addEventListener("submit", (e) => {
    e.preventDefault();

    // Collect the updated data from the form
    const options = {
      name: document.querySelector("#edit-popup #product-name").value,
      price: parseFloat(document.querySelector("#edit-popup #price").value),
      quantity: parseInt(document.querySelector("#edit-popup #quantity").value),
      brand: document.querySelector("#edit-popup #brand").value,
      season: document.querySelector("#edit-popup #season").value,
      color: document.querySelector("#edit-popup #color").value,
    };

    console.log("Editing Item ID:", editingId); // Debugging: Log the item ID
    console.log("New Options:", options); // Debugging: Log the new options

    // Call the modifyItem function to send the updated data to the backend
    modifyItem(editingId, options);

    // Close the popup after submission
    edit_popup.style.visibility = "hidden";
  });
}

function initializeFilters() {
  const filtersForm = document.querySelector("#filters-form");

  // Submit Behaviour
  filtersForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let searchQuery = document.querySelector("#search").value || undefined;
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
    let inputBrand = document.querySelector("#filter-brand").value;
    let inputSeason = document.querySelector("#filter-season").value;
    let inputColor = document.querySelector("#filter-color").value;

    filters = {
      search: searchQuery,
      minPrice: inputMinPrice,
      maxPrice: inputMaxPrice,
      minQuantity: inputMinQuantity,
      maxQuantity: inputMaxQuantity,
      brand: inputBrand === "any" ? undefined : inputBrand,
      season: inputSeason === "any" ? undefined : inputSeason,
      color: inputColor === "any" ? undefined : inputColor,
    };

    updateTable();
  });
}

window.onload = async () => {
  console.log(localStorage.getItem("sessionToken"));
  initializeAddPopup();
  initializeEditPopup();
  initializeFilters();

  await updateTable();
};
