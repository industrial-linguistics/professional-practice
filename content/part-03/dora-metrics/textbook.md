Picture the monthly release meeting at Meridian Insurance, a mid-sized firm with a claims platform that most of its two thousand staff touch every day. The head of operations wants to push the next release back a fortnight because the last one caused a Saturday outage. The development manager wants to ship this week because three teams have finished features promised to customers. Both are certain they are right, and the meeting is drifting towards a decision by seniority and stamina.

For much of the industry's history, that was the state of the argument. Speed and stability were treated as opposite ends of a rope, and organisations chose a position through instinct and recent trauma. The DORA research programme matters because it gave teams a way to test that story with delivery data. DORA's research and definitions continue to evolve, so use its current guidance rather than memorising a diagram from an old report. [@dora-research; @dora-metrics]

## From The Original Four Keys To Five Metrics

DORA began as DevOps Research and Assessment, associated with researchers including Nicole Forsgren, Jez Humble and Gene Kim. Its long-running surveys examined software-delivery practices and organisational outcomes across industries. The original model became widely known through four key measures: deployment frequency, lead time for changes, change failure rate and time to restore service.

The current model has five measures and more precise names. DORA explains that the model changed with the technology landscape: *failed deployment recovery time* replaced the broader MTTR label, and *deployment rework rate* became a separate measure. That history matters because dashboards, job interviews and older books still refer to “the four DORA metrics”. They are describing an earlier version, not an entirely different framework. [@dora-metrics]

DORA organises the current measures under throughput and instability:

- **Change lead time** measures the time from a change being committed to version control until it is running in production. Lower is generally better.
- **Deployment frequency** measures the number of deployments in a period, or the time between deployments. More frequent delivery can indicate smaller batches and a smoother path to production.
- **Failed deployment recovery time** measures how long it takes to recover from a deployment failure that requires immediate intervention. Lower is better.
- **Change fail rate** is the proportion of deployments that need immediate intervention, such as a rollback or hotfix. Lower is better.
- **Deployment rework rate** is the proportion of unplanned deployments made because of a production incident. Lower is better.

The categories are not a management scorecard with one winning number. They describe how changes move and what instability follows. A team deploying daily but performing emergency rework after every third release has produced motion, not dependable delivery.

## Read Direction And Context, Not A Universal Pass Mark

Read each metric as a direction of travel for one application or service. A team with changes waiting weeks for a manual test cycle has a different constraint from a team that deploys quickly but spends every afternoon on hotfixes. The first team should investigate the path to production; the second should investigate why planned changes repeatedly create unplanned work.

Do not combine unlike services into a single league table. A mobile consumer application, a safety-critical control system and a quarterly mainframe release operate under different risk, regulation and demand. DORA's current guidance warns that service context matters and that comparisons between unlike applications can mislead. Use the measures to compare a service with its own recent performance and to identify the next bottleneck. [@dora-metrics]

The measurements are also indicators, not proof of causation. DORA reports that they predict organisational performance and team well-being, and its research repeatedly finds that speed and stability are not general trade-offs. Those findings support an improvement hypothesis; they do not prove that increasing a dashboard number will create profit. Delivery performance can improve because teams reduce batch size, automate tests, simplify architecture and learn from failures. Chasing the number while ignoring those capabilities reverses the logic.

## Why Small Changes Can Improve Speed And Stability

Return to Meridian's release argument. A monthly release accumulates many changes into one event. When it breaks, the team must search a large set of possible causes, rollback carries more business risk, and the next batch begins queuing while the incident is still being understood.

A team that deploys small changes frequently has a narrower search space. A failed change is easier to identify, revert or repair; automation runs against each small increment; and recovery becomes a routine path rather than an improvised emergency. Frequent deployment is not automatically safe, but small batches, tested rollback and fast feedback can improve both throughput and stability. The pipeline, branching and error-budget practices in the rest of this part show how.

This reframes the release meeting. The useful question is not “should operations or development win?” It is “what evidence shows that this service can move a smaller change safely, and which part of the delivery system currently prevents that?” The answer may still be to delay a release. The difference is that the delay addresses a named risk rather than preserving a habit.

## Measure Without Weaponising

Metrics help only when teams use them as evidence about a delivery system.

Track trends rather than isolated weeks. Correlate delivery data with user outcomes and incident records. Review the five measures together so that apparent throughput cannot hide instability. Pull data from version control, deployment tooling and incident systems where practical, but do not spend months building perfect integrations before holding the first improvement conversation.

Avoid incentives tied to a single measure. Once teams are ranked by deployment frequency, they can split one release into several without improving the service. Once recovery time becomes a target, they can close incidents early. DORA's own guidance warns against setting a metric as the goal, relying on one metric, comparing unlike systems and turning improvement into competition. [@dora-metrics]

The healthier routine is:

1. Choose one application or service and establish a transparent baseline.
2. Map its delivery path and identify the largest source of waiting or instability.
3. Agree on one improvement, an owner and a review date.
4. Observe all five measures alongside user and operational outcomes.
5. Keep, adapt or reverse the intervention based on the result.

The team owns the interpretation. Managers can remove constraints and fund improvement, but the numbers should not become a device for allocating blame or bonuses.

## Use The Current Model Precisely

You should now be able to explain the original four-key model when it appears in older material and use the current five-metric model in new work. More importantly, you should be able to challenge two common errors: treating speed and stability as automatic enemies, and treating a metric as a lever that can be pulled without changing the delivery system underneath it.

For Meridian, the next step is not another argument. It is a service-level baseline, a map of the release path, and a smaller release whose outcome can be observed. Teams that measure delivery performance can improve it deliberately. Teams that reward the appearance of performance teach people to improve the dashboard.
