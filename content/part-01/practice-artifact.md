Produce a one-page intake and escalation sheet for five incoming records. For each record, decide whether it is an incident, service request, problem, or change; assign an initial priority; name the support tier that should own the next step; and write the first customer-facing update.

The useful evidence is not the label by itself. Show the sentence or field that justified the classification, the handoff that should happen next, and the point at which the work would need an incident commander or another escalation path.


## Extension: modern role handoffs

Coralline is adding an AI assistant to its returns portal. It uses order records and the refund policy to recommend a response. A refund must be approved by an authorised person.

Assign responsibility for each of these six pieces of work. For each, give a role, an output to hand over, the recipient and the decision authority:

1. Define acceptable refund behaviour and the business rules.
2. Build the accessible interface and its connection to the refund service.
3. Supply current, trusted order and policy data.
4. Test unsafe requests, incorrect recommendations and unauthorised actions.
5. Approve release and make the service ready to support.
6. Respond when the assistant recommends a wrong refund after launch.

Then allocate the roles to a five-person team. Record where one person holds several roles, where a second person must review a decision, and who covers absence or an on-call handoff. Explain one difference between DevOps, SRE and platform work in your arrangement.

### Suggested response

This is one workable allocation. Other arrangements can work if the outputs and authorities are clear.

- **Needs and rules**. Business analyst and product manager give engineering agreed scenarios and acceptance criteria. Service owner agrees service scope with the business; the business assigns refund authority.
- **Interface and service**. Front-end/back-end or full-stack developers give testers a reviewed implementation; AI engineer supplies evaluated recommendations. Technical lead coordinates design within the agreed constraints.
- **Trusted data**. Data engineer and analytics engineer give AI/application engineers validated feeds and definitions; DBA supports recovery. Data owner authorises access; service owner agrees freshness requirements.
- **Quality and security**. QA/test automation and AppSec/AI red team give developers reproducible findings and the release decision-makers test results and remaining risks. Authorised test scope first; designated risk owners decide on remaining risk.
- **Release and readiness**. DevOps/CI/CD engineer provides a repeatable deployment; SRE agrees reliability checks and rollback; release manager gives the desk a support brief. Change authority and service owner act under the organisation's release governance.
- **Wrong refund**. Service desk records impact and informs users; application/AI support and SRE investigate and contain the fault; problem management coordinates follow-up. Incident lead coordinates recovery; an authorised business owner decides refund corrections.

A platform engineer could provide a supported deployment service used by several teams. A platform product manager would prioritise its users' needs. That differs from automating this one delivery workflow or owning the portal's reliability objectives. In a small team, those tasks may belong to the same person.

Check your map for unowned decisions, a maintainer for each component, and a clear route from a user report to technical and business action. A diagram full of job titles without those handoffs is not yet an operating arrangement.


For example, the five people could hold these combined responsibilities:

- Person A: service ownership, product priorities and business analysis; liaison with the business's refund authority.
- Person B: application development and technical leadership.
- Person C: data and AI engineering, including data freshness and model evaluation.
- Person D: infrastructure, delivery automation, reliability and release coordination.
- Person E: quality checks, support coordination and security testing within their competence and authorisation.

Person A should review business acceptance separately from the implementation; Person E should check the unsafe-request scenarios. Specialist security review may need external help. Agree who deputises for each person and what the team can actually support outside working hours. Combining titles does not create extra capacity.
