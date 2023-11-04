# Contributing to wahooMapsCreator <!-- omit in toc --> 

#### Table of contents <!-- omit in toc --> 
- [How to Contribute](#how-to-contribute)
  - [Developer Anaconda environment](#developer-anaconda-environment)
  - [Pylint](#pylint)
  - [Unittests](#unittests)
- [Structure of the repository](#structure-of-the-repository)
- [User directory](#user-directory)
- [Git Guidelines](#git-guidelines)
  - [No Merge Commits](#no-merge-commits)
  - [Pull Requests](#pull-requests)
    - [Pull Request Title](#pull-request-title)
      - [Types](#types)
    - [Squash Commit Summary](#squash-commit-summary)
      - [Example](#example)
- [Release](#release)
  - [Automatic CHANGELOG creation](#automatic-changelog-creation)
  - [PyPI commands](#pypi-commands)

## How to Contribute
1. Create a Anaconda environment for developers
    - 👉 [Developer Anaconda environment](#developer-anaconda-environment)
2. Create a branch by forking the repository and apply your change.
3. Commit and push your change on that branch.
4. Run Pylint with 10.00/10
5. Run unittests successfully
6. Create a pull request.
    - 👉 **Please follow the [Git Guidlines](#Git-Guidelines).**
7. Wait for our code review and approval, possibly enhancing your change on request.
    - Note that the wahooMapsCreator maintainers have many duties. So, depending on the required effort for reviewing, testing, and clarification, this may take a while.
8. Once the change has been approved and merged, we will inform you in a comment.
9. Celebrate! 🎉

### Developer Anaconda environment 
- /conda_env/gdal-user.yml is for creating Anaconda environment for users
- /conda_env/gdal-dev.yml is for creating Anaconda environment for developers

The Anaconda environment for development can be installed via

  - macOS/ Linux
```
conda env create -f ./conda_env/gdal-dev.yml
```
  - Windows
```
conda env create -f .\conda_env\gdal-dev.yml 
```

more information on [documentation for sharing Anaconda environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#exporting-an-environment-file-across-platforms)

The .yml files with only the installed packages were created via
```
conda env export > environment.yml --from-history
```

### Pylint
Run pylint for all relevant directories/files
```
pylint -j 0 ./wahoomc ./tests
```

### Unittests
Python unittests are defined in the directory `tests`.
They can be started via "Testing" pane from VSCode or via terminal in the root of the repo with
```
python -m unittest
```

For the `test_generated_files.py` unittests to run successful, static land-poligons-file and static country files are needed to ensure equal results. The country files are included in the repo in `tests/resources`, the land-poligons-file needs to be downloaded from https://1drv.ms/u/s!AnpNcYd7Zz7TnXorg_zZuvsbMGsJ?e=fL6zvM and extracted to `~/wahooMapsCreatorData/_unittest/` like this:
<img src="./pictures/unittest-land-poligons.png" alt="land-poligons extracted for unittests" width=50%>

More information about Python unittest can be read here: https://docs.python.org/3/library/unittest.html.

## Structure of the repository
There is one python coding base for both Windows and for macOS.
Differences between the different OS are the used programs.
The folders in the repo have the following purposes:
- `wahoo_mc` - custom python files
- `wahoo_mc/resources` - config, json files
- `wahoo_mc/tooling_win` - programs, scripts for Windows
- `tooling` - programs, scripts used by Windows and macOS to test and check the generated maps

## User directory
Files which are processed through the tool are stored in the user directory to be release-independent. The name of the directory is: `$user_directory/wahooMapsCreatorData` and has the follwing folders:
- root - generated files are saved here
- `_download` - all downloaded files are saved and extracted here
- `_tiles` - intermediate files per tile are stored here

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
After testing carefully, a Release will be created based on branch develop or a hotfix branch.

### Automatic CHANGELOG creation 
After installing [git-chglog](https://github.com/git-chglog/git-chglog) locally, the CHANGELOG.md can be generated with this command:  
```
git-chglog -o CHANGELOG.md
```

To generate the CHANGELOG.md for a upcoming release (no tag exists yet), the following command can be used:  
```
git-chglog -o CHANGELOG.md --next-tag v0.10.0
```

### PyPI commands
1. Change the version in setup.cfg and gdal-user.yml
2. Build a new release to publish to PyPI:  
```
py -m build
```
3. Publish these files to PyPI:  
```
twine upload dist\*
```
