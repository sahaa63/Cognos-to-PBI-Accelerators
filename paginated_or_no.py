#Expects Input in following csv Name|Type|Location|JobName|ReportName|Recipient|SearchPath
import streamlit as st
import pandas as pd
import re

# Streamlit app title
st.title("JobName and ReportName Extractor with Granular Report")

# File uploader for CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Add JobName and ReportName columns
    df['JobName'] = df['Location'].apply(lambda x: x.split('>>')[-1].strip() if isinstance(x, str) and '>>' in x else '')
    df['ReportName'] = df.apply(lambda row: row['Name'] if row['Type'] == 'Schedule' 
                                else row['Name'].split('-')[-1] if row['Type'] == 'JobStepDefinition' 
                                else '', axis=1)
    
    # Trim spaces from ReportName column
    df['ReportName'] = df['ReportName'].str.strip()

    # Ensure all recipients are strings to avoid TypeError during concatenation
    df['Recipient'] = df['Recipient'].astype(str)

    # Step 1: Create the 'Report Name' column with distinct values from 'ReportName'
    distinct_reports = df['ReportName'].unique()

    # Step 2: Aggregate Recipients for each report and Type
    grouped = df.groupby(['ReportName', 'Type'])['Recipient'].apply(lambda x: ','.join(x.unique())).reset_index()

    # Step 3: Pivot the grouped DataFrame to have separate columns for each Type
    pivot = grouped.pivot(index='ReportName', columns='Type', values='Recipient').reset_index()

    # Step 4: Create the 'JOBs' column
    job_map = df[df['JobName'] != ''].groupby('ReportName')['JobName'].apply(lambda x: ','.join(x.unique())).to_dict()
    pivot['JOBs'] = pivot['ReportName'].map(job_map)

    # Step 5: Populate 'JobDefinition Recipients2' using the job names
    pivot['JobDefinition Recipients2'] = pivot['JOBs'].apply(lambda x: ','.join(df[df['Name'].isin(x.split(','))]['Recipient'].unique()) if isinstance(x, str) else '')

    # Step 6: Add 'SearchPath' (assuming it is the first non-null SearchPath for each ReportName)
    search_path_map = df.groupby('ReportName')['SearchPath'].first().to_dict()
    pivot['SearchPath'] = pivot['ReportName'].map(search_path_map)

    # Rename the columns to match the desired output
    pivot = pivot.rename(columns={
        'ReportName': 'Report Name',
        'Schedule': 'Schedule Recipients',
        'JobStepDefinition': 'JobStepDefinition Recipients',
        'JobDefinition': 'JobDefinition Recipients'
    })

    # Remove rows where 'Report Name' is null or empty
    pivot = pivot[pivot['Report Name'].notna() & (pivot['Report Name'] != '')]

    # Add a new column 'all recipients' by concatenating the three recipient columns
    pivot['all recipients'] = pivot['JobStepDefinition Recipients'].fillna('') + ',' + \
                              pivot['Schedule Recipients'].fillna('') + ',' + \
                              pivot['JobDefinition Recipients2'].fillna('')

    # Remove any leading or trailing commas that might occur from empty values
    pivot['all recipients'] = pivot['all recipients'].str.strip(',')

    # Add the 'paginated flag' column based on email domain logic
    def check_paginated_flag(recipients):
        # Regex to extract all email domains
        email_domains = re.findall(r'@([\w.-]+)', recipients)
        # Check if any domain is not 'goodyear.com'
        for domain in email_domains:
            if domain.lower() != 'goodyear.com':
                return 'yes'
        return 'no'

    pivot['paginated flag'] = pivot['all recipients'].apply(check_paginated_flag)

    # Display the final granular DataFrame
    st.write("Granular Report DataFrame:")
    

    #df cleaning
    pivot = pivot[~pivot['SearchPath'].str.contains('CAMID', na=True) & pivot['SearchPath'].notna()]

    st.dataframe(pivot)

    # Option to download the granular DataFrame as a CSV
    st.download_button(
        label="Download Granular Report Data",
        data=pivot.to_csv(index=False).encode('utf-8'),
        file_name='granular_report_data.csv',
        mime='text/csv'
    )
else:
    st.write("Please upload a CSV file.")
