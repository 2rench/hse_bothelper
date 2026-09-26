const tg = window.Telegram?.WebApp || {};


const TRANSLATIONS = {
    ru: {
        today: "Сегодня",
        tomorrow: "Завтра",
        week: "Неделя",
        sessions: "Сессия",
        profile: "Профиль",
        loading: "Загружаем расписание…",
        loadingShort: "Загружаем…",
        noToday: "На сегодня пар нет.",
        noTomorrow: "На завтра пар нет.",
        noWeek: "На этой неделе пар нет.",
        noLessons: "Пар нет.",
        chooseGroup: "Сначала выбери группу.",
        settings: "Настройки",
        notifications: "Уведомления",
        appearance: "Оформление",
        theme: "Тема",
        interface: "Интерфейс",
        light: "Светлая",
        dark: "Тёмная",
        excludePairs: "Исключить пары",
        excludePairsHint: "Управление скрытыми предметами",
        calendar: "Календарь",
        calendarHint: "Подписка на расписание",
        scheduleUpdates: "Изменения расписания",
        scheduleUpdatesHint: "Уведомления о новых изменениях",
        tomorrowNotif: "Завтрашнее расписание",
        tomorrowNotifHint: "Напоминание о парах",
        on: "ВКЛ",
        off: "ВЫКЛ",
        startAt: "Начнёшь в",
        endAt: "закончишь в",
        noSessions: "Сессий пока нет.",
        noSessionLessons: "Для этой сессии расписания нет.",
        noSubjectsWeek: "На этой неделе предметов нет.",
        excludedDescription: "Нажми на предмет, чтобы скрыть его из сегодняшнего, завтрашнего и недельного расписания.",
        groupNotSelected: "Группа не выбрана",
        student: "Студент",
        schedule: "Расписание",
        current: "текущая",
        loadError: "Не удалось загрузить данные",
        hintGroup: "Откройте бота в Telegram и выберите учебную группу, чтобы Mini App подтянул расписание.",
        hintAuth: "Откройте Mini App из Telegram — по прямой ссылке авторизация недоступна.",
        pairExcluded: "Пара исключена",
        pairIncluded: "Пара снова включена",
        themeChanged: "Оформление:",
        now: "Идёт сейчас",
        error: "Ошибка",
    },
    en: {
        today: "Today",
        tomorrow: "Tomorrow",
        week: "Week",
        sessions: "Session",
        profile: "Profile",
        loading: "Loading schedule…",
        loadingShort: "Loading…",
        noToday: "No classes today.",
        noTomorrow: "No classes tomorrow.",
        noWeek: "No classes this week.",
        noLessons: "No classes.",
        chooseGroup: "Choose your group first.",
        settings: "Settings",
        notifications: "Notifications",
        appearance: "Appearance",
        theme: "Theme",
        interface: "Interface",
        light: "Light",
        dark: "Dark",
        excludePairs: "Exclude classes",
        excludePairsHint: "Manage hidden subjects",
        calendar: "Calendar",
        calendarHint: "Schedule subscription",
        scheduleUpdates: "Schedule changes",
        scheduleUpdatesHint: "Notifications about changes",
        tomorrowNotif: "Tomorrow's schedule",
        tomorrowNotifHint: "Class reminder",
        on: "ON",
        off: "OFF",
        startAt: "Start at",
        endAt: "end at",
        noSessions: "No sessions yet.",
        noSessionLessons: "No classes for this session.",
        noSubjectsWeek: "No subjects this week.",
        excludedDescription: "Tap a subject to hide it from the schedule.",
        groupNotSelected: "Group not selected",
        student: "Student",
        schedule: "Schedule",
        current: "current",
        loadError: "Failed to load data",
        hintGroup: "Open the bot in Telegram and choose your group first.",
        hintAuth: "Open the Mini App from Telegram — direct link has no auth.",
        pairExcluded: "Class excluded",
        pairIncluded: "Class restored",
        themeChanged: "Theme:",
        now: "Now",
        error: "Error",
    },
    fr: {
        today: "Aujourd'hui",
        tomorrow: "Demain",
        week: "Semaine",
        sessions: "Session",
        profile: "Profil",
        loading: "Chargement…",
        loadingShort: "Chargement…",
        noToday: "Pas de cours aujourd'hui.",
        noTomorrow: "Pas de cours demain.",
        noWeek: "Pas de cours cette semaine.",
        noLessons: "Pas de cours.",
        chooseGroup: "Choisis d'abord un groupe.",
        settings: "Paramètres",
        notifications: "Notifications",
        appearance: "Apparence",
        theme: "Thème",
        interface: "Interface",
        light: "Clair",
        dark: "Sombre",
        excludePairs: "Exclure des cours",
        excludePairsHint: "Gérer les matières masquées",
        calendar: "Calendrier",
        calendarHint: "Abonnement à l'emploi du temps",
        scheduleUpdates: "Modifications",
        scheduleUpdatesHint: "Notifications des changements",
        tomorrowNotif: "Cours de demain",
        tomorrowNotifHint: "Rappel des cours",
        on: "ON",
        off: "OFF",
        startAt: "Début à",
        endAt: "fin à",
        noSessions: "Aucune session.",
        noSessionLessons: "Pas de cours pour cette session.",
        noSubjectsWeek: "Aucune matière cette semaine.",
        excludedDescription: "Appuie sur une matière pour la masquer.",
        groupNotSelected: "Groupe non choisi",
        student: "Étudiant",
        schedule: "Emploi du temps",
        current: "actuelle",
        loadError: "Échec du chargement",
        hintGroup: "Ouvre le bot dans Telegram et choisis ton groupe.",
        hintAuth: "Ouvre la Mini App depuis Telegram.",
        pairExcluded: "Cours exclu",
        pairIncluded: "Cours rétabli",
        themeChanged: "Thème :",
        now: "En cours",
        error: "Erreur",
    },
    zh: {
        today: "今天",
        tomorrow: "明天",
        week: "本周",
        sessions: "考试周",
        profile: "个人中心",
        loading: "加载中…",
        loadingShort: "加载中…",
        noToday: "今天没有课。",
        noTomorrow: "明天没有课。",
        noWeek: "本周没有课。",
        noLessons: "没有课。",
        chooseGroup: "请先选择班级。",
        settings: "设置",
        notifications: "通知",
        appearance: "外观",
        theme: "主题",
        interface: "界面",
        light: "浅色",
        dark: "深色",
        excludePairs: "排除课程",
        excludePairsHint: "管理隐藏的科目",
        calendar: "日历",
        calendarHint: "订阅课程表",
        scheduleUpdates: "课程表变化",
        scheduleUpdatesHint: "变更通知",
        tomorrowNotif: "明天的课程",
        tomorrowNotifHint: "课程提醒",
        on: "开",
        off: "关",
        startAt: "开始于",
        endAt: "结束于",
        noSessions: "暂无考试。",
        noSessionLessons: "该考试周没有课程。",
        noSubjectsWeek: "本周没有科目。",
        excludedDescription: "点击科目以从课程表中隐藏。",
        groupNotSelected: "未选择班级",
        student: "学生",
        schedule: "课程表",
        current: "当前",
        loadError: "加载失败",
        hintGroup: "请在 Telegram 中打开机器人并选择班级。",
        hintAuth: "请从 Telegram 打开小程序。",
        pairExcluded: "已排除",
        pairIncluded: "已恢复",
        themeChanged: "主题：",
        now: "正在进行",
        error: "错误",
    },
};


const LANGUAGE_THEMES = {
    english: "en",
    french: "fr",
    chinese: "zh",
};


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
    lastSchedule: null,
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


function currentLang() {
    const theme = state.profile?.theme || "default";

    if (LANGUAGE_THEMES[theme]) {
        return LANGUAGE_THEMES[theme];
    }

    return "ru";
}


function t(key) {
    const lang = currentLang();
    const dict = TRANSLATIONS[lang] || TRANSLATIONS.ru;
    return dict[key] ?? TRANSLATIONS.ru[key] ?? key;
}


function pluralPairs(n) {
    const lang = currentLang();

    if (lang === "en") {
        return n === 1 ? "class" : "classes";
    }
    if (lang === "fr") {
        return "cours";
    }
    if (lang === "zh") {
        return "节课";
    }

    const mod10 = n % 10;
    const mod100 = n % 100;

    if (mod10 === 1 && mod100 !== 11) return "пара";
    if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return "пары";
    return "пар";
}


function applyTranslations() {
    const lang = currentLang();
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.dataset.i18n;
        const dict = TRANSLATIONS[lang] || TRANSLATIONS.ru;
        const value = dict[key] ?? TRANSLATIONS.ru[key];
        if (value != null) {
            el.textContent = value;
        }
    });

    renderProfile();
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

    const separator = url.includes("?") ? "&" : "?";
    const bustedUrl = `${url}${separator}_t=${Date.now()}`;

    const response = await fetch(bustedUrl, {
        ...options,
        headers,
        cache: "no-store",
    });

    let data = null;
    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {
        const message = data?.detail || `${t("error")} ${response.status}`;
        const err = new Error(message);
        err.status = response.status;
        throw err;
    }

    return data;
}


function setupInsets() {
    try {
        const insets = tg.contentSafeAreaInset || {};
        const safeTop = insets.top || 0;
        const safeBottom = insets.bottom || 0;

        const top = Math.max(safeTop, 12);
        const bottom = safeBottom;

        const root = document.documentElement;
        root.style.setProperty("--inset-top", `${top}px`);
        root.style.setProperty("--inset-bottom", `${bottom}px`);
    } catch (error) {
        document.documentElement.style.setProperty("--inset-top", "12px");
        document.documentElement.style.setProperty("--inset-bottom", "0px");
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
    applyTranslations();
    applyAppearance();

    rerenderCurrentSchedule();
}


function rerenderCurrentSchedule() {
    const data = state.lastSchedule;

    if (!data) return;

    const container = $("scheduleContainer");

    if (!container) return;

    if (!data.lessons || !data.lessons.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">
                    ${escapeHtml(state.theme?.tokens?.lesson || "○")}
                </div>
                <p>${escapeHtml(emptyMessageFor(data.view))}</p>
            </div>
        `;
        return;
    }

    if (data.view === "week") {
        renderWeek(data.lessons);
        return;
    }

    const shouldHighlight =
        data.view === "today";

    container.innerHTML =
        renderTimeRange(data.lessons) +
        data.lessons
            .map(lesson =>
                lessonCard(lesson, {
                    highlightNow: shouldHighlight,
                })
            )
            .join("");
}


function renderProfile() {
    const firstName = state.identity?.first_name || t("student");
    const group = state.profile?.group_name || t("groupNotSelected");

    const nameEl = $("profileName");
    const groupEl = $("profileGroup");
    const subtitleEl = $("topbarSubtitle");

    if (nameEl) nameEl.textContent = firstName;
    if (groupEl) groupEl.textContent = group;

    if (subtitleEl) {
        subtitleEl.textContent =
            group === t("groupNotSelected")
                ? t("schedule")
                : group;
    }

    const avatarLetter =
        (firstName.trim().charAt(0) || "H").toUpperCase();

    const avatarBtn = $("avatarButton");
    const avatarProfile = $("profileAvatar");

    if (avatarBtn) avatarBtn.textContent = avatarLetter;
    if (avatarProfile) avatarProfile.textContent = avatarLetter;

    renderNotificationValues();
}


function renderNotificationValues() {
    const updates = state.profile?.schedule_updates;
    const tomorrow = state.profile?.tomorrow_notifications;

    const updatesElement = $("scheduleUpdatesValue");
    const tomorrowElement = $("tomorrowValue");

    if (!updatesElement || !tomorrowElement) return;

    updatesElement.textContent = updates ? t("on") : t("off");
    tomorrowElement.textContent = tomorrow ? t("on") : t("off");

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
        today: t("today"),
        tomorrow: t("tomorrow"),
        week: t("week"),
    };

    $("scheduleTitle").textContent = titles[view] || t("schedule");
}


function renderGreeting(greeting, view) {
    const bar = $("greetingBar");

    if (!bar) return;

    if (view !== "today" || !greeting) {
        bar.hidden = true;
        bar.textContent = "";
        return;
    }

    bar.hidden = false;
    bar.textContent = greeting;
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
                ? `${week} · ${t("current")}`
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


function parseTimeToMinutes(value) {
    const match = String(value || "").match(/(\d{1,2}):(\d{2})/);

    if (!match) return null;

    const hours = parseInt(match[1], 10);
    const minutes = parseInt(match[2], 10);

    if (Number.isNaN(hours) || Number.isNaN(minutes)) return null;

    return hours * 60 + minutes;
}


function parseLessonRange(value) {
    const text = String(value || "").trim();

    if (!text) return null;

    const matches = text.match(/\d{1,2}:\d{2}/g);

    if (!matches || matches.length < 2) return null;

    const start = parseTimeToMinutes(matches[0]);
    const end = parseTimeToMinutes(matches[matches.length - 1]);

    if (start == null || end == null) return null;

    return { start, end };
}


function nowMinutes() {
    const now = new Date();
    return now.getHours() * 60 + now.getMinutes();
}


function isLessonNow(lesson) {
    const range = parseLessonRange(lesson.lesson_time);

    if (!range) return false;

    const current = nowMinutes();

    return current >= range.start && current <= range.end;
}


function computeTimeRange(lessons) {
    if (!lessons || !lessons.length) return null;

    const first = parseLessonRange(lessons[0].lesson_time);
    const last = parseLessonRange(lessons[lessons.length - 1].lesson_time);

    if (!first || !last) return null;

    const format = minutes => {
        const h = Math.floor(minutes / 60);
        const m = minutes % 60;
        return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
    };

    return {
        start: format(first.start),
        end: format(last.end),
        count: lessons.length,
    };
}


function renderTimeRange(lessons) {
    const range = computeTimeRange(lessons);

    if (!range) return "";

    return `
        <div class="time-range">
            <span>${escapeHtml(t("startAt"))} <strong>${escapeHtml(range.start)}</strong></span>
            <span class="dot">·</span>
            <span>${escapeHtml(t("endAt"))} <strong>${escapeHtml(range.end)}</strong></span>
            <span class="dot">·</span>
            <span><strong>${range.count}</strong> ${escapeHtml(pluralPairs(range.count))}</span>
        </div>
    `;
}


function emptyMessageFor(view) {
    if (view === "today") return t("noToday");
    if (view === "tomorrow") return t("noTomorrow");
    if (view === "week") return t("noWeek");
    return t("noLessons");
}


async function loadSchedule(view) {
    state.view = view;

    showScreen(view);
    setActiveNav(view);
    updateScheduleHeader(view);

    const container = $("scheduleContainer");
    container.innerHTML = `<div class="loading">${escapeHtml(t("loading"))}</div>`;

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
            renderGreeting(null, view);
            renderSchedule(data);
            return;
        }

        $("weekPicker").hidden = true;

        const data = await api(`/api/schedule?view=${view}`);
        renderGreeting(data.greeting, view);
        renderSchedule(data);
    } catch (error) {
        renderGreeting(null, view);

        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">!</div>
                <p>${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}


function renderSchedule(data) {
    state.lastSchedule = data;

    const container = $("scheduleContainer");

    if (!data.lessons || !data.lessons.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">
                    ${escapeHtml(state.theme?.tokens?.lesson || "○")}
                </div>
                <p>${escapeHtml(emptyMessageFor(data.view))}</p>
            </div>
        `;
        return;
    }

    if (data.view === "week") {
        renderWeek(data.lessons);
        return;
    }

    const range = renderTimeRange(data.lessons);

    const shouldHighlight =
        data.view === "today";

    container.innerHTML =
        range +
        data.lessons
            .map(lesson =>
                lessonCard(lesson, {
                    highlightNow: shouldHighlight,
                })
            )
            .join("");
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


function lessonCard(lesson, options = {}) {
    const tokens = state.theme?.tokens || {};
    const meta = [];
    const isNow = options.highlightNow === true && isLessonNow(lesson);

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
        <article class="lesson-card ${isNow ? "current" : ""}">
            <div class="lesson-top">
                <div>
                    <div class="lesson-time">
                        ${escapeHtml(lesson.lesson_time || "—")}
                    </div>
                    <div class="lesson-number">
                        ${escapeHtml(lesson.lesson_number || "")} ${escapeHtml(pluralPairs(1))}
                    </div>
                </div>

                ${isNow ? `
                    <span class="lesson-badge">
                        ${escapeHtml(t("now"))}
                    </span>
                ` : ""}
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
        `<div class="loading">${escapeHtml(t("loadingShort"))}</div>`;
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
                <p>${escapeHtml(t("noSessions"))}</p>
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
    container.innerHTML = `<div class="loading">${escapeHtml(t("loadingShort"))}</div>`;

    try {
        const data = await api(
            `/api/sessions/${encodeURIComponent(session)}`
        );

        if (!data.lessons.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>${escapeHtml(t("noSessionLessons"))}</p>
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


function renderExcluded(data) {
    const container = $("excludedGrid");

    if (!data.subjects.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-symbol">—</div>
                <p>${escapeHtml(t("noSubjectsWeek"))}</p>
            </div>
        `;
        return;
    }

    const excluded = new Set(data.excluded);

    container.innerHTML = data.subjects
        .map(subject => {
            const active = excluded.has(subject);

            return `
                <button
                    type="button"
                    class="excluded-item ${active ? "active" : ""}"
                    data-action="toggle-excluded"
                    data-subject="${escapeAttribute(subject)}"
                >
                    <span class="subject-name">${escapeHtml(subject)}</span>
                    <span class="subject-mark">${active ? "×" : "＋"}</span>
                </button>
            `;
        })
        .join("");
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
                ? t("pairExcluded")
                : t("pairIncluded")
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
        applyTranslations();
        updateScheduleHeader(state.view);
        showToast(`${t("themeChanged")} ${data.theme.name}`);

        if (
            state.view === "today" ||
            state.view === "tomorrow" ||
            state.view === "week"
        ) {
            await loadSchedule(state.view);
        }
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

    const container = $("scheduleContainer");
    if (container) {
        container.innerHTML = `<div class="loading">${escapeHtml(t("loading"))}</div>`;
    }

    const tasks = [
        loadBootstrap().catch(error => ({ __error: error, __from: "bootstrap" })),
        loadSchedule("today").catch(error => ({ __error: error, __from: "schedule" })),
    ];

    const results = await Promise.all(tasks);

    const bootstrapFailure = results.find(
        r => r && r.__from === "bootstrap" && r.__error
    );

    if (bootstrapFailure) {
        const error = bootstrapFailure.__error;
        const message = error.message || t("loadError");

        let hint = "";
        if (error.status === 404 || /not found/i.test(message)) {
            hint = t("hintGroup");
        } else if (error.status === 401 || /initdata/i.test(message)) {
            hint = t("hintAuth");
        }

        if (container) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-symbol">!</div>
                    <p>${escapeHtml(message)}</p>
                    ${hint ? `<p class="empty-hint">${escapeHtml(hint)}</p>` : ""}
                </div>
            `;
        }
        return;
    }

    loadWeeks().catch(() => {});
}


setInterval(() => {
    if (
        state.view !== "today" &&
        state.view !== "tomorrow" &&
        state.view !== "week"
    ) {
        return;
    }

    const data = state.lastSchedule;

    if (!data) return;

    const container = $("scheduleContainer");

    if (!container) return;

    if (!data.lessons || !data.lessons.length) return;

    if (data.view === "week") {
        renderWeek(data.lessons);
        return;
    }

    const shouldHighlight =
        data.view === "today";

    container.innerHTML =
        renderTimeRange(data.lessons) +
        data.lessons
            .map(lesson =>
                lessonCard(lesson, {
                    highlightNow: shouldHighlight,
                })
            )
            .join("");
}, 60000);


init();