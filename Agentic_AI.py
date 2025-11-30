import arxiv
import pandas as pd
import os

# 1. Fetch the 5 most recent papers in AI
client = arxiv.Client()
results = client.results(arxiv.Search(query="AI", max_results=5, sort_by = arxiv.SortCriterion.SubmittedDate))
print("--- ArXiv Watchdog Papers Fetched ---")

#%%

results_dict = dict({"Title":[], "Abstract":[], "Summary":[]})
for paper in results:
    # 2. Extract Title and Summary
    results_dict['Title'].append(paper.title)
    results_dict['Abstract'].append(paper.summary)
    print(f"TITLE: {paper.title}\n---\n{paper.summary}") 
    
    
#%%

import google.genai as genai
client = genai.Client()

# Your excellent instruction:
system_instruction = "You are a technical researcher, read below given papers to create a summary for a data scientist, output should be a one sentence summary of the paper"

# Inside the loop:
for abstract in results_dict['Abstract']:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[abstract],                                 # The data to be analyzed (as a list)
        config={'system_instruction': system_instruction}    # Your instruction goes into config
    )
    
    results_dict['Summary'].append(response.text)

#%%    
results_df = pd.DataFrame(results_dict)

#%%

import smtplib

# 1. Establish the connection
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)

# 2. Start the TLS encryption
smtp_server.starttls()

sender_mail = "solanki2899@gmail.com"
password = os.environ['EMAIL_PASSWORD']

smtp_server.login(sender_mail, password)

from email.message import EmailMessage
msg = EmailMessage()

msg['From'] = sender_mail
msg['To'] = 'pkhunterr1234@gmail.com'
msg['Subject'] = 'ArXiv Watchdog Daily Digest 🐕'

# 1. Build the email body string:
email_body = ""
for index in range(len(results_df)):
    email_body += f"**{results_df['Title'][index]}**\nRelevance: {results_df['Summary'][index]} \n---\n\n"

# 2. Add the body content to the message object:
msg.set_content(email_body)

# 3. Send the email and close the connection:
smtp_server.sendmail(sender_mail, msg['To'], msg.as_string())
smtp_server.quit()




    


