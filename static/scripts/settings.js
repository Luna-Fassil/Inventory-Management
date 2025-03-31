function removeUnauthorizedElements() {
  userRole = localStorage.getItem("userRole");

  if (!(userRole === "admin" || userRole === "manager")) {
    document.querySelector("#users-tab").remove();
  }
}

window.onload = () => {
  removeUnauthorizedElements();

  console.log("Settings");
};
