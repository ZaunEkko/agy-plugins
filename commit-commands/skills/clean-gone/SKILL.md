---
name: clean-gone
description: Removes local branches whose remote tracking branches have been deleted.
---

# clean-gone

When requested to clean gone branches, run `git fetch --prune` and then delete local branches marked as `[gone]`.
