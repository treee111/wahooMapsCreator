# Contributing to wahooMapsCreator <!-- omit in toc --> 

#### Table of contents <!-- omit in toc --> 
- [How to Contribute](#how-to-contribute)
- [Git Guidelines](#git-guidelines)
  - [No Merge Commits](#no-merge-commits)
  - [Pull Requests](#pull-requests)
- [Release](#release)
  - [Automatic CHANGELOG creation](#automatic-changelog-creation)
- [Structure of the repository](#structure-of-the-repository)
- [Anaconda environment](#anaconda-environment)

## How to Contribute
1. Create a branch by forking the repository and apply your change.
2. Commit and push your change on that branch.
3. Create a pull request in the relevant repository.
    - 👉 **Please follow the [Git Guidlines](#Git-Guidelines).**
4. Follow the link posted by the CLA assistant to your pull request and accept it, as described above.
5. Wait for our code review and approval, possibly enhancing your change on request.
    - Note that the UI5 developers have many duties. So, depending on the required effort for reviewing, testing, and clarification, this may take a while.
6. Once the change has been approved and merged, we will inform you in a comment.
7. Celebrate! 🎉

## Git Guidelines
### No Merge Commits
Please use [rebase instead of merge](https://www.atlassian.com/git/tutorials/merging-vs-rebasing) to update a branch to the latest master. This helps keeping a clean commit history in the project.

### Pull Requests
#### Pull Request Title
The pull request title is a short description of the change to be introduced in the repository.  
The pull request tilte will later on be used for the squash commit summary and then appear in the CHANGELOG.
- The title should be 50-70 characters long.
- The commit summary must be **prefixed** by one of the following types.

##### Types
- The commit summary must be **prefixed** by one of the following types.
    + Use `[FEATURE]` for new features / enhancements.
    + Use `[FIX]` for bugfixes.
    + Use `[DEV]` for development, infrastructure, test or CI topics.
    + Use `[BREAKING]` for breaking / incompatible changes.  
      _**Note:** The commit body of a breaking change should also include a paragraph starting with `BREAKING CHANGE:`.  
      This paragraph will be highlighted in the changelog._
    + Exceptions are changes created by automated processes like releases or dependency updates

#### Squash Commit Summary
The commit summary is the first line of the commit message.  
For a squash commit to appear in the CHANGELOG.md later on, it has to follow a certain naming pattern:
- [type] ... (#PR-number)
- The commit summary must be **prefixed** by one of the [types](#Types).
- In the end there must be the `#pull request number` to be automatically linked in Github

##### Example
```
[FEATURE] Add check for required input parameter for CLI and GUI (#41)
```
```
[FIX] Storing and interpretation of CLI arguments (#48)
```
## Release
Coding is updated in the develop-branch mainly via pull requests.  
After testing carefully, changes are merged into main and a Release will be created.

### Automatic CHANGELOG creation 
After installing [git-chglog](https://github.com/git-chglog/git-chglog) locally, the CHANGELOG.md can be generated with this command:  
```
git-chglog -o CHANGELOG.md
```

To generate the CHANGELOG.md for a upcoming release (no tag exists yet), the following command can be used:  
```
git-chglog -o CHANGELOG.md --next-tag v0.10.0
```

## Structure of the repository
There is one python coding base for both Windows and for macOS.
Differences between the different OS are the used programs.
The folders in the repo have the following purposes:
- common_download - all downloaded files are saved and extracted here
- common_python - custom python files
- common_resources - config, json files
- tooling - programs, scripts used by Windows and macOS
- tooling_windows - programs, scripts for Windows

## Anaconda environment
- /conda_env/enduser.yml is for creating Anaconda environment for users
- /conda_env/developer.yml is for creationg Anaconda environment for developers
- /conda_env/ ..mac.yml and ..win.yml files contain the installed packages including dependencies

.yml files with only the installed packages were installed via
```
conda env export > environment.yml --from-history
```
and the .yml files with the dependencies via
```
conda env export > environment.yml
```

The installation of Anaconda envirionments is described [here](docs/QUICKSTART_ANACONDA.md)

more information on [documentation for sharing Anaconda environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-an-environment-file-across-platforms)