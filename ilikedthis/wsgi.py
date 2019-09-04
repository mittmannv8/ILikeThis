from ilikedthis.app import create_app, get_session

session = get_session()
app = create_app(session())
