from googleapiclient.discovery import build
from google.auth import default, iam
from google.auth.transport import requests
from google.oauth2 import service_account
import json

token_uri = 'https://accounts.google.com/o/oauth2/token'
scopes = ['https://apps-apis.google.com/a/feeds/groups/', 
        'https://www.googleapis.com/auth/admin.directory.group', 
        'https://www.googleapis.com/auth/admin.directory.group.readonly']
workspace_admin = 'sudheerv@devopscounsel.com'

def generate_credentials(credentials, subject, scopes):
    try:
        updated_credentials = credentials.with_subject(subject).with_scopes(scopes)
    except AttributeError:
        request = requests.Request()
        credentials.refresh(request)
        signer = iam.Signer(
            request,
            credentials,
            credentials.service_account_email
        )
        updated_credentials = service_account.Credentials(
            signer,
            credentials.service_account_email,
            token_uriI,
            scopes=scopes,
            subject=subject
        )
    except Exception:
        raise
    return updated_credentials


creds, project = default()
creds = generate_credentials(creds, workspace_admin, scopes) 
service = build('admin', 'directory_v1', credentials=creds)
try:
    groups_list = service.groups().list(domain='devopscounsel.com').execute()
except Exception:
    raise
groups_list = json.loads(json.dumps(groups_list))
for group in groups_list['groups']:
    print(group['email'])
