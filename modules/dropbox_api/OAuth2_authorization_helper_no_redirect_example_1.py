from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
APP_KEY = 'orl3775x8jdgcg0'
APP_SECRET = 'cgz8tvz8k4uiubx'

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

authorize_url = auth_flow.start()

print("1. Go to: " + authorize_url)
print('2. Click\Allow\\(you might have to log in first).')
print("3. Copy the authorization code.")

auth_code = input("Enter the authorization code here: ").strip()
oauth_result = ''
try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error:% s' % e, )

dbx = Dropbox(oauth_result.access_token)

