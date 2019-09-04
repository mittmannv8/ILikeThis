from src.app import get_session, create_app

session = get_session()
app = create_app(session())
