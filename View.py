from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

# Step 1: Start OAuth flow
class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'path_to_client_secret.json',  # Path to your client_secret.json file
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return Response({'authorization_url': authorization_url})

# Step 2: Handle redirect and get access_token and list of events
class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'path_to_client_secret.json',  # Path to your client_secret.json file
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

        # Use 'credentials' to make API requests (e.g., get events from user's calendar)
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        return Response({'access_token': credentials.token, 'events': events})

