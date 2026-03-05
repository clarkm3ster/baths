from sqlalchemy import Column, String, Float, Integer, Boolean, Text
from app.database import Base


class Parcel(Base):
    __tablename__ = "parcels"

    parcel_number = Column(String, primary_key=True, index=True)
    address = Column(String, default="")
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    # Ownership
    owner = Column(String, default="")  # raw owner_1
    owner_agency = Column(String, default="", index=True)  # normalized

    # Physical
    total_area_sqft = Column(Float, default=0)
    zoning = Column(String, default="")
    category_code = Column(String, default="")
    category_description = Column(String, default="")
    frontage = Column(Float, default=0)
    depth = Column(Float, default=0)
    exterior_condition = Column(String, default="")
    year_built = Column(String, default="")
    geographic_ward = Column(String, default="")
    zip_code = Column(String, default="")

    # Value
    market_value = Column(Float, default=0)
    taxable_land = Column(Float, default=0)
    taxable_building = Column(Float, default=0)
    exempt_land = Column(Float, default=0)
    exempt_building = Column(Float, default=0)

    # Computed
    activation_score = Column(Integer, default=0, index=True)
    activation_categories = Column(Text, default="[]")  # JSON list
    vacancy_likely = Column(Boolean, default=False)
