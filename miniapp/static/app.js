const tg = window.Telegram?.WebApp || {};


const state = {
    identity: null,
    profile: null,
    theme: null,
    themes: [],
    view: "today",
    appearance: "light",
    sessions: [],
    currentSession: null,
    weeks: [],
    currentWeek: null,
    defaultWeek: null,
    selectedWeek: null,
};


const screenIds = {
    today: "screenSchedule",
    tomorrow: "screenSchedule",
    week: "screenSchedule",
    sessions: "screenSessions",
    profile: "screenProfile",
    excluded: "screenExcluded",
};


function $(id) {
    return document.getElementById(id);
}


function haptic() {
    try {
        tg.HapticFeedback.impactOccurred("light");
    } catch (error) {
        // ignore
    }
}


function showToast(text) {
    const toast = $("toast");
    toast.textContent = text;
    toast.classList.add("visible");

    window.clearTimeout(showToast.timer);
    showToast.timer = setTimeout(
        () => toast.classList.remove("visible"),
        1800
    );
}


async function api(url, options = {}) {
    const headers = {
        ...(options.headers || {}),
        "X-Telegram-Init-Data": tg.initData || "",
    };

    if (options.body && !headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(url, { ...options, headers });

    let data = null;
    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {
        const message =
            data?.detail ||
            `Ошибка ${response.status}`;
        const err = new Error(message);
        err.status = response.status;
        throw err;
    }

    return data;
}


function setupInsets() {
    try {
        const insets = tg.contentSafeAreaInset || {};
        const top = insets.top || 56;
        const bottom = insets.bottom || 0;
        const root = document.documentElement;
        root.style.setProperty("--inset-top", `${top}px`);
        root.style.setProperty("--inset-bottom", `${bottom}px`);
    } catch (error) {
        // ignore
    }
}


function getSavedAppearance() {
    const saved = localStorage.getItem("hse-appearance");

    if (saved === "light" || saved === "dark") {
        return saved;
    }

    return tg.colorScheme === "dark" ? "dark" : "light";
}


function applyAppearance() {
    state.appearance = state.appearance || getSavedAppearance();

    document.documentElement.dataset.mode = state.appearance;
    document.documentElement.dataset.displayTheme =
        state.profile?.theme || "default";

    document
        .querySelectorAll("[data-appearance]")
        .forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.appearance === state.appearance
            );
        });

    syncTelegramChrome();
}


function syncTelegramChrome() {
    try {
        const bg = getComputedStyle(document.documentElement)
            .getPropertyValue("--bg")
            .trim();

        if (bg && typeof tg.setHeaderColor === "function") {
            tg.setHeaderColor(bg);
        }
        if (bg && typeof tg.setBackgroundColor === "function") {
            tg.setBackgroundColor(bg);
        }
    } catch (error) {
        // ignore
    }
}


function setAppearance(appearance) {
    state.appearance = appearance;
    localStorage.setItem("hse-appearance", appearance);
    applyAppearance();
    haptic();
}


function showScreen(screen) {
    const targetId = screenIds[screen];

    Object.values(screenIds).forEach(id => {
        const element = $(id);
        if (!element) return;
        element.classList.toggle("active", id === targetId);
    });

    const bottomNav = document.querySelector(".bottom-nav");
    const isNested = screen === "excluded";

    if (bottomNav) {
        bottomNav.style.display = isNested ? "none" : "";
    }

    try {
        if (isNested) {
            tg.BackButton?.show();
        } else {
            tg.BackButton?.hide();
        }
    } catch (error) {
        // ignore
    }
}


function setActiveNav(view) {
    document
        .querySelectorAll(".nav-item")
        .forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.view === view
            );
        });
}


async function loadBootstrap() {
    const data = await api("/api/bootstrap");

    state.identity = data.identity;
    state.profile = data.user;
    state.theme = data.theme;
    state.themes = data.themes;

    renderProfile();
    renderThemes();
    applyAppearance();
}


function renderProfile() {
    const firstName = state.identity?.first_name || "Студент";
    const group = state.profile?.group_name || "Группа не выбрана";

    $("profileName").textContent = firstName;
    $("profileGreeting").textContent = "ПРОФИЛЬ";
    $("profileGroup").textContent = group;

    $("topbarSubtitle").textContent =
        group === "Группа не выбрана"
            ? "Расписание"
            : group;

    const avatarLetter =
        (firstName.trim().charAt(0) || "H").toUpperCase();

    $("avatarButton").textContent = avatarLetter;
    $("profileAvatar").textContent = avatarLetter;

    renderNotificationValues();
}


function renderNotificationValues() {
    const updates = state.profile?.schedule_updates;
    const tomorrow = state.profile?.tomorrow_notifications;

    const updatesElement = $("scheduleUpdatesValue");
    const tomorrowElement = $("tomorrowValue");

    updatesElement.textContent = updates ? "ВКЛ" : "ВЫКЛ";
    tomorrowElement.textContent = tomorrow ? "ВКЛ" : "ВЫКЛ";

    updatesElement.classList.toggle("active", Boolean(updates));
    tomorrowElement.classList.toggle("active", Boolean(tomorrow));
}


function renderThemes() {
    const container = $("themesGrid");
    container.innerHTML = "";

    state.themes.forEach(theme => {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "theme-card";
        button.dataset.action = "theme";
        button.dataset.theme = theme.id;

        if (theme.id === state.profile.theme) {
            button.classList.add("active");
        }

        button.innerHTML = `
            <div class="theme-symbol">
                ${escapeHtml(theme.symbol)}
            </div>
            <div class="theme-name">
                ${escapeHtml(theme.name)}
            </div>
        `;

        container.appendChild(button);
    });
}


function updateScheduleHeader(view) {
    const titles = {
        today: "Сегодня",
        tomorrow: "Завтра",
        week: "Неделя",
    };

    const eyebrows = {
        today: "СЕГОДНЯ",
        tomorrow: "ЗАВТРА",
        week: "7 ДНЕЙ",
    };

    $("scheduleTitle").textContent = titles[view] || "Расписание";
    $("scheduleEyebrow").textContent = eyebrows[view] || "";
}


async function loadWeeks() {
    try {
        const data = await api("/api/weeks");
        state.weeks = data.weeks || [];
        state.currentWeek = data.current_week;
        state.defaultWeek = data.default_week;
    } catch (error) {
        state.weeks = [];
        state.currentWeek = null;
        state.defaultWeek = null;
    }
}


function renderWeekPicker() {
    const picker = $("weekPicker");
    const list = $("weekPickerList");

    if (!state.weeks || state.weeks.length <= 1) {
        picker.hidden = true;
        list.innerHTML = "";
        return;
    }

    picker.hidden = false;

    list.innerHTML = state.weeks
        .map(week => {
            const active = week === state.selectedWeek;
            const label = week === state.currentWeek
                ? `${week} · текущая`
                : String(week);

            return `
                <button
                    type="button"
                    class="week-chip ${active ? "active" : ""}"
                    data-action="select-week"
                    data-week="${week}"
                >
                    ${escapeHtml(label)}
                </button>
            `;
        })
        .join("");
}


async function loadSchedule(view) {
    state.view = view;

    showScreen(view);
    setActiveNav(view);
    updateScheduleHeader(view);

    const container = $("scheduleContainer");
    container.innerHTML = `<div class="loading">Загружаем расписание…</div>`;

    try {
        if (view === "week") {
            if (!state.weeks.length) {
                await loadWeeks();
            }

            if (state.selectedWeek == null) {
                state.selectedWeek = state.defaultWeek;
            }

            renderWeekPicker();

            const query = state.selectedWeek != null
                ? `/api/schedule?view=week&week=${state.selectedWeek}`
                : `/api/schedule?view=week`;

            const data = await api(query);
            renderSchedule(data);
            return;
        }

        $("weekPicker").hidden = true;

        const data = await api(`/api/schedule?view=${view}`);
        renderSchedule(data);
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">!</div>
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}


function renderSchedule(data) {
    const container = $("scheduleContainer");

    if (!data.lessons || !data.lessons.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">
                    ${escapeHtml(state.theme?.tokens?.lesson || "○")}
                </div>
                <p>${escapeHtml(data.empty_message || "Пар нет")}</p>
            </div>
        `;
        return;
    }

    if (data.view === "week") {
        renderWeek(data.lessons);
        return;
    }

    container.innerHTML = data.lessons.map(lessonCard).join("");
}


function renderWeek(lessons) {
    const grouped = {};

    lessons.forEach(lesson => {
        const key = `${lesson.day}|${lesson.date}`;
        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(lesson);
    });

    const container = $("scheduleContainer");

    container.innerHTML = Object.entries(grouped)
        .map(([key, dayLessons]) => {
            const [day, date] = key.split("|");

            return `
                <section class="day-section">
                    <div class="day-title">
                        ${escapeHtml(day)} · ${escapeHtml(date)}
                    </div>
                    <div class="schedule-container">
                        ${dayLessons.map(lessonCard).join("")}
                    </div>
                </section>
            `;
        })
        .join("");
}


function lessonCard(lesson) {
    const tokens = state.theme?.tokens || {};
    const meta = [];

    if (lesson.lesson_type) {
        meta.push(`
            <span class="meta-chip accent">
                ${escapeHtml(tokens.type || "•")}
                ${escapeHtml(lesson.lesson_type)}
            </span>
        `);
    }

    if (lesson.teacher) {
        meta.push(`
            <span class="meta-chip">
                ${escapeHtml(lesson.teacher)}
            </span>
        `);
    }

    if (lesson.room) {
        let roomText = lesson.room;
        if (lesson.building) roomText += ` · ${lesson.building}`;
        meta.push(`
            <span class="meta-chip">
                ${escapeHtml(tokens.room || "•")}
                ${escapeHtml(roomText)}
            </span>
        `);
    }

    if (lesson.is_online) {
        meta.push(`
            <span class="meta-chip accent">
                ${escapeHtml(tokens.online || "Онлайн")}
            </span>
        `);
    }

    return `
        <article class="lesson-card">
            <div class="lesson-top">
                <div>
                    <div class="lesson-time">
                        ${escapeHtml(lesson.lesson_time || "—")}
                    </div>
                    <div class="lesson-number">
                        ${escapeHtml(lesson.lesson_number || "")} пара
                    </div>
                </div>
            </div>

            <div class="lesson-subject">
                ${escapeHtml(tokens.subject || "•")}
                ${escapeHtml(lesson.subject)}
            </div>

            ${meta.length ? `<div class="lesson-meta">${meta.join("")}</div>` : ""}
        </article>
    `;
}


async function openSessions() {
    showScreen("sessions");
    setActiveNav("sessions");

    $("sessionsContainer").innerHTML =
        `<div class="loading">Загружаем…</div>`;
    $("sessionLessonsContainer").innerHTML = "";

    try {
        const data = await api("/api/sessions");
        state.sessions = data.sessions;
        renderSessions();
    } catch (error) {
        $("sessionsContainer").innerHTML = `
            <div class="empty-state">
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}


function renderSessions() {
    const container = $("sessionsContainer");

    if (!state.sessions.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">—</div>
                <p>Сессий пока нет.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = state.sessions
        .map(session => `
            <button
                type="button"
                class="session-button ${
                    state.currentSession === session ? "active" : ""
                }"
                data-action="session"
                data-session="${escapeAttribute(session)}"
            >
                ${escapeHtml(session)}
            </button>
        `)
        .join("");
}


async function openSession(session) {
    state.currentSession = session;
    renderSessions();

    const container = $("sessionLessonsContainer");
    container.innerHTML = `<div class="loading">Загружаем…</div>`;

    try {
        const data = await api(
            `/api/sessions/${encodeURIComponent(session)}`
        );

        if (!data.lessons.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>Для этой сессии расписания нет.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = data.lessons.map(lessonCard).join("");
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}


async function openExcluded() {
    showScreen("excluded");

    try {
        const data = await api("/api/excluded-subjects");
        renderExcluded(data);
    } catch (error) {
        $("excludedGrid").innerHTML = `
            <div class="empty-state">
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}


function renderSchedule(data) {
    const container = $("scheduleContainer");

    const debugLine = `
        <p style="font-size:11px;color:#999;margin-top:12px;font-family:monospace">
            view=${escapeHtml(String(data.view ?? "?"))} ·
            group=${escapeHtml(String(data.group ?? "—"))} ·
            count=${Array.isArray(data.lessons) ? data.lessons.length : "null"} ·
            excluded=${escapeHtml(String(state.profile?.excluded_subjects?.length ?? "?"))}
        </p>
    `;

    if (!data.lessons || !data.lessons.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">
                    ${escapeHtml(state.theme?.tokens?.lesson || "○")}
                </div>
                <p>${escapeHtml(data.empty_message || "Пар нет")}</p>
                ${debugLine}
            </div>
        `;
        return;
    }

    if (data.view === "week") {
        renderWeek(data.lessons);
        return;
    }

    container.innerHTML =
        data.lessons.map(lessonCard).join("") +
        `<div class="empty-state" style="padding:12px;margin-top:8px">${debugLine}</div>`;
}


async function toggleExcluded(subject) {
    haptic();

    try {
        const data = await api(
            "/api/excluded-subjects/toggle",
            {
                method: "POST",
                body: JSON.stringify({ subject }),
            }
        );

        const current = await api("/api/excluded-subjects");

        state.profile.excluded_subjects = data.excluded;
        renderExcluded(current);

        showToast(
            data.excluded.includes(subject)
                ? "Пара исключена"
                : "Пара снова включена"
        );
    } catch (error) {
        showToast(error.message);
    }
}


async function changeTheme(theme) {
    if (theme === state.profile.theme) return;

    haptic();

    try {
        const data = await api("/api/theme", {
            method: "POST",
            body: JSON.stringify({ theme }),
        });

        state.profile.theme = theme;
        state.theme = data.theme;

        renderThemes();
        applyAppearance();
        showToast(`Оформление: ${data.theme.name}`);
    } catch (error) {
        showToast(error.message);
    }
}


async function toggleNotification(field) {
    haptic();

    try {
        const data = await api("/api/notifications/toggle", {
            method: "POST",
            body: JSON.stringify({ field }),
        });

        state.profile.schedule_updates = data.schedule_updates;
        state.profile.tomorrow_notifications = data.tomorrow_notifications;

        renderNotificationValues();
    } catch (error) {
        showToast(error.message);
    }
}


async function openCalendar() {
    try {
        const data = await api("/api/calendar");
        tg.openLink?.(data.https_url) || window.open(data.https_url, "_blank");
    } catch (error) {
        showToast(error.message);
    }
}


document.addEventListener("click", async event => {
    const nav = event.target.closest(".nav-item");

    if (nav) {
        const view = nav.dataset.view;
        haptic();

        if (view === "sessions") {
            await openSessions();
            return;
        }

        if (view === "profile") {
            showScreen("profile");
            setActiveNav("profile");
            return;
        }

        await loadSchedule(view);
        return;
    }

    const appearance = event.target.closest("[data-appearance]");
    if (appearance) {
        setAppearance(appearance.dataset.appearance);
        return;
    }

    const actionButton = event.target.closest("[data-action]");
    if (!actionButton) return;

    const action = actionButton.dataset.action;

    if (action === "excluded") {
        haptic();
        await openExcluded();
        return;
    }

    if (action === "calendar") {
        haptic();
        await openCalendar();
        return;
    }

    if (action === "theme") {
        await changeTheme(actionButton.dataset.theme);
        return;
    }

    if (action === "select-week") {
        const week = Number(actionButton.dataset.week);
        if (week === state.selectedWeek) return;
        haptic();
        state.selectedWeek = week;
        await loadSchedule("week");
        return;
    }

    if (action === "session") {
        haptic();
        await openSession(actionButton.dataset.session);
        return;
    }

    if (action === "toggle-excluded") {
        await toggleExcluded(actionButton.dataset.subject);
        return;
    }

    if (action === "toggle-notification") {
        await toggleNotification(actionButton.dataset.field);
    }
});


$("refreshButton").addEventListener("click", async () => {
    haptic();
    await loadSchedule(state.view);
});


$("avatarButton").addEventListener("click", () => {
    showScreen("profile");
    setActiveNav("profile");
});


try {
    tg.BackButton?.onClick(() => {
        showScreen("profile");
        setActiveNav("profile");
    });

    tg.onEvent?.("themeChanged", () => {
        if (!localStorage.getItem("hse-appearance")) {
            state.appearance = tg.colorScheme === "dark"
                ? "dark"
                : "light";
            applyAppearance();
        }
    });
} catch (error) {
    // ignore
}


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function escapeAttribute(value) {
    return escapeHtml(value);
}


async function init() {
    try {
        tg.ready?.();
        tg.expand?.();
    } catch (error) {
        // ignore
    }

    setupInsets();

    state.appearance = getSavedAppearance();
    applyAppearance();

    try {
        await loadBootstrap();
        await loadSchedule("today");
    } catch (error) {
        const message = error.message || "Не удалось загрузить данные";

        let hint = "";
        if (error.status === 404 || /not found/i.test(message)) {
            hint = "Откройте бота в Telegram и выберите учебную группу, чтобы Mini App подтянул расписание.";
        } else if (error.status === 401 || /initdata/i.test(message)) {
            hint = "Откройте Mini App из Telegram — по прямой ссылке авторизация недоступна.";
        }

        $("scheduleContainer").innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">!</div>
                <p>${escapeHtml(message)}</p>
                ${hint ? `<p class="empty-hint">${escapeHtml(hint)}</p>` : ""}
            </div>
        `;
    }
}


init();