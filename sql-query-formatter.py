import streamlit as st
import re

st.set_page_config(layout="wide")

def process_sql_query(query):
    # Regular expression to match AS clauses with quoted identifiers
    pattern = r'(AS\s+)(["\'])(.+?)\2'
    
    def replace_underscore(match):
        as_keyword = match.group(1)
        quote = match.group(2)
        alias = match.group(3)
        # Replace underscores with spaces in the alias
        alias = alias.replace('_', ' ')
        return f"{as_keyword}{quote}{alias}{quote}"
    
    # Apply the transformation
    processed_query = re.sub(pattern, replace_underscore, query, flags=re.IGNORECASE)
    return processed_query

# Streamlit app
st.title("Cognos Biz Layer to PBI Biz Layer Query")

# Instructions
st.markdown("""
### Instructions:
1. Enter your business layer SQL query in the text area.
2. Click the "Format Query" button.
3. A side-by-side comparison of the original and formatted queries will be shown at the bottom.
""")

# Input text area for SQL query
input_query = st.text_area("Enter your SQL query:", height=200)

if st.button("Format Query"):
    if input_query:
        # Process the query
        formatted_query = process_sql_query(input_query)
        
        # Display the result
        #st.subheader("Formatted Query:")
        #st.code(formatted_query, language="sql")
        
        # Display side-by-side comparison
        st.subheader("Side-by-Side Comparison:")
        col1, col2 = st.columns(2)
        with col1:
            st.text("Original Query:")
            st.code(input_query, language="sql")
        with col2:
            st.text("Formatted Query:")
            st.code(formatted_query, language="sql")
    else:
        st.warning("Please enter a SQL query.")
