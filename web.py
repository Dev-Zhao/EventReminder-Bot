from __future__ import print_function
import sys
import os
import flask
import requests
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import pymongo

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret_464056054365-n17ssc4td11rte9fgf8jb3v5vi7e9v9e.apps.googleusercontent.com.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar.events.readonly']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = b"\xec\x15,]\xbd\xe6\xeb\xd2\xf0'\x86(Xx\xdd\x9b\x91i-OC\x91Y\xd6"

DBCRED = os.environ.get("DBCRED")
database = pymongo.MongoClient(DBCRED)["ruhacks"]
googleevents = database["googleevents"]

@app.route('/')
def index():
  return flask.render_template('index.html')


@app.route('/calendar')
def test_api_request():
  result = googleevents.find_one({"userID": flask.request.args["userID"]})

  if result == None:
    return '', 404

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **result['credentials'])

  calendar = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)

  events = calendar.events().list(calendarId='primary', orderBy='startTime', pageToken=None).execute()

  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  googleevents.update(
    { "userID": flask.request.args["userID"] },
    {
      "$set": {"credentials": credentials }
    }
  )
  print(events)
  return flask.jsonify(**events)


@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true',
      state=flask.request.args["userID"])

  print(authorization_url, file=sys.stderr)
  data = {'authorization_url': authorization_url}
  return data


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  print(flask.request.args)
  state = flask.request.args['state']
  print(state)
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  googleevents.update(
    { "userID": flask.request.args['state'] },
    {
      "$set": {"credentials": credentials_to_dict(credentials) }
    }
  )

  return bytes("Success!", "utf-8")


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def print_index_table():
    resp = flask.make_response(flask.render_template("index.html"))
    resp.mimetype = 'text/plain'
    return resp


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('https://event-reminder-discord-bot.herokuapp.com', 8080, debug=True)

