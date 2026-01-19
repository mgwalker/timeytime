import { $, initializeDurations } from "./util.js";

const start = (e) => {
  const button =
    e.target.tagName === "button" ? e.target : e.target.closest("button");
  window.location.href = `/start?id=${button.id}`;
};

const stop = (e) => {
  const id = e.target.dataset.stopEntry;
  window.location.href = `/stop?id=${id}`;
};

const deleteEntry = (e) => {
  const client = e.target.dataset.clientName;
  const start = new Date(e.target.dataset.entryStart).toLocaleTimeString();

  if (
    confirm(
      `Are you sure you want to delete the entry for ${client} that starts at ${start}?`,
    )
  ) {
    window.location.href = `/delete-entry?id=${e.target.dataset.deleteEntry}`;
  }
};

const init = () => {
  initializeDurations();

  $("div.timers .token").forEach((token) => {
    token.closest("button").addEventListener("click", start);
  });

  $("button[data-stop-entry]").forEach((button) => {
    button.addEventListener("click", stop);
  });

  $("a[data-delete-entry]").forEach((element) => {
    element.addEventListener("click", deleteEntry);
  });
};

document.addEventListener("DOMContentLoaded", init);
