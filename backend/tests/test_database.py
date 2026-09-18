from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.db.session import create_database_engine


def test_database_engine_executes_query():
    engine = create_database_engine("sqlite://")

    TestSession = sessionmaker(bind=engine)

    with TestSession() as session:
        result = session.scalar(text("SELECT 1"))

    assert result == 1

    engine.dispose()


def test_database_transaction_persists_data(tmp_path):
    database_path = tmp_path / "test.db"
    database_url = f"sqlite:///{database_path}"

    engine = create_database_engine(database_url)
    TestSession = sessionmaker(bind=engine)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE notes (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL
                )
                """
            )
        )

    with TestSession() as session:
        session.execute(
            text(
                """
                INSERT INTO notes (content)
                VALUES (:content)
                """
            ),
            {"content": "Database foundation"},
        )
        session.commit()

    with TestSession() as session:
        content = session.scalar(
            text("SELECT content FROM notes")
        )

    assert content == "Database foundation"

    engine.dispose()


def test_uncommitted_transaction_is_not_persisted(tmp_path):
    database_path = tmp_path / "rollback.db"
    database_url = f"sqlite:///{database_path}"

    engine = create_database_engine(database_url)
    TestSession = sessionmaker(bind=engine)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE notes (
                    id INTEGER PRIMARY KEY,
                    content TEXT NOT NULL
                )
                """
            )
        )

    with TestSession() as session:
        session.execute(
            text(
                """
                INSERT INTO notes (content)
                VALUES (:content)
                """
            ),
            {"content": "Do not persist"},
        )
        session.rollback()

    with TestSession() as session:
        count = session.scalar(
            text("SELECT COUNT(*) FROM notes")
        )

    assert count == 0

    engine.dispose()