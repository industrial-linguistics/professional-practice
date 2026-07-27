(function () {
  "use strict";

  var stage = document.getElementById("case-stage");
  var resultPanel = document.getElementById("result-panel");
  var scoreValue = document.getElementById("score-value");
  var counter = document.getElementById("case-counter");
  var scenarios = [];
  var current = 0;
  var answers = {};

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function selectedCount() {
    return Object.keys(answers).reduce(function (total, caseId) {
      return total + Object.keys(answers[caseId] || {}).length;
    }, 0);
  }

  function correctCount() {
    var total = 0;
    scenarios.forEach(function (scenario) {
      scenario.decisions.forEach(function (decision) {
        if (answers[scenario.id] && answers[scenario.id][decision.id] === decision.correct) {
          total += 1;
        }
      });
    });
    return total;
  }

  function score() {
    var possible = scenarios.reduce(function (total, scenario) {
      return total + scenario.decisions.length;
    }, 0);
    if (!possible) return 0;
    return Math.round((correctCount() / possible) * 100);
  }

  function updateScore() {
    if (scoreValue) scoreValue.textContent = score() + " / 100";
  }

  function optionMarkup(option, selected) {
    return '<option value="' + escapeHtml(option.value) + '"' +
      (selected === option.value ? " selected" : "") + ">" +
      escapeHtml(option.label) + "</option>";
  }

  function decisionMarkup(scenario, decision, checked) {
    var selected = (answers[scenario.id] || {})[decision.id] || "";
    var correctness = "";
    var feedback = "";
    if (checked) {
      correctness = selected === decision.correct ? " correct" : " incorrect";
      feedback = '<p class="decision-feedback">' + escapeHtml(decision.explanation) + "</p>";
    }
    return '<div class="decision-field' + correctness + '">' +
      '<label for="' + escapeHtml(scenario.id + "-" + decision.id) + '">' +
      escapeHtml(decision.prompt) + "</label>" +
      '<select id="' + escapeHtml(scenario.id + "-" + decision.id) + '" ' +
      'data-decision="' + escapeHtml(decision.id) + '"' + (checked ? " disabled" : "") + ">" +
      '<option value="">Choose…</option>' +
      decision.options.map(function (option) {
        return optionMarkup(option, selected);
      }).join("") +
      "</select>" + feedback + "</div>";
  }

  function renderCase(checked) {
    var scenario = scenarios[current];
    if (!scenario) return;
    counter.textContent = "Case " + (current + 1) + " of " + scenarios.length;
    var caseAnswers = answers[scenario.id] || {};
    var ready = scenario.decisions.every(function (decision) {
      return Boolean(caseAnswers[decision.id]);
    });
    stage.innerHTML =
      '<article class="case-card">' +
      '<header class="case-header">' +
      '<p class="eyebrow">' + escapeHtml(scenario.queue) + "</p>" +
      "<h2>" + escapeHtml(scenario.title) + "</h2>" +
      '<div class="record-meta">' +
      scenario.meta.map(function (item) {
        return "<span>" + escapeHtml(item) + "</span>";
      }).join("") +
      "</div>" +
      '<p class="record-copy">' + escapeHtml(scenario.record) + "</p>" +
      "</header>" +
      '<div class="decision-list">' +
      scenario.decisions.map(function (decision) {
        return decisionMarkup(scenario, decision, checked);
      }).join("") +
      "</div>" +
      '<div class="case-actions">' +
      (current > 0 ? '<button type="button" class="secondary" id="previous-case">Previous case</button>' : "") +
      (checked
        ? '<button type="button" id="next-case">' +
          (current === scenarios.length - 1 ? "See result" : "Next case") + "</button>"
        : '<button type="button" id="check-case"' + (ready ? "" : " disabled") + ">Check this record</button>") +
      "</div>" +
      "</article>";

    stage.querySelectorAll("select[data-decision]").forEach(function (select) {
      select.addEventListener("change", function () {
        answers[scenario.id] = answers[scenario.id] || {};
        answers[scenario.id][select.dataset.decision] = select.value;
        renderCase(false);
      });
    });
    var previous = document.getElementById("previous-case");
    if (previous) {
      previous.addEventListener("click", function () {
        current -= 1;
        renderCase(true);
      });
    }
    var check = document.getElementById("check-case");
    if (check) {
      check.addEventListener("click", function () {
        renderCase(true);
        updateScore();
        window.ProfessionalPracticeSCORM.recordAssessment(answers, score(), false);
      });
    }
    var next = document.getElementById("next-case");
    if (next) {
      next.addEventListener("click", function () {
        if (current === scenarios.length - 1) {
          renderResult();
        } else {
          current += 1;
          renderCase(Boolean(answers[scenarios[current].id]));
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      });
    }
  }

  function renderResult() {
    var finalScore = score();
    var report = window.ProfessionalPracticeSCORM.recordAssessment(answers, finalScore, true);
    stage.hidden = true;
    resultPanel.hidden = false;
    counter.textContent = "Lab complete";
    updateScore();
    var heading;
    var message;
    if (!report.lessonsComplete) {
      heading = "Good queue work. Finish the lessons to complete the module.";
      message = "Your assessment score is saved. The LMS will keep the module incomplete until all seven lessons have been completed.";
    } else if (finalScore >= 70) {
      heading = "The queue is under control.";
      message = "You passed the lab and the LMS has recorded the result.";
    } else {
      heading = "The queue needs another pass.";
      message = "Review the feedback, revisit the service-practice lessons and retry the lab.";
    }
    resultPanel.innerHTML =
      '<p class="eyebrow">Result</p>' +
      "<h2>" + escapeHtml(heading) + "</h2>" +
      '<div class="result-score">' + finalScore + "%</div>" +
      "<p>" + escapeHtml(message) + "</p>" +
      "<ul>" +
      "<li>" + correctCount() + " of " + selectedCount() + " decisions matched the recommended first action.</li>" +
      "<li>Pass mark: 70%.</li>" +
      "<li>Score, completion and resume data are reported through SCORM 1.2.</li>" +
      "</ul>" +
      '<div class="case-actions">' +
      '<a class="primary-action" href="index.html">Return to module</a>' +
      '<button type="button" class="secondary" id="retry-lab">Retry the lab</button>' +
      "</div>";
    document.getElementById("retry-lab").addEventListener("click", function () {
      answers = {};
      current = 0;
      window.ProfessionalPracticeSCORM.resetAssessment();
      resultPanel.hidden = true;
      stage.hidden = false;
      renderCase(false);
      updateScore();
    });
  }

  function restore() {
    var saved = window.ProfessionalPracticeSCORM.assessmentState();
    answers = saved.answers || {};
    if (saved.complete) {
      renderResult();
      return;
    }
    var firstIncomplete = scenarios.findIndex(function (scenario) {
      return scenario.decisions.some(function (decision) {
        return !answers[scenario.id] || !answers[scenario.id][decision.id];
      });
    });
    current = firstIncomplete < 0 ? scenarios.length - 1 : firstIncomplete;
    renderCase(Boolean(answers[scenarios[current].id]));
    updateScore();
  }

  fetch("assets/scenarios.json")
    .then(function (response) {
      if (!response.ok) throw new Error("Scenario data could not be loaded.");
      return response.json();
    })
    .then(function (data) {
      scenarios = data.scenarios || [];
      if (scenarios.length !== 5) throw new Error("Five scenarios are required.");
      restore();
    })
    .catch(function (error) {
      stage.innerHTML = "<h2>The lab could not start.</h2><p>" + escapeHtml(error.message) + "</p>";
    });
}());
