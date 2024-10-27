"""
This module create Road map kind of view in excel sheet based on JIRA project.
Expeaction is that we create epics and stories in JIRA and link them together.
all estimations are done on Stories in hours.
Epics can also have the estimations, if case epics is not broken down into stories yet.
"""
__version__ = '0.1'
__author__ = 'Sanju Koli'

import os
import re
import getpass
import argparse
from jira import JIRA
from time import localtime, strftime
import urllib3
import xlsxwriter

# to disable SSL certificate warting 
urllib3.disable_warnings()

JIRA_URL = 'https://jira.com/'  # jira server url
link =  JIRA_URL + 'browse/' # + issue key
hours_per_day = 7.5
sorting = 'ASC'     #sorting ASC or DESC
project = {'key': '', 'name': ''}
epics = []





def write_to_excel(project, epics, epic_issues):

    timestamp = strftime("%Y%m%d",localtime())
    filename = '%s_%s.xlsx'%(project['name'], timestamp)
    filepath = os.path.join(args.path, filename)
    
    workbook = xlsxwriter.Workbook(filepath)  # create excel file
    worksheet = workbook.add_worksheet(project['name'])  # create worksheet
    worksheet.outline_settings(symbols_below = False)  # summary row at top
    worksheet.freeze_panes(1, 0)  # freeze first row
    worksheet.set_column("A:A", 10)
    worksheet.set_column("B:B", 30)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 60)
    worksheet.set_column("E:E", 10)
    worksheet.set_column("F:F", 15)
    worksheet.set_column("G:G", 15)
    worksheet.set_column('H:H', 15, None, {'hidden': True})
    worksheet.set_column('I:I', 15, None, {'hidden': True})
    worksheet.set_column("J:J", 10)
    worksheet.set_column("K:K", 10)
    worksheet.set_column("L:L", 10)

    header_format = workbook.add_format({'bold': True, "valign": "vcenter", 'bg_color': '#f3f6f4'})
    header_format.set_text_wrap()
    epic_row_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})

    worksheet.set_row(0, 26, header_format)
    
    worksheet.write('A1', 'Project key')
    worksheet.write('B1', 'Project name')
    worksheet.write('C1', 'Epic')
    worksheet.write('D1', 'Issue')
    worksheet.write('E1', 'Issue type')
    worksheet.write('F1', 'Isuue key')
    worksheet.write('G1', 'Status')
    worksheet.write('H1', 'Assingee')
    worksheet.write('I1', 'Reporter')
    worksheet.write('J1', 'Remaining Estimate')
    worksheet.write('K1', 'Time Spent')
    worksheet.write('L1', 'Original Estimate')
    
    i = 2 # row number
    epic_rows = []
    for epic in epics:
        worksheet.set_row(i-1, None, None, {'level': 1, 'collapsed': True})
        worksheet.write('A%s'%i, project['key'], epic_row_format)
        worksheet.write('B%s'%i, project['name'], epic_row_format)
        worksheet.write('C%s'%i, epic['summary'], epic_row_format)
        worksheet.write('D%s'%i, '', epic_row_format)
        worksheet.write('E%s'%i, epic['type'], epic_row_format)
        worksheet.write('F%s'%i, epic['key'], epic_row_format)
        worksheet.write('G%s'%i, epic['status'], epic_row_format)
        worksheet.write('H%s'%i, epic['assignee'], epic_row_format)
        worksheet.write('I%s'%i, epic['reporter'], epic_row_format)
        
        next_row = write_epic_issues(worksheet, project, epic_issues[epic['key']], i+1)

        epic_remaining_estimate = round(epic['remaining_estimate']/3600, 1) if epic['remaining_estimate'] else 0
        epic_time_spent = round(epic['time_spent']/3600, 1) if epic['time_spent'] else 0
        epic_original_estimate = round(epic['original_estimate']/3600, 1) if epic['original_estimate'] else 0
        if len(epic_issues[epic['key']]) > 0:
            worksheet.write('J%s'%i, "=SUM(J%s:J%s)+%f"%(i+1, next_row-1, epic_remaining_estimate), epic_row_format)
            worksheet.write('K%s'%i, "=SUM(K%s:K%s)+%f "%(i+1, next_row-1, epic_time_spent), epic_row_format)
            worksheet.write('L%s'%i, "=SUM(L%s:L%s)+%f"%(i+1, next_row-1, epic_original_estimate), epic_row_format)
        else:
            worksheet.write('J%s'%i, epic_remaining_estimate, epic_row_format)
            worksheet.write('K%s'%i, epic_time_spent, epic_row_format)
            worksheet.write('L%s'%i, epic_original_estimate, epic_row_format)
            
        epic_rows.append(i)
        i = next_row
    #for loop epics
    
    i = add_total_row(worksheet, project, i, epic_rows, epic_row_format)
    
    # Set the autofilter.
    worksheet.autofilter("A1:L%s"%i)   
    workbook.close()
    print("Roadmap created at: %s"%filepath)

def write_epic_issues(worksheet, project, issues, row):
    i = row
    for issue in issues:
        worksheet.set_row(i-1, None, None, {'level': 2, 'hidden': True})
        worksheet.write('A%s'%i, project['key'])
        worksheet.write('B%s'%i, project['name'])
        
        worksheet.write('D%s'%i, issue['summary'])
        worksheet.write('E%s'%i, issue['type'])
        worksheet.write('F%s'%i, issue['key'])
        worksheet.write('G%s'%i, issue['status'])
        worksheet.write('H%s'%i, issue['assignee'])
        worksheet.write('I%s'%i, issue['reporter'])
        remaining_estimate = round(issue['remaining_estimate']/3600, 1) if issue['remaining_estimate'] else 0
        worksheet.write('J%s'%i, remaining_estimate)
        time_spent = round(issue['time_spent']/3600, 1) if issue['time_spent'] else 0
        worksheet.write('K%s'%i, time_spent)
        original_estimate = round(issue['original_estimate']/3600, 1) if issue['original_estimate'] else 0
        worksheet.write('L%s'%i, original_estimate)
        i += 1
    return i

def add_total_row(worksheet, project, i, epic_rows, row_format):
    #Grand Total row
    worksheet.write('A%s'%i, project['key'], row_format)
    worksheet.write('B%s'%i, project['name'], row_format)
    worksheet.write('C%s'%i, 'Grand Total Hours', row_format)
    
    str = ""
    for j in epic_rows:
        str = str + "J%s,"%j
    worksheet.write('J%s'%i, "=SUM(%s)"%str[:-1], row_format)
    
    str = ""
    for j in epic_rows:
        str = str + "K%s,"%j
    worksheet.write('K%s'%i, "=SUM(%s)"%str[:-1], row_format)
    
    str = ""
    for j in epic_rows:
        str = str + "L%s,"%j
    worksheet.write('L%s'%i, "=SUM(%s)"%str[:-1], row_format)
    
    #Grand Total ManDays row
    i += 1
    worksheet.write('A%s'%i, project['key'], row_format)
    worksheet.write('B%s'%i, project['name'], row_format)
    worksheet.write('C%s'%i, 'Grand Total ManDays ', row_format)
    worksheet.write('J%s'%i, "=ROUND(J%s/%s, 1)"%(i-1, hours_per_day), row_format)
    worksheet.write('K%s'%i, "=ROUND(K%s/%s, 1)"%(i-1, hours_per_day), row_format)
    worksheet.write('L%s'%i, "=ROUND(L%s/%s, 1)"%(i-1, hours_per_day), row_format)
    return i

def add_dummy_epic(key):
    epic_details = {}
    epic_details['key'] = key
    epic_details['summary'] = 'Issues without epics (No Epic)'
    epic_details['type'] = 'Epic'
    epic_details['status'] = 'Open'
    epic_details['assignee'] = None
    epic_details['reporter'] = None
    epic_details['original_estimate'] = 0
    epic_details['time_spent'] = 0
    epic_details['remaining_estimate'] = 0
    return epic_details

def get_issue_without_epics(jira):
    data = jira.search_issues("project = %s AND issuetype in (Bug, Story, Task) AND resolution = Unresolved AND 'Epic Link' is EMPTY ORDER BY key %s" %(project['key'], sorting))                          
    issue_list = []
    for d in data:
        issue_details = {}
        issue_details['key'] = d.key
        issue_details['summary'] = d.fields.summary
        issue_details['type'] = d.fields.issuetype.name
        issue_details['status'] = d.fields.status.name
        issue_details['assignee'] = d.fields.assignee.name if d.fields.assignee else None
        issue_details['reporter'] = d.fields.reporter.name if d.fields.reporter else None
        issue_details['original_estimate'] = d.fields.timeoriginalestimate
        issue_details['time_spent'] = d.fields.timespent
        issue_details['remaining_estimate'] = d.fields.timeestimate
        issue_list.append(issue_details)
    return issue_list

def get_epics_issues(jira):
    epic_issues = {}
    for epic in epics:
        epic_key = epic['key']
        data = jira.search_issues("project = %s AND 'Epic Link' = %s AND resolution = Unresolved ORDER BY key %s" %(project['key'], epic_key, sorting))
        issue_list = []
        for d in data:
            issue_details = {}
            issue_details['key'] = d.key
            issue_details['summary'] = d.fields.summary
            issue_details['type'] = d.fields.issuetype.name
            issue_details['status'] = d.fields.status.name
            issue_details['assignee'] = d.fields.assignee.name if d.fields.assignee else None
            issue_details['reporter'] = d.fields.reporter.name if d.fields.reporter else None
            issue_details['original_estimate'] = d.fields.timeoriginalestimate
            issue_details['time_spent'] = d.fields.timespent
            issue_details['remaining_estimate'] = d.fields.timeestimate
            issue_list.append(issue_details)
        epic_issues['%s'%epic_key] = issue_list
    # for loop epic in epics 
    #print(epic_issues)
    
    issue_list = get_issue_without_epics(jira)
    if len(issue_list) > 0:
        epic_issues['NoEpicIssues'] = issue_list
        epics.append(add_dummy_epic('NoEpicIssues')) # add dummy epic for issues without epic

    write_to_excel(project, epics, epic_issues)

def main(jira): 
    project['key'] = args.project_key
    project['name']= jira.project(project['key']).name

    data = jira.search_issues("project = %s AND issuetype = Epic AND resolution = Unresolved ORDER BY key %s" %(project['key'], sorting))
    for d in data:
        epic_details = {}
        epic_details['key'] = d.key
        #epic_details['name'] = d.fields.cutsomfield_10104
        epic_details['summary'] = d.fields.summary
        epic_details['type'] = d.fields.issuetype.name
        epic_details['status'] = d.fields.status.name
        epic_details['assignee'] = d.fields.assignee.name if d.fields.assignee else None
        epic_details['reporter'] = d.fields.reporter.name if d.fields.reporter else None
        epic_details['original_estimate'] = d.fields.timeoriginalestimate
        epic_details['time_spent'] = d.fields.timespent
        epic_details['remaining_estimate'] = d.fields.timeestimate
        epics.append(epic_details)
    #print(epics)
    
    get_epics_issues(jira)


def login_to_jira(url, user, password):
    try:
        jira = JIRA(options = {'server': JIRA_URL, 'verify': False}, basic_auth=(user, password))
        return jira
    except:
        print("login to Jira failed!! please check username/password")
        exit(1)


if "__main__" == __name__:
    
    def list_of_strings(arg):
        return arg.split(',')
    parser = argparse.ArgumentParser(prog='python roadmap.py <project_key>',
                                     description='It create roadmap view in excel sheet'
                                     )
    
    #parser.add_argument('username', help='user name to be used to log in into git and Jira')
    #parser.add_argument('password', help='password associated with user to login into git and Jira')
    parser.add_argument('project_key', help='project whose roadmap is to be created')
    parser.add_argument('-p', '--path', help='path, where roadmap shall be saved', default='.')
 
    args = parser.parse_args()
    user = getpass.getuser()
    print ('User Name: %s' %user )
    password = getpass.getpass(prompt='Password :')
    
    jira =  login_to_jira(JIRA_URL, user, password)

    if not os.path.exists(args.path):
        os.makedirs(args.path)

    main(jira)
   
