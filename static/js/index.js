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

const editEntry = (e) => {
  const id = e.target.dataset.editEntry;
  const row = document.querySelector(`tr[data-edit-row="${id}"]`);
  if (row) {
    row.classList.toggle("display-none");
  }
};

const beforeSubmitEdit = (e) => {
  const form = e.target;

  const startRaw = form.querySelector(`input[name="start_time_raw"]`).value;
  if (startRaw) {
    const startTime = new Date(Date.parse(startRaw)).toISOString();
    form.querySelector(`input[name="start_time"]`).value = startTime;

    // End time is not strictly required. If the user is editing the start
    // time of the currently-active entry, there won't be an end time.
    const endRaw = form.querySelector(`input[name="end_time_raw"]`).value;
    if (endRaw) {
      const endTime = new Date(Date.parse(endRaw)).toISOString();
      form.querySelector(`input[name="end_time"]`).value = endTime;
    }
  } else {
    // If there's no start time, that's an error. Don't do anything.
    e.preventDefault();
  }
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

  $("a[data-edit-entry]").forEach((element) => {
    element.addEventListener("click", editEntry);
  });

  $("form[data-edit-entry]").forEach((element) =>
    element.addEventListener("submit", beforeSubmitEdit),
  );
};

document.addEventListener("DOMContentLoaded", init);
