# Pack: CLI tool

Compose with: `script` when starting as a one-off, and `infra-change` if distribution or
runtime environments are part of the project.

Command-line tools that are reused or distributed — Python, Perl, zsh, or compiled
binaries.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. Who uses the CLI and how often — you, a team, external users? [default: you and your
   team]

2. How is it distributed — checked into the repo, packaged (pip, npm, homebrew), or
   bundled as a container image? [default: script in the repo]

3. What environments must it run in — macOS, Linux, containers, CI systems? [default:
   your current development environment plus CI]

4. Does it need versioning and backwards compatibility — will old scripts or users rely
   on specific behaviours? [default: simple versioning; moderate compatibility]

5. Where does it read and write configuration and state — files, environment variables,
   databases? [default: local files and environment variables]

## Notes for the PRD

- Distribution and environment coverage in Q2 and Q3 are scope findings; a widely used
  tool needs more robustness than a personal helper.
- Versioning and compatibility in Q4 affect how aggressively you can refactor; record
  any guarantees as explicit requirements.
- Config and state named in Q5 should be checked against sensitivity and retention rules
  under core Q12.
