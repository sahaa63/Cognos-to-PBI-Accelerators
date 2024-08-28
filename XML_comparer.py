import streamlit as st
import pandas as pd
import re
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances

## It takes bsp excels and give groups on basis of names and cols,filters

# Function to extract the package name from the string
def extract_package_name(package_str):
    match = re.search(r"@name='(.*?)'", package_str)
    if match:
        return match.group(1)
    return package_str

# Function to process the CSV file and bring granularity to report/search paths
def process_csv(file):
    df = pd.read_csv(file)
    
    # Apply the extraction function to the Package column
    df['Package'] = df['Package'].apply(extract_package_name)
    
    # Filtering DataFrame based on DataItemType for dataItem and detailFilter
    data_items_df = df[df['DataItemType'] == 'dataItem']
    detail_filters_df = df[df['DataItemType'] == 'detailFilter']

    # Grouping by 'SearchPath' and concatenating the 'DataItemDetails' with duplicates removed
    grouped_data_items = data_items_df.groupby(['SearchPath', 'ReportName']).agg({
        'DataItemDetails': lambda x: ', '.join(sorted(set(str(item) for item in x if pd.notna(item)))),
        'Package': 'first'
    }).reset_index()

    # Renaming the columns
    grouped_data_items.rename(columns={'DataItemDetails': 'columnnames'}, inplace=True)

    # Grouping by 'SearchPath' and concatenating 'DataItemDetails' for detailFilter with duplicates removed
    grouped_detail_filters = detail_filters_df.groupby('SearchPath').agg({
        'DataItemDetails': lambda x: ', '.join(sorted(set(str(item) for item in x if pd.notna(item))))
    }).reset_index()

    # Renaming the column
    grouped_detail_filters.rename(columns={'DataItemDetails': 'Datafilters'}, inplace=True)

    # Merging the two grouped DataFrames on 'SearchPath'
    # Merging the two grouped DataFrames on 'SearchPath'
    final_df = pd.merge(grouped_data_items, grouped_detail_filters, on='SearchPath', how='left')

    # Reordering columns to have 'Package' as the first column
    final_df = final_df[['Package', 'SearchPath', 'ReportName', 'columnnames', 'Datafilters']]

    return final_df

# Function to create new columns with group IDs for similar report names
def assign_group_ids(df):
    # Ensure all entries in 'ReportName' are strings and fill missing values
    df['ReportName'] = df['ReportName'].astype(str).fillna('')

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['ReportName'])
    distance_matrix = pairwise_distances(X, metric='cosine')
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.5, affinity='precomputed', linkage='average')
    clustering.fit(distance_matrix)
    df['reportGroupId'] = clustering.labels_

    return df

# Function to calculate match percentages and differences
def calculate_matches_and_differences(group):
    # Initialize the lists to store results
    column_matches = []
    filter_matches = []
    column_differences = []
    filter_differences = []

    for i, row in group.iterrows():
        # Convert the columns and filters to strings and split into sets for comparison
        columns_set = set(str(row['columnnames']).split(', ')) if pd.notna(row['columnnames']) else set()
        filters_set = set(str(row['Datafilters']).split(', ')) if pd.notna(row['Datafilters']) else set()
        
        # Initialize max matches to 0
        max_column_match = 0
        max_filter_match = 0
        
        # Compare with all other rows in the group
        for j, compare_row in group.iterrows():
            if i != j:
                compare_columns_set = set(str(compare_row['columnnames']).split(', ')) if pd.notna(compare_row['columnnames']) else set()
                compare_filters_set = set(str(compare_row['Datafilters']).split(', ')) if pd.notna(compare_row['Datafilters']) else set()
                
                # Calculate intersection (matches) and differences
                column_intersection = columns_set.intersection(compare_columns_set)
                filter_intersection = filters_set.intersection(compare_filters_set)
                
                column_difference = columns_set.symmetric_difference(compare_columns_set)
                filter_difference = filters_set.symmetric_difference(compare_filters_set)
                
                # Calculate the match percentages
                column_match_percentage = len(column_intersection) / max(len(columns_set), len(compare_columns_set)) * 100
                filter_match_percentage = len(filter_intersection) / max(len(filters_set), len(compare_filters_set)) * 100
                
                # Update max matches if current comparison is higher
                max_column_match = max(max_column_match, column_match_percentage)
                max_filter_match = max(max_filter_match, filter_match_percentage)
                
                # Store differences (we assume we're interested in the first comparison)
                if max_column_match == column_match_percentage:
                    column_diff = column_difference
                if max_filter_match == filter_match_percentage:
                    filter_diff = filter_difference
        
        # Append the results for the current row
        column_matches.append(max_column_match)
        filter_matches.append(max_filter_match)
        column_differences.append(", ".join(column_diff))
        filter_differences.append(", ".join(filter_diff))
    
    # Add results as new columns in the group
    group['% of column matches'] = column_matches
    group['% of filter matches'] = filter_matches
    group['difference in columns'] = column_differences
    group['difference in filters'] = filter_differences
    
    return group

# Function to assign xmlcompare_groupid within reportGroupId based on similarities in columnnames and Datafilters
def assign_xmlcompare_groupid(df):
    def calculate_similarity(group):
        if len(group) < 2:
            return pd.Series([0] * len(group), index=group.index)
        
        vectorizer = TfidfVectorizer()
        combined_features = group['columnnames'].fillna('') + " " + group['Datafilters'].fillna('')
        
        X = vectorizer.fit_transform(combined_features)
        distance_matrix = pairwise_distances(X, metric='cosine')
        
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.3, affinity='precomputed', linkage='average')
        clustering.fit(distance_matrix)
        
        return pd.Series(clustering.labels_, index=group.index)

    # Apply the calculation and reindex the result to ensure alignment with the original dataframe
    df['xmlcompare_groupid'] = df.groupby('reportGroupId', group_keys=False).apply(calculate_similarity)

    # Calculate match percentages and differences within each xmlcompare_groupid
    df = df.groupby('xmlcompare_groupid', group_keys=False).apply(calculate_matches_and_differences)
    
    return df

# Streamlit app
st.title('Granularity Processor for Report/Search Paths (Excel Output)')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    processed_df = process_csv(uploaded_file)
    
    # Assign group IDs based on similar report names
    processed_df = assign_group_ids(processed_df)

    # Assign xmlcompare_groupid within reportGroupId
    processed_df = assign_xmlcompare_groupid(processed_df)
    
    st.write("Processed Data:")
    st.dataframe(processed_df)
    
    # Prepare the Excel file for download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        processed_df.to_excel(writer, index=False, sheet_name='Processed Data')
    processed_excel = output.getvalue()
    
    st.download_button(
        label="Download Processed Excel",
        data=processed_excel,
        file_name='processed_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
