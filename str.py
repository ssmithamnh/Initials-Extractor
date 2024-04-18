import streamlit as st
import pandas as pd
from io import StringIO

# Function to get initials from a name
def get_initials(name):
    # Split the name into parts and get the first letter of each part
    parts = name.split()
    initials = ''.join([part[0].upper() for part in parts])
    return initials

# Function to convert DataFrame to CSV download link
def convert_df_to_csv(df):
    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)
    # Create a string buffer
    buffer = StringIO(csv)
    # Return the buffer
    return buffer.getvalue()

# Streamlit app main body
def main():
    st.title('Initials Extractor')

    # File uploader allows user to add their own Excel
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])

    if uploaded_file is not None:
        # Read Excel file into DataFrame
        try:
            df = pd.read_excel(uploaded_file)

            # Check if 'Name' column is in the DataFrame
            if 'Name' in df.columns:
                # Apply the get_initials function
                df['Initials'] = df['Name'].apply(get_initials)
                st.write('Updated DataFrame with Initials:')
                st.dataframe(df)

                # Convert updated DataFrame to CSV
                csv = convert_df_to_csv(df)
                # Create download link
                st.download_button(label="Download CSV", data=csv, file_name='updated_data.csv', mime='text/csv')
            else:
                st.error("The uploaded file does not contain a 'Name' column.")
        except Exception as e:
            st.error(f"An error occurred while reading the Excel file: {e}")

# Run the app
if __name__ == "__main__":
    main()