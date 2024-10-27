# jira
Jira related python scripts
=====================================================

# Release Notes Creation
This is my first attempt to create release notes automatically based on git log.

## Dependency
    pip install jira 
    you shall have credentials to login to jira, 
    one liner git log (a gitlog example is available in the repo)

## How to run
    usage: python relase_notes.py [-h] [-p PATH] [-d] gitlog
    It create release notes based on gitlog file
    positional arguments:
        gitlog                git log file conatining one liner git log
    options:
        -h, --help            show this help message and exit
        -p PATH, --path PATH  path, where release_notes shall be saved, otherwise it will be saved in current folder
        -d, --debug_info      create debug/log file (csv format) with some extra info
        -l, --labels          add list of labels to filter only those jira issues

    python release_notes.py gitlog.txt

## Output
    Release notes will be created in html format in current folder if -p option is not used

## How to create git log
Git Log can be created using following command, depends on what fit suits your need.
Script depends on one line gitlog hence we must use --oneline option while creating git log
to remove commit id, we use --pretty formatting

    1. Git log between two tags
    git log --oneline --pretty=format:"%s" <from_tag>..<to_tag> > gitlog.txt 

    2. Git log from a tag upto the head of branch
    git log --oneline --pretty=format:"%s" <your_tag>..HEAD > gitlog.txt 

    3. Git log between last tag  upto the head of branch. in this case you dont need what last tag you used
    git log --oneline  --pretty=format:"%s" $(git describe --tag --abbrev=0)..HEAD > gitlog.txt

In case you need to know what tags are put on your branch, you can use below git command to list

## Last 3 tags on master branch
    git log --simplify-by-decoration --decorate --pretty=oneline "master" | fgrep 'tag:' | head -n 3


=========================================================================================================
=========================================================================================================

# Road map kind of view in excel
This is my first attempt to create jira backlog roadmap view in excel sheet

## Dependency
    pip install jira
    pip install XlsxWriter 
 
## How to run
    usage: python roadmap.py [-h] [-p PATH] project_key

    It creates jira backlog roadmap view in excel sheet
    positional arguments:
        project_key           Jira project key 
    options:
        -h, --help            show this help message and exit
        -p PATH, --path PATH  path, where excel sheet shall be saved, otherwise it will be saved in current folder

    python roadmap.py project_key

## Output
    Roadmap view  will be created in excel sheet  in current folder if -p option is not used
    
