# mailtester
This script validates possible email addresses of leads outputs a CSV file that you can import in Streak for GMAIL to create lead generation boxes automatically

# Usage
python mailtester.py streak_stage_name

# Input format
A csv file called "inputlist.csv" should be in the same folder have the right format

# Output format
valid.csv: uploadable directly to streak

failed.csv: Contains the error message of failure (if something else that email not valid)

Streak CRM: You can import valid.csv directly in Streak, this will create all the lead generation boxes you need with the right name, company and email address