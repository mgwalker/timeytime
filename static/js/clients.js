import { $ } from "./util.js";

const deleteClient = (e) => {
  const name = e.target.dataset.clientName;
  if (confirm(`Are you sure you want to delete the ${name} client?`)) {
    window.location.href = `/delete-client?id=${e.target.dataset.deleteClient}`;
  }
};

const init = () => {
  $("a[data-delete-client]").forEach((element) => {
    element.addEventListener("click", deleteClient);
  });
};

document.addEventListener("DOMContentLoaded", init);
