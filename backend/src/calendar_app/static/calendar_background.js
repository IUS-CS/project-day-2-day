(function () {
  const select = document.getElementById("calendarBackground");
  if (!select) return;

    const presets = {
  default:  { bg: "#f6f7fb", img: "none" },
  soft:     { bg: "#e2e6ef", img: "none" },  
  blue:     { bg: "#cfe8ff", img: "none" },  
  pink:     { bg: "#ffd1dc", img: "none" },
  green:    { bg: "#d1f7d6", img: "none" },
  red:      { bg: "#ffd6d6", img: "none" }, 
};


  function applyPreset(key) {
    const preset = presets[key] || presets.default;
    document.documentElement.style.setProperty("--calendar-bg", preset.bg);
    document.documentElement.style.setProperty("--calendar-bg-image", preset.img);
  }

  const saved = localStorage.getItem("calendarBackground") || "default";
  select.value = saved;
  applyPreset(saved);

  select.addEventListener("change", () => {
    localStorage.setItem("calendarBackground", select.value);
    applyPreset(select.value);
  });
})();
