# Pack: website

Compose with: `schema-change` for sites backed by a database the change touches.

Building or maintaining a public-facing site. Assumes the core bank has run. Ordered by
cost-of-missing; drop from the bottom.

1. Do any existing URLs change or disappear? [default: no — URLs are a public contract]
   - → *if they do:* are there inbound links or search rankings that matter, and do the
     old paths need to keep resolving?

2. Who edits the content after this ships — you, or someone who won't touch the repo?
   [default: you, in the repo]
   *(This one answer decides whether the project includes an editing surface. Getting it
   wrong late is the most expensive rework on this list.)*

3. Is there caching or a CDN between visitors and the origin? [default: yes — assume
   something serves stale content until proven otherwise]
   - → *if yes:* what invalidates it, and can you trigger that on deploy?

4. What does the site collect from visitors — forms, accounts, analytics, payments?
   [default: nothing]
   - → *if anything:* carry it back into core Q12 rather than answering both.

5. What browsers and devices have to work? [default: current evergreen browsers,
   mobile included]

## Notes for the PRD

- A Q2 answer of "someone non-technical" makes the editing workflow a requirement in its
  own right. It belongs in the numbered scope list, not in a sentence about the CMS.
- Q1 changes with real inbound links make redirects a deliverable, not an afterthought.
- Q3 is the reason "it works locally" and "it works in production" diverge. If the answer
  is unknown, log it as an assumption rather than letting it default silently.
