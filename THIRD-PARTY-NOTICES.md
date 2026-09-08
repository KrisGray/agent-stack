# Third-Party Notices

This package includes material adapted from third-party, MIT-licensed work.

## agent-skills (addyosmani/agent-skills) via @chankov/agent-skills

Eight specialist personas in `agents/` are adapted from
[@chankov/agent-skills](https://github.com/chankov/agent-skills) v0.4.2 (MIT),
itself a fork of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
(MIT). Both upstream projects retain their respective licenses; their notices
are reproduced below.

| File in this package | Relationship to @chankov/agent-skills v0.4.2 |
| --- | --- |
| `agents/planner.md` | Verbatim copy |
| `agents/builder.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |
| `agents/scout.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |
| `agents/documenter.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |
| `agents/code-reviewer.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |
| `agents/test-engineer.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |
| `agents/security-auditor.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |
| `agents/plan-reviewer.md` | Upstream file + added `model:` / `thinking:` frontmatter pins |

Everything else in this package — the pm kernel (`agents/pm.md`), the
`researcher` / `oracle` / `worker` personas, the charter format and templates,
the interview pack system, the `/pm`, `/hire-pm`, `/spec` and `/task` prompt
templates, and the scripts in `bin/` — is original to agent-stack.

## Distributed dependencies (installed by npm, not bundled)

agent-stack declares these MIT-licensed pi packages as dependencies and loads
their resources through its manifest. They remain their authors' work, under
their own licenses, each carrying its LICENSE in its installed directory:

- `pi-subagents` — the subagent runtime (personas, delegation, review fan-out)
- `@chankov/agent-skills` 0.4.2 — the execution pipeline commands and skills
- `pi-ask-user` — structured user questions
- `pi-prompt-template-model` — deterministic prompt pre-steps

The upstream license, as carried by both addyosmani/agent-skills and its
chankov fork:

```
MIT License

Copyright (c) 2025 Addy Osmani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
