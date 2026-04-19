(function () {
  const select = document.getElementById("calendarBackground");
  const upload = document.getElementById("calendarBackgroundUpload");
  const clearBtn = document.getElementById("clearCustomBackground");

  if (!select) return;

  const presets = {
    default: { bg: "#f6f7fb", img: "none" },
    soft: { bg: "#e2e6ef", img: "none" },
    blue: { bg: "#cfe8ff", img: "none" },
    pink: { bg: "#ffd1dc", img: "none" },
    green: { bg: "#d1f7d6", img: "none" },
    red: { bg: "#ffd6d6", img: "none" }
  };

  function setBackground(bg, img) {
    document.documentElement.style.setProperty("--calendar-bg", bg);
    document.documentElement.style.setProperty("--calendar-bg-image", img);
  }

  function applyPreset(key) {
    const preset = presets[key] || presets.default;
    setBackground(preset.bg, preset.img);
  }

  function applyCustomImage(dataUrl) {
    setBackground("#f6f7fb", `url("${dataUrl}")`);
  }

  function updateControls() {
    const isCustom = select.value === "custom";

    if (upload) {
      upload.style.display = isCustom ? "inline-block" : "none";
    }

    if (clearBtn) {
      clearBtn.style.display = isCustom ? "inline-block" : "none";
    }
  }

  const savedMode = localStorage.getItem("calendarBackground") || "default";
  const savedCustomImage = localStorage.getItem("calendarCustomBackgroundImage");

  if (savedMode === "custom" && savedCustomImage) {
    select.value = "custom";
    applyCustomImage(savedCustomImage);
  } else {
    select.value = savedMode;
    applyPreset(savedMode);
  }

  updateControls();

  select.addEventListener("change", () => {
    localStorage.setItem("calendarBackground", select.value);

    if (select.value === "custom") {
      const customImage = localStorage.getItem("calendarCustomBackgroundImage");

      if (customImage) {
        applyCustomImage(customImage);
      } else {
        applyPreset("default");
      }
    } else {
      applyPreset(select.value);
    }

    updateControls();
  });

  if (upload) {
    upload.addEventListener("change", (event) => {
      const file = event.target.files && event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function (e) {
        const dataUrl = e.target.result;
        localStorage.setItem("calendarBackground", "custom");
        localStorage.setItem("calendarCustomBackgroundImage", dataUrl);
        select.value = "custom";
        applyCustomImage(dataUrl);
        updateControls();
      };

      reader.readAsDataURL(file);
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      localStorage.removeItem("calendarCustomBackgroundImage");
      localStorage.setItem("calendarBackground", "default");
      select.value = "default";

      if (upload) {
        upload.value = "";
      }

      applyPreset("default");
      updateControls();
    });
  }
})();