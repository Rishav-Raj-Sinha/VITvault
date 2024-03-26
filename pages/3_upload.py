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

SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = "1BsQ8U_8vSRMk-5IeYSDQdFlBnggN1y6N"
st.title("Upload Question Papers")
#sidebar
#st.sidebar.markdown("# VITvault")
subjects = ["MAT","CSE","EEE","PLA"]
subject = st.selectbox("subject",subjects)

#python code 
def authenticate():
    creds = service_account.Credentials.from_service_account_info(credentials, scopes = SCOPES)
    return creds
def upload_file(file_path):
    creds = authenticate()
    service = build('drive', 'v3' , credentials=creds)
    file_metadata = {
        'name' : subject,
        'parents' : [PARENT_FOLDER_ID]
    }
    file = service.files().create(
        body = file_metadata,
        media_body = file_path
    ).execute()

#mainpage
img = st.file_uploader("To upload a question paper browse or drag and drop the file in png format",type=["png"])
#creating a temp directory to store the pdf and get a path for this directory to pass to the drive api
path = " "
if img:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, img.name)
        with open(path, "wb") as f:
                f.write(img.getvalue())
#st.write(path)
upload = st.button("Upload")

if upload:
    upload_file(path)
    st.success('Thanks for you contribution!', icon="❤️")

