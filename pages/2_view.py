import streamlit as st
import tempfile
import os
import io
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image

credentials={
  "type": st.secrets["type"],
  "project_id": st.secrets["project_id"],
  "private_key_id": st.secrets["private_key_id"],
  "private_key": st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id": st.secrets["client_id"],
  "auth_uri": st.secrets["auth_uri"],
  "token_uri": st.secrets["token_uri"],
  "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
  "client_x509_cert_url": st.secrets["client_x509_cert_url"]
}

folder_IDs = ["13HOZK7mDooKkAL0LAekUiaOnn6p0hVnl","1pAef5Z5cPpUuWp_CuuNCUp70TYhmwVbQ","1DEN4GfCR_bgof5yhZhUHY5lGet85pdlB"]
SCOPES = ['https://www.googleapis.com/auth/drive']
#SERVICE_ACCOUNT_FILE = 'vitvault-e1a0e0732033.json'
#PARENT_FOLDER_ID = "1BsQ8U_8vSRMk-5IeYSDQdFlBnggN1y6N"
#FILE_ID = "1IK-yUAXFmynsoBldj3KVSTBMtBg4TkM-"
st.title("View Question Papers")
#st.sidebar.markdown("# VITvault")
subjects = ["MAT","ECE","CSE"]
subject = st.selectbox("subject",subjects)
if subject == "MAT":
    PARENT_FOLDER_ID = folder_IDs[0]
    FILE_ID = "16YL6vkptPsc7OwX5G3HlCp1b_umVY50Z"
elif subject == "ECE":
    PARENT_FOLDER_ID = folder_IDs[1]
    FILE_ID = "1sTepgJzTmpKuxbEmfvjhCD3syHPLvNRg"
elif subject == "CSE":
    PARENT_FOLDER_ID = folder_IDs[1]
    FILE_ID = "1c0ivU-Po7L6GL3N35rFJ96QnzFfjwh6z"

#python code 
creds = " "
def authenticate():
    creds = service_account.Credentials.from_service_account_info(credentials, scopes = SCOPES)
    return creds
st.write(creds)
def download_file(file_id, output_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    # Retrieve the file metadata
    file_metadata = service.files().get(fileId=file_id).execute()
    
    # Download the file content
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, mode='wb')
    downloader = io.BytesIO()
    downloader.write(request.execute())
    fh.write(downloader.getvalue())
    fh.close()

#download files
img = " "
view = st.button("View")
if view:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, "MAT")
    download_file(FILE_ID,path)
    
    st.write(path)
#    with pdfplumber.open(path)as pdf:
#        pages = pdf.pages[0]
#        st.write(pages.extract_text())
#   page = 
    img = Image.open(path)
    st.image(
        img , 
        width = 500,
        channels = "RGB"
    )
    