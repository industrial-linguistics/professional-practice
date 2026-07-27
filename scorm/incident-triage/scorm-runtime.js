(function () {
  "use strict";

  var STORAGE_KEY = "industrial-linguistics:professional-practice:incident-triage:v1";
  var REQUIRED_TOPICS = [
    "part-01/overview",
    "part-01/value-chain",
    "part-01/incident-vs-request",
    "part-01/escalation-tiers",
    "part-01/major-incident-drill",
    "part-01/servicenow-visual-guide",
    "part-01/job-roles-lifecycle"
  ];
  var api = null;
  var active = false;
  var finished = false;
  var state = {
    version: 1,
    location: "index.html",
    lessons: {},
    assessment: { answers: {}, score: 0, complete: false }
  };

  function findApi(win, depth) {
    try {
      while (win && depth > 0) {
        if (win.API) return win.API;
        if (win.parent === win) break;
        win = win.parent;
        depth -= 1;
      }
    } catch (error) {
      return null;
    }
    return null;
  }

  function locateApi() {
    var found = findApi(window, 12);
    if (!found && window.opener) found = findApi(window.opener, 12);
    return found;
  }

  function getValue(key) {
    if (!active) return "";
    try {
      return api.LMSGetValue(key) || "";
    } catch (error) {
      return "";
    }
  }

  function setValue(key, value) {
    if (!active) return false;
    try {
      return api.LMSSetValue(key, String(value)) === "true";
    } catch (error) {
      return false;
    }
  }

  function commit() {
    if (!active) return false;
    try {
      return api.LMSCommit("") === "true";
    } catch (error) {
      return false;
    }
  }

  function parseState(value) {
    if (!value) return null;
    try {
      var parsed = JSON.parse(value);
      if (!parsed || parsed.version !== 1) return null;
      parsed.lessons = parsed.lessons || {};
      parsed.assessment = parsed.assessment || { answers: {}, score: 0, complete: false };
      parsed.assessment.answers = parsed.assessment.answers || {};
      return parsed;
    } catch (error) {
      return null;
    }
  }

  function loadState() {
    var stored = active ? getValue("cmi.suspend_data") : "";
    if (!active) {
      try {
        stored = window.localStorage.getItem(STORAGE_KEY) || "";
      } catch (error) {
        stored = "";
      }
    }
    var parsed = parseState(stored);
    if (parsed) state = parsed;
  }

  function lessonsComplete() {
    return REQUIRED_TOPICS.every(function (topic) {
      var lesson = state.lessons[topic];
      return lesson && lesson.total > 0 && lesson.max >= lesson.total - 1;
    });
  }

  function updateLessonStatus() {
    if (!active) return;
    var complete = Boolean(state.assessment.complete);
    var score = Number(state.assessment.score) || 0;
    setValue("cmi.core.score.min", "0");
    setValue("cmi.core.score.max", "100");
    if (complete && lessonsComplete()) {
      // Some LMSs immediately turn any raw score below the manifest mastery
      // score into "failed". Do not publish a raw score until the learner has
      // met every completion condition.
      setValue("cmi.core.score.raw", String(score));
      setValue("cmi.core.lesson_status", score >= 70 ? "passed" : "failed");
    } else {
      setValue("cmi.core.lesson_status", "incomplete");
    }
  }

  function save(location) {
    if (location) {
      state.location = location;
    }
    var encoded = JSON.stringify(state);
    try {
      window.localStorage.setItem(STORAGE_KEY, encoded);
    } catch (error) {
      // LMS persistence remains available when local storage is blocked.
    }
    if (active) {
      setValue("cmi.suspend_data", encoded);
      setValue("cmi.core.lesson_location", state.location);
      setValue("cmi.core.exit", "suspend");
      updateLessonStatus();
      commit();
    }
    renderHubProgress();
  }

  function initialize() {
    api = locateApi();
    if (api) {
      try {
        active = api.LMSInitialize("") === "true";
      } catch (error) {
        active = false;
      }
    }
    if (active) {
      var status = getValue("cmi.core.lesson_status");
      if (!status || status === "not attempted") {
        setValue("cmi.core.lesson_status", "incomplete");
      }
    }
    loadState();
    save();
    return active;
  }

  function finish() {
    if (!active || finished) return;
    save();
    finished = true;
    try {
      api.LMSFinish("");
    } catch (error) {
      // The LMS owns final session cleanup.
    }
  }

  function recordLesson(topic, index, total) {
    var current = state.lessons[topic] || { max: -1, total: total };
    current.max = Math.max(Number(current.max) || 0, Number(index) || 0);
    current.total = Number(total) || current.total || 0;
    state.lessons[topic] = current;
    save(topic + "/index.html#" + (Number(index) + 1));
  }

  function assessmentState() {
    return JSON.parse(JSON.stringify(state.assessment));
  }

  function recordAssessment(answers, score, complete) {
    state.assessment = {
      answers: answers || {},
      score: Math.max(0, Math.min(100, Number(score) || 0)),
      complete: Boolean(complete)
    };
    save("incident-triage.html");
    return {
      score: state.assessment.score,
      passed: state.assessment.complete && lessonsComplete() && state.assessment.score >= 70,
      lessonsComplete: lessonsComplete()
    };
  }

  function resetAssessment() {
    state.assessment = { answers: {}, score: 0, complete: false };
    save("incident-triage.html");
  }

  function renderHubProgress() {
    if (!document.body || document.body.dataset.scormPage !== "hub") return;
    var completed = 0;
    document.querySelectorAll(".module-card[data-topic]").forEach(function (card) {
      var lesson = state.lessons[card.dataset.topic];
      var done = Boolean(lesson && lesson.total > 0 && lesson.max >= lesson.total - 1);
      card.classList.toggle("complete", done);
      var indicator = card.querySelector(".module-status");
      if (indicator) {
        indicator.textContent = done ? "●" : "○";
        indicator.setAttribute("aria-label", done ? "Complete" : "Not yet complete");
      }
      if (done) completed += 1;
    });
    var progress = document.getElementById("lesson-progress");
    if (progress) progress.textContent = completed + " of " + REQUIRED_TOPICS.length + " lessons completed";
    var resume = document.getElementById("resume-link");
    if (resume && state.location && state.location !== "index.html") {
      resume.href = state.location;
      resume.textContent = "Resume the module";
    }
  }

  function attachLessonTracking() {
    var dataElement = document.getElementById("lesson-data");
    if (!dataElement) return;
    var lesson;
    try {
      lesson = JSON.parse(dataElement.textContent || "{}");
    } catch (error) {
      return;
    }
    var topic = lesson.topicPath || document.body.dataset.topic;
    var total = Array.isArray(lesson.slides) ? lesson.slides.length : 0;
    if (!topic || !total) return;
    var storageKey = "professional-practice:" + topic + ":slide";
    function capture() {
      var index = 0;
      try {
        index = Number(window.localStorage.getItem(storageKey)) || 0;
      } catch (error) {
        index = 0;
      }
      recordLesson(topic, index, total);
    }
    var progress = document.getElementById("progress-fill");
    if (progress && window.MutationObserver) {
      new MutationObserver(capture).observe(progress, {
        attributes: true,
        attributeFilter: ["style"]
      });
    }
    document.addEventListener("click", function () {
      window.setTimeout(capture, 0);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        window.setTimeout(capture, 0);
      }
    });
    capture();
  }

  window.ProfessionalPracticeSCORM = {
    initialize: initialize,
    finish: finish,
    recordLesson: recordLesson,
    assessmentState: assessmentState,
    recordAssessment: recordAssessment,
    resetAssessment: resetAssessment,
    lessonsComplete: lessonsComplete,
    state: function () {
      return JSON.parse(JSON.stringify(state));
    },
    active: function () {
      return active;
    }
  };

  function start() {
    initialize();
    renderHubProgress();
    if (document.body.dataset.scormPage === "lesson") attachLessonTracking();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
  window.addEventListener("pagehide", finish);
  window.addEventListener("beforeunload", finish);
}());
