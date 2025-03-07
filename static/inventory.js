//! TEMP Just until backend is done
let next_id = 0;
let inventory = [
  {
    color: "red",
    id: 0,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 1,
    name: "asdf",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 2,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
  {
    color: "red",
    id: 3,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 4,
    name: "aoeu",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 5,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
  {
    color: "red",
    id: 6,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 7,
    name: "aoeu",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 8,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
  {
    color: "red",
    id: 9,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 10,
    name: "aoeu",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 11,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
  {
    color: "red",
    id: 12,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 13,
    name: "aoeu",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 14,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
  {
    color: "red",
    id: 15,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 16,
    name: "aoeu",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 17,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
  {
    color: "red",
    id: 18,
    name: "aoeu",
    price: 1,
    quantity: 2,
  },
  {
    color: "blue",
    id: 19,
    name: "aoeu",
    price: 3,
    quantity: 4,
  },
  {
    color: "green",
    id: 20,
    name: "aoeu",
    price: 5,
    quantity: 6,
  },
];

let filters = {};
let editingId = -1;

// DONE -> connected to Flask
function addItem(options) {
  fetch("http://127.0.0.1:5000/add", {
    //sends request to flask backend
    method: "POST", //using HTTP post method
    headers: {
      "Content-Type": "application/json", //tell flask we're sending JSON
    },
    body: JSON.stringify(options), //convert item details to JSON
  })
    .then((response) => response.json()) //convert server response to JSON
    .then((data) => {
      if (data.error) {
        //error handle
        alert("Error: " + data.error);
      } else {
        alert("Item added successfully!"); //success popup
        updateTable(); //get updated data from the backend
      }
    })
    .catch((error) => console.error("Error:", error));
}

//TODO: send the request to the server instead of here
function deleteItem(id) {
  fetch("http://127.0.0.1:5000/remove", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id }), // Send the ID to Flask
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert(data.message);
        updateTable(); // Refresh inventory from Flask
      }
    })
    .catch((error) => console.error("Error:", error));
}

function modifyItem(id, options = {}) {
  console.log("Sending Data to Backend:", {
    id: id,
    quantity: options.quantity,
    price: options.price,
    color: options.color,
  }); // Debugging: Log the data being sent

  fetch("http://127.0.0.1:5000/edit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      name: options.name, // Send the new name
      quantity: options.quantity, // Send the new quantity
      price: options.price, // Send the new price
      color: options.color, // Send the new color
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Backend Response:", data); // Debugging: Log the response from the backend
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert(data.message); // Success message
        updateTable(); // Refresh the table after editing
      }
    })
    .catch((error) => console.error("Error:", error));
}
// TODO: Do this on the server instead of here
function fetchResults(skip, amount, filters) {
  let results = inventory.slice();

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

  if (filters.color) {
    results = results.filter((item) => item.color == filters.color);
  }

  return results.slice(skip, amount);
}

function updateTable() {
  let table = document.querySelector("table > tbody");
  table.innerHTML = ""; // Clear existing table data

  //fetch inventory from Flask instead of local array
  fetch("/inventory")
    .then((response) => response.json()) //converst to json so can be used in js file
    .then((data) => {
      data.forEach((item) => {
        //loop through each item in inventory
        let row = document.createElement("tr"); //new row
        row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>${item.price}</td>
                <td>${item.color}</td>
                <td>
                    <button class="edit-button" onclick="openEditPopup(${item.id})">
                        <img style="width: 1rem" src="/static/icons/edit.svg"">
                    </button>
                </td>
            `;
        table.appendChild(row); //add this row to table
      });
    })
    .catch((error) => console.error("Error fetching inventory:", error));
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

  // Delete the item when the delete button is clicked
  edit_popup.querySelector(".delete").addEventListener("click", () => {
    deleteItem(editingId);
    edit_popup.style.visibility = "hidden"; // Close the popup after deletion
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
  initializeAddPopup();
  initializeEditPopup();
  initializeFilters();

  updateTable();
};
