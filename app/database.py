from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

'''
pgsql server will not be able to parse the special character

Special Characters in URL:
If your password or username contains special characters (like @, #, :, /, etc.), they need to be URL-encoded.

For example:

Original password: P@ssw0rd!
URL-encoded: P%40ssw0rd%21

so, we can use "from urllib.parse import quote" library to parse the values used in the url

'''

user = ""
password = quote("")
host = ""
dbname = ""

database_url = f"postgresql://{user}:{password}@{host}/{dbname}"


engine = create_engine(database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
