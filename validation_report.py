import streamlit as st
import pandas as pd
import io

def generate_validation_report(cognos_df, pbi_df):
    # Identify dimensions and measures
    dims = [col for col in cognos_df.columns if col in pbi_df.columns and 
            (cognos_df[col].dtype == 'object' or 'id' in col.lower() or 'key' in col.lower())]
    cognos_measures = [col for col in cognos_df.columns if col not in dims]
    pbi_measures = [col for col in pbi_df.columns if col not in dims]
    all_measures = list(set(cognos_measures + pbi_measures))

    # Create a unique key by concatenating all dimensions
    cognos_df['unique_key'] = cognos_df[dims].astype(str).agg('-'.join, axis=1)
    pbi_df['unique_key'] = pbi_df[dims].astype(str).agg('-'.join, axis=1)

    # Create the validation report dataframe
    validation_report = pd.DataFrame({'unique_key': list(set(cognos_df['unique_key']) | set(pbi_df['unique_key']))})

    # Add dimensions
    for dim in dims:
        validation_report[dim] = validation_report['unique_key'].map(dict(zip(cognos_df['unique_key'], cognos_df[dim])))
        validation_report[dim].fillna(validation_report['unique_key'].map(dict(zip(pbi_df['unique_key'], pbi_df[dim]))), inplace=True)

    # Determine presence in sheets
    validation_report['presence'] = validation_report['unique_key'].apply(
        lambda key: 'Present in Both' if key in cognos_df['unique_key'].values and key in pbi_df['unique_key'].values
        else ('Present in Cognos' if key in cognos_df['unique_key'].values
              else 'Present in PBI')
    )

    # Add measures
    for measure in all_measures:
        if measure in cognos_df.columns:
            validation_report[f'{measure}_Cognos'] = validation_report['unique_key'].map(dict(zip(cognos_df['unique_key'], cognos_df[measure])))
        if measure in pbi_df.columns:
            validation_report[f'{measure}_PBI'] = validation_report['unique_key'].map(dict(zip(pbi_df['unique_key'], pbi_df[measure])))

    # Reorder columns
    column_order = dims + ['unique_key', 'presence'] + \
                   [f'{m}_Cognos' for m in all_measures if f'{m}_Cognos' in validation_report.columns] + \
                   [f'{m}_PBI' for m in all_measures if f'{m}_PBI' in validation_report.columns]
    validation_report = validation_report[column_order]

    return validation_report

def main():
    st.title("Validation Report Generator")

    uploaded_file = st.file_uploader("Upload Excel file", type="xlsx")

    if uploaded_file is not None:
        try:
            xls = pd.ExcelFile(uploaded_file)
            cognos_df = pd.read_excel(xls, 'Cognos')
            pbi_df = pd.read_excel(xls, 'PBI')

            validation_report = generate_validation_report(cognos_df, pbi_df)

            st.subheader("Validation Report Preview")
            st.dataframe(validation_report)

            # Generate Excel file for download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                cognos_df.to_excel(writer, sheet_name='Cognos', index=False)
                pbi_df.to_excel(writer, sheet_name='PBI', index=False)
                validation_report.to_excel(writer, sheet_name='Validation_Report', index=False)

            output.seek(0)
            
            st.download_button(
                label="Download Excel Report",
                data=output,
                file_name="validation_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
