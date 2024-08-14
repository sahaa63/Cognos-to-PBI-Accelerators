import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import regex as re
import openai
import pandas as pd

# def convert_to_dax_expression(expression):
#     response = openai.Completion.create(
#         model="gpt-3.5-turbo",
#         prompt=f"Convert the following expression to a DAX expression: {expression}",
#         max_tokens=100
#     )
#     dax_expression = response.choices[0].text.strip()
#     return dax_expression

# def process_dataframe(df):
#     # Create a new column for the PowerBI formula
#     df['powerbi formula'] = None
    
#     # Iterate over the dataframe rows
#     for index, row in df.iterrows():
#         if row['Rollup Aggregate'].lower() == 'total':
#             # Get the expression
#             expression = row['Expression']
            
#             # Convert the expression to DAX
#             dax_expression = convert_to_dax_expression(expression)
            
#             # Save the DAX expression in the new column
#             df.at[index, 'powerbi formula'] = dax_expression
    
#     return df

def parse_model_path(model_path):
    """
    Function to parse model path and extract package name and model name separately.
    """
    package_start_index = model_path.find("@name='") + len("@name='")
    package_end_index = model_path.find("'", package_start_index)
    package_name = model_path[package_start_index:package_end_index]
    
    model_start_index = model_path.find("@name='", package_end_index) + len("@name='")
    model_end_index = model_path.find("'", model_start_index)
    model_name = model_path[model_start_index:model_end_index]
    
    return package_name, model_name

def parse_cognos_report(xml_content):
    root = ET.fromstring(xml_content)
    namespace = {'c': 'http://developer.cognos.com/schemas/report/16.2/'}
    
    report_name = root.find('c:reportName', namespace).text
    pages = root.findall('.//c:reportPages/c:page', namespace)
    num_pages = len(pages)
    
    model_path_element = root.find('c:modelPath', namespace)
    model_path = model_path_element.text if model_path_element is not None else 'No model path found'
    
    package_name, model_name = parse_model_path(model_path)
    
    queries = root.findall('.//c:queries/c:query', namespace)
    datasource_details = []
    
    for query in queries:
        query_name = query.get('name')
        columns = []
        detail_filters = []
        data_items = query.findall('.//c:selection/c:dataItem', namespace)
        
        for data_item in data_items:
            column_name = data_item.get('name')
            expression = data_item.find('c:expression', namespace).text
            rollup_aggregate = data_item.get('rollupAggregate', 'none')
            aggregate = data_item.get('aggregate', 'none')
            item_details = {
                'name': column_name,
                'expression': expression,
                'rollupAggregate': rollup_aggregate,
                'aggregate': aggregate
            }
            columns.append(item_details)
        
        detail_filters_nodes = query.findall('.//c:detailFilters/c:detailFilter', namespace)
        for filter_node in detail_filters_nodes:
            filter_expression = filter_node.find('c:filterExpression', namespace).text
            detail_filters.append({'expression': filter_expression})
        
        datasource_details.append({
            'query_name': query_name,
            'columns': columns,
            'detail_filters': detail_filters
        })
    
    page_details = []
    
    for page in pages:
        page_name = page.get('name')
        page_content = []
        
        lists = page.findall('.//c:list', namespace)
        for lst in lists:
            list_name = lst.get('name')
            ref_query = lst.get('refQuery')
            columns = []
            data_items = lst.findall('.//c:listColumnBody/c:contents/c:textItem/c:dataSource/c:dataItemValue', namespace)
            for data_item in data_items:
                columns.append(data_item.get('refDataItem'))
            page_content.append({
                'list_name': list_name,
                'ref_query': ref_query,
                'columns': columns
            })
        
        page_details.append({
            'page_name': page_name,
            'content': page_content
        })
    
    return report_name, num_pages, package_name, model_name, datasource_details, page_details

st.title("Cognos Report Metadata Extractor", help="This accelerator extracts the metadata from Cognos reports such as datasources used in report, columns used in report pages & much more ")

uploaded_files = st.file_uploader("Upload Cognos Report(s) in txt format)", type="txt", accept_multiple_files=True)

if uploaded_files:
    tabs = st.tabs([f"Report {i+1}" for i in range(len(uploaded_files))])
    
    final_columns_df = pd.DataFrame()

    for tab, uploaded_file in zip(tabs, uploaded_files):
        with tab:
            xml_content = uploaded_file.read().decode("utf-8")
            
            report_name, num_pages, package_name, model_name, datasource_details, page_details = parse_cognos_report(xml_content)
            
            #st.info("Report Details")
            st.write(f"**Report Name:** {report_name}")
            st.write(f"**Number of Pages:** {num_pages}")
            st.write(f"**Package Name:** {package_name}")
            st.write(f"**Model Name:** {model_name}")
            
            #st.info("Datasources used in the Report")
            for datasource in datasource_details:
                #st.code(f"Query Name: {datasource['query_name']}")
                
                if datasource['columns']:
                    columns_df = pd.DataFrame(datasource['columns'])
                    #st.dataframe(columns_df)
                
                if datasource['detail_filters']:
                    #st.write("**Detail Filters:**")
                    filters_df = pd.DataFrame(datasource['detail_filters'])
                    #st.dataframe(filters_df)
            
            # st.info("Pages present inside Report")
            for page in page_details:
                #st.subheader(f"Report Page: {page['page_name']}")
                
                for content in page['content']:
                    # st.write(f"**Referenced Query:** {content['ref_query']}")
                    if content['columns']:
                        columns_df = pd.DataFrame(content['columns'], columns=['Column Name'])
                        #st.dataframe(columns_df)
    
            # Collecting data for the final dataframe
            rows = []
            for datasource in datasource_details:
                query_name = datasource['query_name']
                for column in datasource['columns']:
                    used_in_page = "No"
                    page_name = "N/A"
                    for page in page_details:
                        for content in page['content']:
                            if content['ref_query'] == query_name and column['name'] in content['columns']:
                                used_in_page = "Yes"
                                page_name = page['page_name']
                                break
                    rows.append({
                        'Report Name': report_name,
                        'Query Name': query_name,
                        'Report Page Name': page_name,
                        'Column Name': column['name'],
                        'Expression': column['expression'],
                        'Rollup Aggregate': column['rollupAggregate'],
                        'Aggregate': column['aggregate'],
                        'Used in Report Page': used_in_page
                    })
            final_columns_df = pd.concat([final_columns_df, pd.DataFrame(rows)], ignore_index=True)
        # Define regex pattern
    pattern = r'\[([^\]]+)\]\.\[([^\]]+)\]\.\[([^\]]+)\]'

    # Function to extract source
    def extract_source(text):
        match = re.search(pattern, text)
        if match:
            return f"{match.group(1)}.{match.group(2)}"
        else:
            return ''

    # Apply function to create new column
    final_columns_df['Source'] = final_columns_df['Expression'].apply(extract_source)

    # Rearranging columns so that 'Report Name' is first
    final_columns_df = final_columns_df[[
        'Report Name', 'Report Page Name', 'Query Name', 'Column Name', 
        'Expression', 'Rollup Aggregate', 'Aggregate', 'Used in Report Page','Source'
    ]]

    # Process the dataframe
    #final_columns_df = process_dataframe(final_columns_df)

    st.info("Report Analysis")
    st.dataframe(final_columns_df)
    


    # Add download button for the final dataframe
    csv = final_columns_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='final_report_data.csv',
        mime='text/csv',
    )
else:
    print("Please upload one or more Cognos reports in txt format.")
