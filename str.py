import streamlit as st
import pandas as pd
import re
from io import BytesIO
import openpyxl

# Title of the Streamlit app
st.title("Finitials")

# File uploader for Excel files
uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'])

# If a file is uploaded
if uploaded_file is not None:
    # Read the uploaded Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Create 'doc_name' column with concatenated "First" and "Last" names
    df['doc_name'] = df["First"] + " " + df["Last"]

    # Function to format names with initials and last names
    def fred_name(s):
        # Use regular expression to extract the first letter of each word
        initials = re.findall(r'\b\w', s)

        # Extract the last word as the last name
        last_name = s.split()[-1]

        # Combine the initials and last name with dots
        result = '.'.join(initials[:-1]).upper() + '.' + last_name.title()
        return result

    # Apply the function to 'doc_name'
    df['doc_name'] = df['doc_name'].apply(fred_name)

    # Group by 'Session' and 'Course' and collect names
    grouped_df = df.groupby(['Session', 'Course'])['doc_name'].apply(lambda names: ', '.join(names)).reset_index()

    # Display the formatted output
    for _, row in grouped_df.iterrows():
        st.write(f"Session {row['Session']} - {row['Course']}: {row['doc_name']}")

    # Provide download functionality for the updated CSV
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    st.download_button(
        label="Download Updated CSV",
        data=csv_buffer,
        file_name="updated_data.csv",
        mime="text/csv"
    )
else:
    # If no file is uploaded, prompt the user to upload one
    st.write("Please upload an Excel file to process.")
