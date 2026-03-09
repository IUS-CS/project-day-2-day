(() => {
  const gridEl = document.getElementById("grid");
  const monthLabelEl = document.getElementById("monthLabel");
  const detailsBodyEl = document.getElementById("detailsBody");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const todayBtn = document.getElementById("todayBtn");
  const customTaskForm = document.getElementById("customTaskForm");
  const customTaskPanel = document.getElementById("customTaskPanel");
  const selectedDateLabelEl = document.getElementById("selectedDateLabel");
  const taskTitleEl = document.getElementById("taskTitle");
  const taskDateEl = document.getElementById("taskDate");
  const taskTimeEl = document.getElementById("taskTime");
  const taskTypeEl = document.getElementById("taskType");

  const pad2 = (n) => String(n).padStart(2, "0");
  const toISO = (d) => `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`;
  const startDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());

  const addDays = (d, n) => {
    const x = new Date(d);
    x.setDate(x.getDate() + n);
    return x;
  };

  const startOfWeek = (d) => addDays(startDay(d), -d.getDay());
  const startOfMonth = (y, m) => new Date(y, m, 1);
  const monthLabel = (y, m) => new Date(y, m, 1).toLocaleString(undefined, { month: "long" }) + ` ${y}`;

  const today = startDay(new Date());
  let viewY = today.getFullYear();
  let viewM = today.getMonth();
  let selectedISO = toISO(today);

  const mockEvents = [
    { id: 1, title: "Team meeting", date: "2026-03-03", startTime: "10:00" },
    { id: 2, title: "Study block", date: "2026-03-03", startTime: "18:00" },
    { id: 3, title: "Project work", date: "2026-03-08", startTime: "14:30" }
  ];

  let customTasks = JSON.parse(localStorage.getItem("customTasks") || "[]");

  function saveCustomTasks() {
    localStorage.setItem("customTasks", JSON.stringify(customTasks));
  }

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

  function buildCustomTaskMap(list) {
    const map = new Map();
    for (const task of list) {
      if (!map.has(task.date)) map.set(task.date, []);
      map.get(task.date).push(task);
    }
    for (const [k, arr] of map.entries()) {
      arr.sort((a, b) => (a.time || "").localeCompare(b.time || ""));
      map.set(k, arr);
    }
    return map;
  }

  function rebuildMaps() {
    return {
      eventsByDay: buildEventMap(mockEvents),
      customTasksByDay: buildCustomTaskMap(customTasks)
    };
  }

  function clearSelectedDay() {
    document.querySelectorAll(".day.selected").forEach((el) => el.classList.remove("selected"));
  }

  function selectDayCell(iso) {
    clearSelectedDay();
    const selectedCell = gridEl.querySelector(`.day[data-date="${iso}"]`);
    if (selectedCell) selectedCell.classList.add("selected");
  }

  function showTaskPanel(iso) {
    if (taskDateEl) taskDateEl.value = iso;
    if (selectedDateLabelEl) selectedDateLabelEl.textContent = iso;
    if (customTaskPanel) customTaskPanel.classList.remove("hidden");
    setTimeout(() => {
      if (taskTitleEl) taskTitleEl.focus();
    }, 0);
  }

  function renderDayDetails(iso) {
    selectedISO = iso;
    showTaskPanel(iso);

    const { eventsByDay, customTasksByDay } = rebuildMaps();
    const dayEvents = eventsByDay.get(iso) || [];
    const dayTasks = customTasksByDay.get(iso) || [];

    let html = `<strong>${iso}</strong>`;

    if (!dayEvents.length && !dayTasks.length) {
      html += `<div>No events.</div>`;
      detailsBodyEl.innerHTML = html;
      return;
    }

    if (dayEvents.length) {
      html += `<div class="task-item"><strong>Imported Events</strong>`;
      html += dayEvents.map((ev) => `<div>• ${((ev.startTime || "").trim() + " " + (ev.title || "Untitled")).trim()}</div>`).join("");
      html += `</div>`;
    }

    if (dayTasks.length) {
      html += dayTasks.map((task) => `
        <div class="task-item">
          <div><strong>${task.title}</strong></div>
          <div>Time: ${task.time}</div>
          <div>Type: ${task.type}</div>
          <button type="button" class="btn delete-task-btn" data-task-id="${task.id}">Delete</button>
        </div>
      `).join("");
    }

    detailsBodyEl.innerHTML = html;

    detailsBodyEl.querySelectorAll(".delete-task-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const taskId = Number(btn.dataset.taskId);
        customTasks = customTasks.filter((task) => task.id !== taskId);
        saveCustomTasks();
        render();
        renderDayDetails(iso);
        selectDayCell(iso);
      });
    });
  }

  function render() {
    gridEl.innerHTML = "";
    monthLabelEl.textContent = monthLabel(viewY, viewM);

    const { eventsByDay, customTasksByDay } = rebuildMaps();
    const first = startOfWeek(startOfMonth(viewY, viewM));
    const cells = 42;

    for (let i = 0; i < cells; i++) {
      const d = addDays(first, i);
      const iso = toISO(d);
      const inMonth = d.getMonth() === viewM;

      const dayEl = document.createElement("div");
      dayEl.className = "day" + (inMonth ? "" : " outside") + (iso === toISO(today) ? " today" : "");
      dayEl.dataset.date = iso;

      const header = document.createElement("div");
      header.className = "day-header";

      const num = document.createElement("div");
      num.className = "day-number";
      num.textContent = String(d.getDate());
      header.appendChild(num);

      const chips = document.createElement("div");
      chips.className = "chips";

      const evs = eventsByDay.get(iso) || [];
      const tasks = customTasksByDay.get(iso) || [];
      const previews = [
        ...evs.map((ev) => ({ kind: "event", id: ev.id, title: ev.title || "Untitled", time: ev.startTime || "" })),
        ...tasks.map((task) => ({ kind: "task", id: task.id, title: task.title || "Untitled", time: task.time || "" }))
      ].sort((a, b) => (a.time || "").localeCompare(b.time || ""));

      const maxShow = 3;

      previews.slice(0, maxShow).forEach((item) => {
        const chip = document.createElement("div");
        chip.className = item.kind === "task" ? "day-task-preview" : "chip";
        chip.title = item.title || "Untitled";
        chip.textContent = item.time ? `${item.time} ${item.title}` : item.title || "Untitled";

        chip.addEventListener("click", (e) => {
          e.stopPropagation();
          selectedISO = iso;
          selectDayCell(iso);
          renderDayDetails(iso);
        });

        chips.appendChild(chip);
      });

      if (previews.length > maxShow) {
        const more = document.createElement("div");
        more.className = "more";
        more.textContent = `+${previews.length - maxShow} more`;

        more.addEventListener("click", (e) => {
          e.stopPropagation();
          selectedISO = iso;
          selectDayCell(iso);
          renderDayDetails(iso);
        });

        chips.appendChild(more);
      }

      dayEl.appendChild(header);
      dayEl.appendChild(chips);

      dayEl.addEventListener("click", () => {
        selectedISO = iso;
        selectDayCell(iso);
        renderDayDetails(iso);
      });

      gridEl.appendChild(dayEl);
    }

    if (selectedISO) {
      selectDayCell(selectedISO);
      renderDayDetails(selectedISO);
    } else {
      const todayISO = toISO(today);
      selectedISO = todayISO;
      selectDayCell(todayISO);
      renderDayDetails(todayISO);
    }
  }

  if (customTaskForm) {
    customTaskForm.addEventListener("submit", (e) => {
      e.preventDefault();

      const title = taskTitleEl.value.trim();
      const date = taskDateEl.value;
      const time = taskTimeEl.value;
      const type = taskTypeEl.value;

      if (!title || !date || !time || !type) {
        alert("Please fill out all fields.");
        return;
      }

      const newTask = {
        id: Date.now(),
        title,
        date,
        time,
        type
      };

      customTasks.push(newTask);
      saveCustomTasks();

      const taskDateObj = new Date(date + "T00:00:00");
      viewY = taskDateObj.getFullYear();
      viewM = taskDateObj.getMonth();
      selectedISO = date;

      customTaskForm.reset();
      if (taskDateEl) taskDateEl.value = date;
      render();
      selectDayCell(date);
      renderDayDetails(date);
    });
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
    selectedISO = toISO(today);
    render();
  });

  render();
})();