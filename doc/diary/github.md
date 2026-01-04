# Github

[> Back to TOC](entries.md)

I've used Github in a couple of projects before for several college projects, but it was never the focus.
The only knobs I've turned are branch protection rules and workflows.
The former protects my code from someone trying to nuke it.
The latter automates testing and ensures builds are clean and ready to merge.

## Commands

These are common commands that I use in my workflow

- git add \<file>\
    This is used to stage files for commits.
    Sometimes, all modified files should not be in a single commit.

- git checkout \<branch>\
    This is used to switch branches.

- git checkout \<branch> -- \<file>\
    This is used to switch a file from a certain branch.

- git commit -m \<message>\
    This is used to commit staged files with specified message.

- git fetch\
    This is used to fetch changes from the remote server.
    This is includes new branches and commits from other people.

- git pull\
    This is used to fast forward local branches to the remote branchs' commit.
    This is usually used in tandem with fetch.

- git pull origin \<branch>\
    This is used to merge remote branches to local branches.
    Merge conflicts are easier to resolve in vscode.

- git push\
    This is used to push local commits to remote branches.
