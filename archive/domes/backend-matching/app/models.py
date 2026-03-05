from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Provision(Base):
    __tablename__ = "provisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    citation = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    full_text = Column(Text, nullable=False)
    domain = Column(Text, nullable=False)
    provision_type = Column(Text, nullable=False)
    applies_when = Column(Text, nullable=False, default="{}")
    enforcement_mechanisms = Column(Text, nullable=False, default="[]")
    source_url = Column(Text, default="")
    cross_references = Column(Text, nullable=False, default="[]")
