import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
from io import StringIO

def parse_xml(xml_content):
    root = ET.fromstring(xml_content)
    
    # Extract report name
    report_name = root.find('name').text

    # Extract package name
    search_path = root.find('searchPath').text
    package_name = search_path.split("/")[2].split("[@name='")[1][:-2]

    # Map of query references to page names
    page_query_map = {}
    
    # Extract all pages and their associated queries
    page_names = []
    for page in root.findall('.//page'):
        page_name = page.get('name')
        page_names.append(page_name)
        
        # Explore all possible elements that might link a page to a query
        for element in page.iter():
            ref_query = element.get('refQuery')
            if ref_query:
                page_query_map[ref_query] = page_name

    # Extract all queries and associate them with the report
    data = []
    distinct_data_items = set()
    
    # Iterate over all queries in the report
    for query in root.findall('.//query'):
        query_name = query.get('name')
        
        # Determine the page name if it exists
        page_name = page_query_map.get(query_name, "Standalone Query")
        
        # For each query, get the associated data items
        for item in query.findall('.//dataItem'):
            query_item_name = item.get('name')
            query_expression = item.find('expression').text
            
            # Collect distinct data items
            distinct_data_items.add(query_item_name)
            
            # Append the data
            data.append({
                'Report Name': report_name,
                'Package Name': package_name,
                'Page Name': page_name,
                'Query Name': query_name,
                'Query Item Name': query_item_name,
                'Query Expression': query_expression
            })
    
    # Determine the level of effort and effort in hours
    num_pages = len(page_names)
    num_dataitems = len(distinct_data_items)
    
    if num_pages == 1 and num_dataitems < 25:
        level_of_effort = "Low"
        effort_in_hours = 1
    elif num_pages == 2 and num_dataitems < 40:
        level_of_effort = "Medium"
        effort_in_hours = 3
    elif num_pages > 2 or num_dataitems >= 40:
        level_of_effort = "High"
        effort_in_hours = 8
    else:
        level_of_effort = "Unknown"
        effort_in_hours = 0  # Default value if conditions don't match
    
    report_summary = {
        'Report Name': report_name,
        'Package Name': package_name,
        'Total Pages': num_pages,
        'Distinct Data Items': num_dataitems,
        'Level of Effort': level_of_effort,
        'Effort in Hours': effort_in_hours
    }
    
    return pd.DataFrame(data), report_summary

st.title("Cognos XML to CSV Extractor")

uploaded_files = st.file_uploader("Upload Cognos XML Files", type="xml", accept_multiple_files=True)

if uploaded_files:
    combined_df = pd.DataFrame()
    summary_list = []

    for uploaded_file in uploaded_files:
        xml_content = uploaded_file.read().decode("utf-8")
        
        # Parse XML and get DataFrame and summary data
        df, report_summary = parse_xml(xml_content)
        
        # Combine all DataFrames
        combined_df = pd.concat([combined_df, df], ignore_index=True)
        
        # Collect summary data
        summary_list.append(report_summary)
    
    # Convert summary list to DataFrame
    summary_df = pd.DataFrame(summary_list)
    
    # Display the combined DataFrame
    st.subheader("Extracted Data")
    st.write(combined_df)
    
    # Provide a CSV download option for extracted data
    csv_buffer = StringIO()
    combined_df.to_csv(csv_buffer, index=False)
    
    st.download_button(
        label="Download Extracted Data CSV",
        data=csv_buffer.getvalue(),
        file_name="cognos_reports_extraction.csv",
        mime="text/csv"
    )
    
    # Display the summary DataFrame
    st.subheader("Report Summary")
    st.write(summary_df)
    
    # Provide a CSV download option for the summary data
    summary_csv_buffer = StringIO()
    summary_df.to_csv(summary_csv_buffer, index=False)
    
    st.download_button(
        label="Download Summary CSV",
        data=summary_csv_buffer.getvalue(),
        file_name="cognos_reports_summary.csv",
        mime="text/csv"
    )
