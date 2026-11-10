// Generated from narration.json by scripts/explainer_narration.py. Do not edit.
window.EXPLAINER_NARRATION={
 "audio": "narration.mp3",
 "duration": 92.933,
 "lines": [
  {
   "speaker": "Anna",
   "text": "Imagine you promised your app would be available 99.9% of the time. That still allows roughly nine hours of downtime a year.",
   "start": 0.6,
   "end": 9.351
  },
  {
   "speaker": "Greg",
   "text": "Site Reliability Engineering, or SRE, turns those promises into math we can track. The key tools are service level objectives, or SLOs, and the error budgets tied to them.",
   "start": 9.731,
   "end": 22.087
  },
  {
   "speaker": "Anna",
   "text": "By defining how reliable a service must be, we can decide when it's safe to launch new features and when it's time to pause and fix instability.",
   "start": 22.467,
   "end": 31.558
  },
  {
   "speaker": "Anna",
   "text": "An error budget is the small slice of allowable failure built into an SLO. If our target is 99.9% uptime, that gives us about forty minutes of downtime each month.",
   "start": 32.408,
   "end": 44.45
  },
  {
   "speaker": "Greg",
   "text": "As outages or performance issues occur, we \"spend\" that budget. When it's gone, engineering focuses on reliability work instead of shipping new features.",
   "start": 44.83,
   "end": 54.783
  },
  {
   "speaker": "Anna",
   "text": "This approach keeps everyone aligned. Product managers see how instability eats into development time, while engineers know exactly when to slow their release pace.",
   "start": 55.163,
   "end": 65.35
  },
  {
   "speaker": "Anna",
   "text": "Error budgets aren't just for ops teams. They spark conversations about risk across the organisation.",
   "start": 66.2,
   "end": 72.627
  },
  {
   "speaker": "Greg",
   "text": "When the budget burns down faster than expected, it's a sign our releases might be too risky or our SLO is unrealistic.",
   "start": 73.007,
   "end": 80.713
  },
  {
   "speaker": "Anna",
   "text": "Teams can agree to slow deployments, add more testing, or even adjust the SLO if customer impact warrants it. The data helps remove emotion from those decisions.",
   "start": 81.093,
   "end": 91.933
  }
 ]
};
