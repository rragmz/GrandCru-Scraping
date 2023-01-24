import config
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from wines import scrap

data = scrap()

def pg_connection():
    USERNAME = config.DATABASE_CONFIG["USERNAME_DB"]
    PASSWORD = config.DATABASE_CONFIG["PASSWORD"]
    HOST = config.DATABASE_CONFIG["HOST"]
    PORT = config.DATABASE_CONFIG["PORT"]
    DATABASE = config.DATABASE_CONFIG["DATABASE"]

    engine = create_engine(
        f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
        isolation_level = 'AUTOCOMMIT',
    )

    connection = engine.connect()
    return engine

# define the table schema
Base = declarative_base()
class Wine(Base):
    __tablename__ = 'wines'
    id = Column(Integer, primary_key=True)
    product_id = Column(String)
    product_link = Column(String)
    product_image = Column(String)
    product_name = Column(String)
    product_price = Column(Float)
    type_of_wine = Column(String)
    country = Column(String)
    product_stock = Column(String)

# create the table in the database
Base.metadata.create_all(pg_connection())

# create a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=pg_connection())
session = Session()

# insert the data
for i in data:
    session.add(Wine(product_id=i['product_id'], product_link=i['product-link'], product_image=i['product-image'],product_name=i['product_name'], product_price=float(i['product-price']), type_of_wine=i['type-of-wine'], country=i['country'], product_stock=i['product-stock']))
    

session.commit()
