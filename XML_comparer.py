# Report XML Comparer
# expects input csvs of reports 

import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict

# Function to extract relevant data from the report
def extract_report_data(report):
    tree = ET.parse(report)
    root = tree.getroot()

    data_items = set()
    filters = set()
    metrics = set()

    # Extract data items and filters
    for query in root.findall('.//query'):
        for data_item in query.findall('.//dataItem'):
            data_items.add(data_item.get('name'))
        
        for filter in query.findall('.//detailFilter'):
            filter_expression = filter.find('filterExpression')
            if filter_expression is not None:
                filters.add(filter_expression.text)
    
    # Extract metrics (assuming metrics are stored similarly to data items, adjust path if necessary)
    for metric in root.findall('.//metric'):
        metrics.add(metric.get('name'))

    return data_items, filters, metrics

# Function to calculate overlap percentage
def calculate_overlap(set1, set2):
    if not set1 or not set2:
        return 0
    return len(set1 & set2) / len(set1 | set2) * 100

# Function to compute the Report Correlation Index Score
def compute_correlation_index(data1, data2):
    db_attr_overlap = calculate_overlap(data1[0], data2[0])
    filter_overlap = calculate_overlap(data1[1], data2[1])
    metric_overlap = calculate_overlap(data1[2], data2[2])
    
    correlation_index = (0.5 * db_attr_overlap) + (0.3 * filter_overlap) + (0.2 * metric_overlap)
    return db_attr_overlap, filter_overlap, metric_overlap, correlation_index

# Streamlit app
st.title("Report Rationalization")

uploaded_files = st.file_uploader("Upload Report Files", accept_multiple_files=True, type="txt")

if uploaded_files:
    report_data = []
    
    # Extract data from uploaded reports
    for report in uploaded_files:
        data_items, filters, metrics = extract_report_data(report)
        report_data.append((report.name, (data_items, filters, metrics)))
        st.write(f"Extracted from {report.name}:")
        st.write(f"Data Items: {data_items}")
        st.write(f"Filters: {filters}")
        st.write(f"Metrics: {metrics}")

    # Prepare dataframe to store the rationalization scores
    df_scores = pd.DataFrame(columns=[
        'Report 1', 'Report 2', 'Database Attribute Overlap (%)', 
        'Filter Overlap (%)', 'Metrics Overlap (%)', 
        'Correlation Index Score (%)', 'Total Score'
    ])

    # Calculate and display the rationalization scores
    for i in range(len(report_data)):
        for j in range(i + 1, len(report_data)):
            db_attr_overlap, filter_overlap, metric_overlap, score = compute_correlation_index(report_data[i][1], report_data[j][1])
            total_score = db_attr_overlap + filter_overlap + metric_overlap
            df_scores = df_scores.append({
                'Report 1': report_data[i][0],
                'Report 2': report_data[j][0],
                'Database Attribute Overlap (%)': db_attr_overlap,
                'Filter Overlap (%)': filter_overlap,
                'Metrics Overlap (%)': metric_overlap,
                'Correlation Index Score (%)': score,
                'Total Score': total_score
            }, ignore_index=True)
    
    # Display the dataframe
    st.write("Rationalization Scores:")
    st.dataframe(df_scores)
