export const $ = (selector) => Array.from(document.querySelectorAll(selector));

const handleDuration = (time) => {
  const start = Date.parse(
    time.dataset.durationFrom ?? time.getAttribute("datetime"),
  );
  const offset = +time.dataset.durationOffset || 0;

  const updateDuration = () => {
    const diff = (Date.now() - start) / 1000 + offset;
    const hours = Math.floor(diff / 3600);
    const minutes = `${Math.round((diff - hours * 3600) / 60)}`;

    if (hours > 0) {
      time.innerText = `${hours}h ${minutes.padStart(2, "0")}m`;
    } else {
      time.innerText = `${minutes} minutes`;
    }
  };

  updateDuration();
  setInterval(updateDuration, 100);
};

export const initializeDurations = () => {
  $(`time[data-as-duration]`).forEach(handleDuration);
  $("div[data-duration-from][data-duration-offset]").forEach(handleDuration);
};
