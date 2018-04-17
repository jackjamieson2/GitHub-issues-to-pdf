### This script scrapes the issues for a github project, and saves each one as a PDF.

import pdfkit
import requests
import re
import os
from bs4 import BeautifulSoup

from datetime import datetime


# repository to fetch from (e.g. jackjamieson2/GitHub-issues-to-pdf)
repository = 'jackjamieson2/yarns-indie-reader'

output_dir = 'Exported PDFs/' + repository + "/"

#Options
generate_auto_tags = True   # True/False. If true will add automatically generated tags to 
                            # bottom of the PDF in the form ##[tag]. See autotags() function for details
                        

print("starting...")
# Autotags
def autotags(soup):
    referenced = False
    commit_found = False
    tags = "<br><h1>Tags</h1>"
    tags+="<br>###status: " + soup.select(".TableObject-item .State")[0].text

    for item in soup.select('.discussion-item'):
        if str(item).find('This was referenced')>=0:
            referenced = True
        if str(item).find('referenced this issue')>=0:
            referenced = True
        if str(item).find('id="ref-commit-')>=0:
            commit_found = True
    if referenced == True:
        tags+="<br>###referenced"
    if commit_found == True:
        tags+="<br>###referenced_in_commit"
           
    for item in soup.select('.labels a'):
        tags+="<br>###current_label: " + item.text
    
    for item in soup.select('.IssueLabel a'):
        tags+="<br>###past_or_present_label: " + item.text
            
    participants_N = len(soup.select('.participant-avatar'))
    if participants_N ==1:
        tags+="<br>###1_participant"
    elif participants_N ==2:
        tags+="<br>###2_participants"
    elif participants_N >2:
        tags+="<br>###>=3_participants" + "(" + str(participants_N) + ")"
            
    for item in soup.select('.participant-avatar'):
        participant_name = re.sub("/","",item.get('href'))
        tags+="<br>###participant: " + participant_name
        
    for item in soup.select('.assignee'):
        tags+="<br>###assignee: " + item.text
          
    return tags

def log_error(error):   
    if not os.path.isfile(output_dir + "error_log.txt"):
        # Log file does not exist, so write explanatory header  
        with open(output_dir + "error_log.txt", "a") as myfile:
            myfile.write("Errors reported for the following URLs, please check to ensure the generated PDFs are correct.")
    with open(output_dir + "error_log.txt", "a") as myfile:
        myfile.write("\n\n" + str(datetime.now()) + "\n" + error)
        myfile.close()
    return
 
#Options
options = {
    'dpi':'300' # This zooms in to make the PDFs more readable (recommended) 
}

# Look up how many issues the repository has
issue_count = 0
r = requests.get('https://github.com/' + repository + '/issues?q=is%3Aissue')
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "lxml")
    issue = soup.find(class_="js-issue-row")
    issue_count = int(re.sub('issue_',"",issue.get('id')))
    print(str(issue_count) + " issues found")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    errors = []
    # Iterate through each issue page
    for i in range (1,issue_count +1):
        url = 'https://github.com/' + repository + '/issues/' + str(i)
        r = requests.get(url)
        if r.status_code == 200:
            print('\nConverting page to PDF: ' + url)
            c = r.text
            # Strip versioning number from <link> paths (e.g. example.css?1234 -> example.css)
            # This is needed to avoid an error with wkpdftohtml
            # see thread at https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2051
            html = re.sub('#(\.css|\.js)\?[^"]+#', '$1', c)
            soup = BeautifulSoup(html, "lxml")
            html_head = str(soup.head)
            html_body = str(soup.find(class_='repohead'))
            html_body = str(html_body) + str(soup.find(id='show_issue'))
            if generate_auto_tags == True:
                tags = autotags(soup)
            else:
                tags = ""
            
            full_html = html_head + html_body + tags

            try:
                pdfkit.from_string(full_html, output_dir +str(i) +'.pdf', options=options)
            except:
                log_error(url)

                
                
        elif r.status_code == 404:
            print('\n404 not found: ' + url  )

    print('\n\nFinished!\nSaved PDFs for ' + str(i) + ' issues.' )
    print('Find your exported PDFs in ' +output_dir )
else:
    print("Repository not found: " + repository)