from app.models.user import User

def test_create_user_persists(db_session):
    u = User(email="a@b.com", full_name="Alice")
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)

    assert u.id is not None
    assert u.email == "a@b.com"
