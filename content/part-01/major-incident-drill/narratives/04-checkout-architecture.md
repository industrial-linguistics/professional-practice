Speaker 1: Let's map the checkout flow so everyone knows where problems can start.
The web front end hits an API gateway, which then fans out to microservices for
payments, inventory, and orders. Those services talk to a clustered database and
ping the payment provider over the internet. Monitoring agents watch each step.
