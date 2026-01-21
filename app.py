import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model
gemini_api_key = os.getenv('GOOGLE_API_KEY1')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Lets create sidebar for image upload
st.sidebar.title(':red[Upload the Images Here:]')
uploaded_image = st.sidebar.file_uploader('Images',type=['jpeg','jpg','png','jfif'],
                                          accept_multiple_files=True)
uploaded_image = [Image.open(img) for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Images have been uploaded Succesfully')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)

# Lets create the main page
st.title(':orange[STRUCTURAL DEFECT:-] :blue[AI Assited Structural Defect Identifier]')
st.markdown('#### :green[This application takes the images of the structural defects from the construction site and prepares the AI assisted report]')
title = st.text_input('Enter the title of the report:')
name = st.text_input('Enter the name of the person who has prepared the report:')
desig = st.text_input('Enter the designation of the person who has prepared the report:')
orgz = st.text_input('Enter the name of the organization:')

if st.button('SUBMIT'):
    with st.spinner('Processing...'):
        prompt = f'''
        <Role> You are and expert structural engineer with 20+ years experience in construction industry.
        <Goal> You need to prepare a detailed report on the structural defect shown in the 
        images provided by the user.
        <Context> The Images shared by the user has been attached.
        
        <Format>Follow the steps to prepare the report
        * Add title at the top of the report. The title provided by the user is {title}.
        * next add name, designation and organization of a person who has prepared the report.
        also include the date. Follwoing are the details provided by the user.
        name: {name}
        designation: {desig}
        organization: {orgz}
        date : {dt.datetime.now().date()}
        * Identify and classify the defect for eg: crack, spalling, corossion, honeycombing etc.
        * There could be more than one defects in images. Identify all defects seperately.
        * For each defect identified, provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the sevearity as low medium or high. Also mentioning if the defect is inevitable or avoidable.
        * Provide the short term and long term solution for th repair along with an estimated cost in INR and estimated time.
        * What precautionary measures can be taken to avoid these defects in future.
        
        <Instructions>
        * The report generated should be in word format.
        * Use bullet points and tabular format where ever possible.
        * Make sure the report does not exceeds 3 pages.'''

        response = model.generate_content([prompt,*uploaded_image],
                                          generation_config={'temperature':0.9}) 
        st.write(response.text)

    if st.download_button(
    label='Click To Download',
    data = response.text,
    file_name='structural_defect_report.txt',
    mime= 'text/plain'):
        st.success('Your File is Downloaded')  





