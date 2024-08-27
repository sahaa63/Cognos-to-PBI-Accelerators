import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Function to extract the package name from the string
def extract_package_name(package_str):
    match = re.search(r"@name='(.*?)'", package_str)
    if match:
        return match.group(1)
    return package_str

# Function to process the CSV file and generate the required DataFrame
def process_csv(file):
    df = pd.read_csv(file)
    
    # Apply the extraction function to the Package column
    df['Package'] = df['Package'].apply(extract_package_name)
    
    # Filtering DataFrame based on DataItemType for dataItem and detailFilter
    data_items_df = df[df['DataItemType'] == 'dataItem']
    detail_filters_df = df[df['DataItemType'] == 'detailFilter']

    # Grouping by 'SearchPath' and concatenating the 'DataItemDetails' with duplicates removed
    grouped_data_items = data_items_df.groupby(['SearchPath', 'ReportName']).agg({
        'DataItemDetails': lambda x: ', '.join(sorted(set(x))),
        'Package': 'first'
    }).reset_index()

    # Renaming the columns
    grouped_data_items.rename(columns={'DataItemDetails': 'columnnames'}, inplace=True)

    # Grouping by 'SearchPath' and concatenating 'DataItemDetails' for detailFilter with duplicates removed
    grouped_detail_filters = detail_filters_df.groupby('SearchPath').agg({
        'DataItemDetails': lambda x: ', '.join(sorted(set(x)))
    }).reset_index()

    # Renaming the column
    grouped_detail_filters.rename(columns={'DataItemDetails': 'Datafilters'}, inplace=True)

    # Merging the two grouped DataFrames on 'SearchPath'
    final_df = pd.merge(grouped_data_items, grouped_detail_filters, on='SearchPath', how='left')

    # Reordering columns to have 'Package' as the first column
    final_df = final_df[['Package', 'SearchPath', 'ReportName', 'columnnames', 'Datafilters']]

    return final_df

# Streamlit app
st.title('CSV Processor for DataItemDetails')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    processed_df = process_csv(uploaded_file)
    
    st.write("Processed Data:")
    st.dataframe(processed_df)
    
    # Prepare the Excel file for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        processed_df.to_excel(writer, index=False, sheet_name='Processed Data')
        writer.close()  # Ensuring writer is properly closed
        processed_excel = output.getvalue()
    
    st.download_button(
        label="Download Processed Excel",
        data=processed_excel,
        file_name='processed_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
