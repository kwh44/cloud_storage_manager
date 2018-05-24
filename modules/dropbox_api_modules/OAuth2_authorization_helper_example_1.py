from dropbox import DropboxOAuth2Flow

APP_KEY = 'orl3775x8jdgcg0'
APP_SECRET = 'cgz8tvz8k4uiubx'

def get_dropbox_auth_flow(web_app_session):
    redirect_uri= "https://my-web-server.org/dropbox-auth-finish"
    return DropboxOAuth2Flow(APP_KEY, APP_SECRET, redirect_uri, web_app_session,
                             "dropbox-auth-csrf-token")


# URL handler for /dropbox-auth-start
def dropbox_auth_start(web_app_session, request):
    authorize_url = get_dropbox_auth_flow(web_app_session).start()
    # redirect_to(authorize_url) # redirect_to() function is implemented yet


# URL handler for /dropbox-auth-finish
def dropbox_auth_finish(web_app_session, request):
    try:
        oauth_result = get_dropbox_auth_flow(web_app_session).finish(request.query_params)
    except BadRequestException as e:
        pass
        # http_status(400)
    except BadStateException as e:
        # Start the auth flow again.
        pass
        # redirect_to("/dropbox-auth-start")
    except CsrfException as e:
        pass
        # http_status(403)
    except NotApprovedException as e:
        pass
        # flash('Not approved?  Why not?') # flash() function is not implemented
        # return redirect_to("/home")
    except ProviderException as e:
        pass
        # logger.log("Auth error:%s" % (e,))
        # http_status(403
