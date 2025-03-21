let users = [];
let editingUserId = -1;

async function addUser(options) {
  const response = await fetch("http://127.0.0.1:5000/api/users/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("sessionToken"),
      ...options,
    }),
  });

  const data = await response.json();

  if (!response.ok || data.error) {
    alert(`Error: Failed to add user ${data.error}`);
    return false;
  }

  await updateTable();
  return true;
}

async function deleteUser(id) {
  let response = await fetch("http://127.0.0.1:5000/api/users/remove", {
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
    alert(`Error: Failed to delete user ${data.error}`);
    return false;
  }

  await updateTable();
}

async function modifyUser(id, options = {}) {
  let response = await fetch("http://127.0.0.1:5000/api/users/edit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      token: localStorage.getItem("sessionToken"),
      ...options,
    }),
  });

  let data = await response.json();

  if (!response.ok || data.error) {
    alert(`Error: Failed to modify user ${data.error}`);
    return false;
  }

  await updateTable();
}

async function updateTable() {
  const response = await fetch("/api/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("sessionToken"),
    }),
  });

  if (response.status === 401) {
    alert("User is not Authenticated / Authorized");
    window.location.href = "/";
    return;
  }

  const data = await response.json();
  console.log(data);
  users = data;

  let table = document.querySelector("table > tbody");
  table.innerHTML = "";
  for (let user of data) {
    let row = document.createElement("tr");
    row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>${user.password}</td>
            <td>${user.role}</td>
            <td>
                <button class="edit-button" onclick="openEditPopup(${user.id})">
                    <img style="width: 1rem" src="/static/icons/edit.svg">
                </button>
                <button class="delete" onclick="deleteUser(${user.id})">
                    <img style="width: 1rem" src="./static/icons/trash.svg">
                </button>
            </td>
        `;
    table.appendChild(row);
  }
}

function initializeAddPopup() {
  let add_popup = document.querySelector("#add-popup");
  let addUserForm = document.querySelector("#add-user-form");

  add_popup.querySelector(".close").addEventListener("click", () => {
    add_popup.style.visibility = "hidden";
  });

  addUserForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const newUser = {
      username: document.querySelector("#username").value,
      email: document.querySelector("#email").value,
      password: document.querySelector("#password").value,
      role: document.querySelector("#role").value,
    };

    addUser(newUser);
    add_popup.style.visibility = "hidden";
    addUserForm.reset();
  });

  let addUserButton = document.querySelector("#add-user-button");
  addUserButton.addEventListener("click", () => {
    add_popup.style.visibility = "visible";
  });
}

function openEditPopup(id) {
  let edit_popup = document.querySelector("#edit-popup");
  editingUserId = id;

  let user = users.find((user) => user.id == id);

  document.querySelector("#edit-popup #username").value = user.username;
  document.querySelector("#edit-popup #email").value = user.email;
  document.querySelector("#edit-popup #password").value = user.password;
  document.querySelector("#edit-popup #role").value = user.role;

  edit_popup.style.visibility = "visible";
}

function initializeEditPopup() {
  let edit_popup = document.querySelector("#edit-popup");

  edit_popup.querySelector(".close").addEventListener("click", () => {
    edit_popup.style.visibility = "hidden";
  });

  edit_popup.addEventListener("reset", () => {
    edit_popup.style.visibility = "hidden";
  });

  edit_popup.addEventListener("submit", (e) => {
    e.preventDefault();

    const options = {
      username: document.querySelector("#edit-popup #username").value,
      password: document.querySelector("#edit-popup #password").value,
      email: document.querySelector("#edit-popup #email").value,
      role: document.querySelector("#edit-popup #role").value,
    };

    modifyUser(editingUserId, options);
    edit_popup.style.visibility = "hidden";
  });
}

window.onload = async () => {
  initializeAddPopup();
  initializeEditPopup();
  await updateTable();
};
