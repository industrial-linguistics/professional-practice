Speaker 1: A GitHub Actions workflow is defined in a YAML file. YAML is just a human-readable list of instructions, like a shopping list written in plain text.

Speaker 2: Each workflow starts with a trigger—maybe someone pushed code, opened a pull request, or a timer fired. That trigger launches one or more jobs which run on "runners," the virtual machines GitHub provides or your own servers.

Speaker 1: Inside a job you define individual steps. Those steps can call reusable actions from the community or simply run shell commands. Because the workflow lives next to the code, it goes through the same pull request review process, making automation changes visible and safe.
