(() => {
  const gridEl = document.getElementById("grid");
  const monthLabelEl = document.getElementById("monthLabel");
  const detailsBodyEl = document.getElementById("detailsBody");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const todayBtn = document.getElementById("todayBtn");

  const pad2 = (n) => String(n).padStart(2, "0");
  const toISO = (d) =>
    `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`;

  const startDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());

  const addDays = (d, n) => {
    const x = new Date(d);
    x.setDate(x.getDate() + n);
    return x;
  };

  const startOfWeek = (d) => addDays(startDay(d), -d.getDay()); // Sunday
  const startOfMonth = (y, m) => new Date(y, m, 1);

  const monthLabel = (y, m) =>
    new Date(y, m, 1).toLocaleString(undefined, { month: "long" }) + ` ${y}`;

  const today = startDay(new Date());
  let viewY = today.getFullYear();
  let viewM = today.getMonth();

  // Mock events for now
  const mockEvents = [
    { id: 1, title: "Team meeting", date: "2026-03-03", startTime: "10:00" },
    { id: 2, title: "Study block", date: "2026-03-03", startTime: "18:00" },
    { id: 3, title: "Project work", date: "2026-03-08", startTime: "14:30" },
  ];

  function buildEventMap(list) {
    const map = new Map();
    for (const ev of list) {
      if (!map.has(ev.date)) map.set(ev.date, []);
      map.get(ev.date).push(ev);
    }
    for (const [k, arr] of map.entries()) {
      arr.sort((a, b) => (a.startTime || "").localeCompare(b.startTime || ""));
      map.set(k, arr);
    }
    return map;
  }

  const eventsByDay = buildEventMap(mockEvents);

  function clearSelectedDay() {
    document
      .querySelectorAll(".day.selected")
      .forEach((el) => el.classList.remove("selected"));
  }

  function renderDayDetails(iso) {
    const dayEvents = eventsByDay.get(iso) || [];
    detailsBodyEl.textContent = dayEvents.length
      ? `${iso}\n` +
        dayEvents
          .map((ev) =>
            `• ${(ev.startTime || "").trim()} ${ev.title || "Untitled"}`.trim()
          )
          .join("\n")
      : `${iso}: No events.`;
  }

  function render() {
    gridEl.innerHTML = "";
    monthLabelEl.textContent = monthLabel(viewY, viewM);

    const first = startOfWeek(startOfMonth(viewY, viewM));
    const cells = 42;

    for (let i = 0; i < cells; i++) {
      const d = addDays(first, i);
      const iso = toISO(d);
      const inMonth = d.getMonth() === viewM;

      const dayEl = document.createElement("div");
      dayEl.className =
        "day" +
        (inMonth ? "" : " outside") +
        (iso === toISO(today) ? " today" : "");

      const header = document.createElement("div");
      header.className = "day-header";

      const num = document.createElement("div");
      num.className = "day-number";
      num.textContent = String(d.getDate());
      header.appendChild(num);

      const chips = document.createElement("div");
      chips.className = "chips";

      const evs = eventsByDay.get(iso) || [];
      const maxShow = 3;

      evs.slice(0, maxShow).forEach((ev) => {
        const chip = document.createElement("div");
        chip.className = "chip";
        chip.title = ev.title || "Untitled";
        chip.textContent = ev.startTime
          ? `${ev.startTime} ${ev.title}`
          : ev.title || "Untitled";

        chip.addEventListener("click", (e) => {
          e.stopPropagation();
          clearSelectedDay();
          dayEl.classList.add("selected");
          detailsBodyEl.textContent = `${iso}\n• ${(ev.startTime || "")
            .trim()} ${ev.title || "Untitled"}`.trim();
        });

        chips.appendChild(chip);
      });

      if (evs.length > maxShow) {
        const more = document.createElement("div");
        more.className = "more";
        more.textContent = `+${evs.length - maxShow} more`;

        more.addEventListener("click", (e) => {
          e.stopPropagation();
          clearSelectedDay();
          dayEl.classList.add("selected");
          renderDayDetails(iso);
        });

        chips.appendChild(more);
      }

      dayEl.appendChild(header);
      dayEl.appendChild(chips);

      dayEl.addEventListener("click", () => {
        clearSelectedDay();
        dayEl.classList.add("selected");
        renderDayDetails(iso);
      });

      gridEl.appendChild(dayEl);
    }

    const todayCell = gridEl.querySelector(".day.today");
    if (todayCell) {
      clearSelectedDay();
      todayCell.classList.add("selected");
      renderDayDetails(toISO(today));
    }
  }

  prevBtn.addEventListener("click", () => {
    viewM--;
    if (viewM < 0) {
      viewM = 11;
      viewY--;
    }
    render();
  });

  nextBtn.addEventListener("click", () => {
    viewM++;
    if (viewM > 11) {
      viewM = 0;
      viewY++;
    }
    render();
  });

  todayBtn.addEventListener("click", () => {
    viewY = today.getFullYear();
    viewM = today.getMonth();
    render();
  });

  render();
})();
