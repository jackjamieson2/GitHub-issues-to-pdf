# GitHub-issues-to-pdf
Downloads issues from a GitHub repository as PDFs

A simple script to download issues from a github project as PDFs.

## Instructions
Before running this script, there are three options to review. These are found near the top of the script under the heading "#OPTIONS:"

1. *Repository to fetch from*:  The most important setting. Enter the repository from which to select issues. Use the format "{owner}/{repository_name}".  For example this repository should be entered using "jackjamieson2/GitHub-issues-to-pdf"

2. *Output directory to save PDFs*: PDFs will be saved here. No need to change this in most cases 

3. *Generate automatic tags*: (True/False).  If true will add automatically generated tags to bottom of the PDF in the form "##[tag]". See autotags() function for details. Tags can be used to summarize issue status (open/closed), labels, whether this issue has been referenced elsewhere, assignees, and participants. 

