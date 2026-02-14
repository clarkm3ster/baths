"""
Philadelphia Permit & Approval Pathway Database
================================================
Comprehensive database of every permit type required for public space
activation in the City of Philadelphia, with decision-tree routing
for multi-permit workflows.

Data sources: Philadelphia Code Title 10, Title 14 (Zoning),
Streets Department regulations, Parks & Recreation permit schedules,
Department of Licenses & Inspections bulletins, Commerce Department
guidelines, Managing Director's Office special event protocols.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class PermitType:
    id: str
    name: str
    issuing_agency: str
    description: str
    application_process: list[str]
    timeline_days: int
    cost_range: dict  # {"min": float, "max": float}
    requirements: list[str]
    restrictions: list[str]
    seasonal_limitations: Optional[list[str]]
    applicable_zoning: list[str]
    applicable_property_types: list[str]


# ---------------------------------------------------------------------------
# Permit definitions -- Philadelphia-specific
# ---------------------------------------------------------------------------

FILM_PERMIT = PermitType(
    id="film_permit",
    name="Film Permit",
    issuing_agency="Greater Philadelphia Film Office (Commerce Department)",
    description=(
        "Required for all commercial film, television, documentary, and "
        "professional photography productions on public property in "
        "Philadelphia. Covers crew staging, equipment placement, and "
        "temporary set construction on city-owned land and rights-of-way."
    ),
    application_process=[
        "Submit Film Permit Application to the Greater Philadelphia Film Office at least 10 business days before shoot date",
        "Provide proof of general liability insurance ($1M per occurrence, $2M aggregate) naming the City of Philadelphia as additional insured",
        "Include detailed location map with crew parking, equipment staging, and camera positions",
        "Submit traffic management plan if any street or sidewalk impact is anticipated",
        "Obtain written consent from adjacent property owners within 100 feet of filming location",
        "Pay permit fee based on crew size and production scope",
        "Attend pre-production meeting with Film Office coordinator if production involves pyrotechnics, stunts, or street closures",
        "Receive approved permit and post copies at all filming locations during production",
    ],
    timeline_days=15,
    cost_range={"min": 0.0, "max": 1500.0},
    requirements=[
        "General liability insurance: $1,000,000 per occurrence / $2,000,000 aggregate",
        "Workers compensation insurance for all crew",
        "City of Philadelphia named as additional insured on all policies",
        "Certificate of insurance filed with Film Office 5 business days before shoot",
        "Signed hold-harmless and indemnification agreement",
        "Proof of Philadelphia Business Income & Receipts Tax (BIRT) registration",
        "On-site production coordinator designated as city liaison",
    ],
    restrictions=[
        "No filming in active construction zones without L&I coordination",
        "No drone/UAS operations without separate FAA Part 107 waiver and city approval",
        "Noise levels must comply with Philadelphia Code 10-403 (noise ordinance)",
        "No blocking of fire hydrants, bus stops, or emergency vehicle access",
        "All locations must be restored to pre-production condition within 24 hours of wrap",
        "Filming in residential areas restricted to 7:00 AM - 10:00 PM unless special variance granted",
    ],
    seasonal_limitations=None,
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX", "I-1", "I-2", "I-3",
        "RM-1", "RM-2", "RM-3", "RM-4", "RSD-1", "RSD-2", "RSD-3",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
        "SP-PO-A", "SP-PO-P", "SP-INS", "SP-STA", "SP-AIR", "SP-ENT",
    ],
    applicable_property_types=["park", "street", "sidewalk", "plaza", "parking_lot", "vacant_lot"],
)

SPECIAL_EVENT_PERMIT = PermitType(
    id="special_event_permit",
    name="Special Event Permit",
    issuing_agency="Managing Director's Office -- Office of Special Events",
    description=(
        "Required for any organized public gathering of 75 or more people "
        "on city-owned property or public rights-of-way. Covers festivals, "
        "rallies, parades, races, concerts, and large community celebrations. "
        "Events under 75 attendees on park land require a separate Parks & "
        "Recreation reservation instead."
    ),
    application_process=[
        "Submit Special Event Application to the Managing Director's Office at least 90 days before event date for large events (500+ attendees) or 45 days for smaller events",
        "Complete the online Special Events Portal application at phila.gov/special-events",
        "Provide event site plan showing stage, vendor, restroom, and emergency egress locations",
        "Submit security and crowd management plan (events over 250 attendees require licensed private security)",
        "Provide proof of general liability insurance ($1M per occurrence) naming City as additional insured",
        "Obtain Philadelphia Department of Public Health approval if food service is involved",
        "Obtain Streets Department approval for any street closures or parking restrictions",
        "Submit noise variance application to L&I if amplified sound will exceed 65 dB at property line",
        "Pay permit fee and post-event cleanup deposit",
        "Attend inter-agency coordination meeting (required for events over 1,000 attendees)",
    ],
    timeline_days=90,
    cost_range={"min": 150.0, "max": 5000.0},
    requirements=[
        "General liability insurance: $1,000,000 per occurrence naming City as additional insured",
        "Security plan with licensed security personnel for events over 250 attendees",
        "Emergency medical services plan (events over 500 require on-site EMS)",
        "Portable sanitation: minimum 1 unit per 100 attendees",
        "ADA-compliant event layout with accessible routes, viewing areas, and restrooms",
        "Trash and recycling plan meeting Philadelphia Zero Waste standards",
        "Signed hold-harmless agreement",
        "BIRT registration if event generates revenue",
    ],
    restrictions=[
        "No events in Fairmount Park without separate Fairmount Park Commission approval",
        "Amplified sound prohibited after 10:00 PM in residential-adjacent areas",
        "No sale of alcohol without separate PLCB Special Occasion Permit",
        "Street closures require 30-day advance notice to SEPTA for bus route detours",
        "Events on Benjamin Franklin Parkway require additional Art Commission review",
        "No open flames or pyrotechnics without Philadelphia Fire Department permit",
        "Event organizer must provide 24-hour emergency contact to the city",
    ],
    seasonal_limitations=[
        "Benjamin Franklin Parkway restricted June-September for existing city programming",
        "Outdoor events in flood-prone areas (Manayunk, East Falls) may require additional review during March-May",
        "Holiday season (November-January) events in Center City require 120-day advance application",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "SP-PO-A", "SP-PO-P", "SP-ENT", "SP-STA",
    ],
    applicable_property_types=["park", "street", "sidewalk", "plaza", "parking_lot"],
)

TEMPORARY_USE_PERMIT = PermitType(
    id="temporary_use_permit",
    name="Temporary Use Agreement / License",
    issuing_agency="Philadelphia Land Bank / Department of Public Property",
    description=(
        "A temporary use agreement or license for activation of city-owned "
        "vacant land or surplus property. Covers community gardens, pop-up "
        "markets, temporary recreation, and neighborhood beautification on "
        "parcels in the Philadelphia Land Bank inventory or under the "
        "Department of Public Property."
    ),
    application_process=[
        "Verify parcel ownership and Land Bank inventory status via Philadelphia Atlas (atlas.phila.gov)",
        "Submit Temporary Use License Application to the Philadelphia Land Bank",
        "Provide site plan showing proposed use, fencing, access points, and any structures",
        "Submit community engagement documentation (letter of support from registered community organization or neighborhood advisory committee)",
        "Provide proof of general liability insurance ($1M per occurrence) naming City and Land Bank as additional insured",
        "Complete environmental screening questionnaire (Land Bank will order Phase I ESA if warranted)",
        "Execute Temporary Use License Agreement (typically 1-year term, renewable)",
        "Pay annual license fee",
    ],
    timeline_days=60,
    cost_range={"min": 0.0, "max": 500.0},
    requirements=[
        "General liability insurance: $1,000,000 per occurrence",
        "Letter of support from Registered Community Organization (RCO) or neighborhood group",
        "Site maintenance plan including mowing, litter removal, and snow clearance",
        "No permanent structures without separate L&I building permit",
        "Environmental compliance: no disturbance of soil on parcels with known contamination without remediation plan",
        "Quarterly status reports to Land Bank",
    ],
    restrictions=[
        "License is revocable with 30 days notice",
        "No sublicensing or assignment without Land Bank approval",
        "No overnight habitation or storage of hazardous materials",
        "Structures limited to temporary/removable installations (sheds, raised beds, shade structures)",
        "Licensee responsible for all property taxes if applicable",
        "No commercial use without separate commercial license",
    ],
    seasonal_limitations=None,
    applicable_zoning=[
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
        "RSD-1", "RSD-2", "RSD-3",
        "CMX-1", "CMX-2", "CMX-2.5",
        "I-1", "I-2",
        "ICMX",
    ],
    applicable_property_types=["vacant_lot", "parking_lot"],
)

ENCROACHMENT_PERMIT = PermitType(
    id="encroachment_permit",
    name="Encroachment Permit",
    issuing_agency="Philadelphia Streets Department -- Right-of-Way Unit",
    description=(
        "Required when any private installation or activation encroaches "
        "into the public right-of-way, including awnings, planters, "
        "bollards, seating, signage, bike racks, or art installations "
        "that extend beyond the property line into the sidewalk or street."
    ),
    application_process=[
        "Submit Encroachment Permit Application to the Streets Department Right-of-Way Unit",
        "Provide survey or site plan showing property line, proposed encroachment, and dimensioned clearances",
        "Demonstrate minimum 5-foot clear pedestrian passage on sidewalk (ADA requirement)",
        "Obtain written approval from abutting property owners if encroachment affects their frontage",
        "Pay application fee and annual encroachment license fee",
        "Execute Encroachment License Agreement with indemnification clause",
        "Schedule Streets Department field inspection after installation",
    ],
    timeline_days=30,
    cost_range={"min": 100.0, "max": 1200.0},
    requirements=[
        "Minimum 5-foot clear pedestrian path on sidewalk maintained at all times",
        "General liability insurance: $500,000 minimum naming City as additional insured",
        "Encroachment cannot obstruct fire hydrants, utility access, or stormwater infrastructure",
        "Annual renewal required -- non-renewal results in mandatory removal at licensee expense",
        "All installations must meet Philadelphia Building Code structural requirements",
    ],
    restrictions=[
        "No encroachment into travel lanes without separate street closure permit",
        "Encroachments in historic districts (Old City, Society Hill, Rittenhouse) require Historical Commission review",
        "No permanent foundation or below-grade installation without separate excavation permit",
        "Encroachment must not impede sight lines at intersections (sight triangle requirement)",
        "City reserves right to require removal with 48-hour notice for emergency utility work",
    ],
    seasonal_limitations=None,
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "I-1", "I-2",
        "SP-ENT", "SP-STA",
    ],
    applicable_property_types=["sidewalk", "street"],
)

STREET_CLOSURE_PERMIT = PermitType(
    id="street_closure_permit",
    name="Street Closure Permit",
    issuing_agency="Philadelphia Streets Department -- Traffic Engineering Division",
    description=(
        "Required for any temporary closure of a public street, alley, or "
        "traffic lane for events, construction, filming, or community "
        "activities. Includes full closures, partial lane restrictions, "
        "and temporary parking prohibitions."
    ),
    application_process=[
        "Submit Street Closure Application to Streets Department Traffic Engineering at least 30 days before closure date",
        "Provide traffic management plan (TMP) prepared by a Pennsylvania-certified flagger or traffic engineer",
        "Include detour route map with signage plan conforming to PennDOT Publication 213",
        "Notify SEPTA at least 30 days in advance if closure affects bus routes",
        "Notify Philadelphia Fire Department and Police Department of closure dates and detour routes",
        "Post No Parking signs (temporary) at least 72 hours before closure",
        "Pay closure permit fee based on duration and roadway classification",
        "Provide proof of general liability insurance ($1M per occurrence)",
    ],
    timeline_days=30,
    cost_range={"min": 200.0, "max": 3000.0},
    requirements=[
        "Traffic management plan (TMP) conforming to Manual on Uniform Traffic Control Devices (MUTCD)",
        "Pennsylvania-certified flaggers on-site during partial closures",
        "Emergency vehicle access maintained at all times -- minimum 20-foot clear lane",
        "General liability insurance: $1,000,000 per occurrence naming City as additional insured",
        "Temporary No Parking signs posted 72 hours in advance with Streets Department approval",
        "Notification to all affected businesses and residents within 300 feet",
    ],
    restrictions=[
        "No closures on arterial streets (Broad Street, Market Street, Chestnut Street, Walnut Street) without mayoral office approval",
        "Interstate and state route closures (I-76, I-95, Roosevelt Boulevard) require PennDOT coordination",
        "SEPTA bus route streets require 45-day advance notice minimum",
        "No closures during Philly Free Streets, Made in America, or other major city events without Managing Director's Office approval",
        "Maximum 14-day continuous closure without renewal",
        "Closures in Center City Improvement District require additional CCID coordination",
    ],
    seasonal_limitations=[
        "Street closures in Center City heavily restricted November 15 - January 2 (holiday shopping season)",
        "Closures near stadiums restricted on game days (Eagles, Phillies, Union, 76ers, Flyers)",
        "University City closures restricted during Penn/Drexel commencement weeks in May",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSD-1", "RSD-2", "RSD-3",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
        "I-1", "I-2", "I-3",
        "SP-PO-A", "SP-PO-P", "SP-STA", "SP-ENT",
    ],
    applicable_property_types=["street"],
)

PARK_USE_PERMIT = PermitType(
    id="park_use_permit",
    name="Park Use Permit / Reservation",
    issuing_agency="Philadelphia Parks & Recreation",
    description=(
        "Required for organized activities, gatherings, and installations "
        "in any Philadelphia park, playground, recreation center grounds, "
        "or Fairmount Park property. Covers picnic reservations, athletic "
        "field use, organized group activities, and temporary installations "
        "in park spaces."
    ),
    application_process=[
        "Submit Park Use Permit Application via PhillyParks portal or in-person at Parks & Recreation headquarters (1515 Arch Street)",
        "Identify specific park, area, and dates requested",
        "Provide event description including expected attendance, equipment, and activities",
        "Submit site plan if any temporary structures, stages, or equipment will be installed",
        "Provide proof of general liability insurance for events over 75 attendees",
        "Pay permit fee and refundable damage deposit",
        "Receive permit -- post at event site during activity",
    ],
    timeline_days=21,
    cost_range={"min": 50.0, "max": 2500.0},
    requirements=[
        "General liability insurance required for events over 75 attendees: $1,000,000 per occurrence",
        "Damage deposit: $250-$2,500 depending on park and event size",
        "Portable restrooms required for events over 100 attendees if park restrooms are inadequate",
        "Event cleanup completed within 4 hours of event end",
        "No vehicles on park grounds without prior authorization",
        "Compliance with Philadelphia Parks & Recreation Rules (Chapter 10-800 of Philadelphia Code)",
    ],
    restrictions=[
        "No amplified sound after 9:00 PM in neighborhood parks",
        "No alcohol without separate Parks & Recreation alcohol variance and PLCB Special Occasion Permit",
        "No stakes, anchors, or ground penetration without prior approval (underground utility clearance required)",
        "No inflatables or bounce houses without separate insurance rider",
        "Fairmount Park properties require additional Fairmount Park Conservancy coordination",
        "Historic park structures (pavilions, boathouses) require separate facility rental agreement",
        "No commercial activities without Commercial Activity in Parks permit",
    ],
    seasonal_limitations=[
        "Athletic fields closed during spring thaw and re-seeding periods (typically March 1 - April 15)",
        "Wissahickon Valley trails restricted during hunting season (select dates in November-January)",
        "Outdoor pool areas available for events only during non-swimming season (September - May)",
    ],
    applicable_zoning=[
        "SP-PO-A", "SP-PO-P",
    ],
    applicable_property_types=["park"],
)

VACANT_LAND_GARDEN_LICENSE = PermitType(
    id="vacant_land_garden_license",
    name="Community Garden / Vacant Land Activation License",
    issuing_agency="Pennsylvania Horticultural Society (PHS) / Philadelphia Land Bank",
    description=(
        "License and support program for establishing community gardens, "
        "urban farms, and greening projects on vacant land in Philadelphia. "
        "PHS LandCare and the Philadelphia Land Bank jointly administer "
        "the community garden licensing program, providing liability "
        "coverage, materials, and technical assistance."
    ),
    application_process=[
        "Contact PHS Community Gardens program or Philadelphia Land Bank to identify eligible parcels",
        "Form a garden committee of at least 3 neighborhood residents",
        "Submit Garden License Application including garden plan, committee roster, and maintenance schedule",
        "Obtain letter of support from Registered Community Organization (RCO)",
        "Complete PHS garden orientation workshop (offered quarterly)",
        "Execute Garden License Agreement with Land Bank or property owner",
        "Schedule soil testing through Penn State Extension if growing food crops",
        "Install required fencing and signage per license terms",
    ],
    timeline_days=45,
    cost_range={"min": 0.0, "max": 100.0},
    requirements=[
        "Garden committee of minimum 3 Philadelphia residents",
        "RCO letter of support",
        "Soil testing for food production gardens (lead and heavy metals screening)",
        "Fencing: minimum 4-foot perimeter fence with locking gate",
        "Signage: garden name, contact information, and hours posted at entrance",
        "Regular maintenance: mowing, weeding, litter removal, and seasonal cleanup",
        "Annual renewal with updated committee roster",
        "Water access plan (rain barrels, nearby hydrant permit, or utility connection)",
    ],
    restrictions=[
        "No permanent structures without L&I building permit",
        "No livestock other than chickens (maximum 4 hens, no roosters per Philadelphia Code 10-112)",
        "No herbicides or pesticides classified as Restricted Use by EPA",
        "Garden hours: dawn to dusk unless lighting is installed with L&I electrical permit",
        "No sale of produce exceeding $15,000 annual revenue without commercial licensing",
        "No tree removal without separate Philadelphia Parks & Recreation tree removal permit",
    ],
    seasonal_limitations=[
        "Soil testing recommended March-May before growing season",
        "PHS orientation workshops offered January, April, July, October",
    ],
    applicable_zoning=[
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
        "RSD-1", "RSD-2", "RSD-3",
        "CMX-1", "CMX-2",
        "I-1",
    ],
    applicable_property_types=["vacant_lot"],
)

RIGHT_OF_WAY_PERMIT = PermitType(
    id="right_of_way_permit",
    name="Right-of-Way Occupancy Permit",
    issuing_agency="Philadelphia Streets Department -- Right-of-Way Unit",
    description=(
        "Required for any temporary or semi-permanent occupancy of the "
        "public right-of-way for purposes other than transportation, "
        "including dumpster placement, scaffolding, construction staging, "
        "pop-up installations, and utility work that occupies sidewalk or "
        "street space."
    ),
    application_process=[
        "Submit Right-of-Way Occupancy Permit Application to Streets Department",
        "Provide dimensioned site plan showing occupied area, clear pedestrian path, and duration",
        "Demonstrate minimum 5-foot clear pedestrian walkway maintained at all times",
        "Submit traffic control plan if occupancy affects travel lanes",
        "Provide proof of general liability insurance ($1M per occurrence) naming City as additional insured",
        "Pay permit fee based on square footage and duration of occupancy",
        "Receive permit placard -- display at occupancy site for duration",
    ],
    timeline_days=14,
    cost_range={"min": 75.0, "max": 800.0},
    requirements=[
        "Minimum 5-foot clear pedestrian path on sidewalk (ADA compliant)",
        "General liability insurance: $1,000,000 per occurrence",
        "Reflective barricades and signage conforming to MUTCD standards",
        "Nighttime lighting if occupancy creates pedestrian hazard",
        "Daily inspection and maintenance of barricades and signage",
        "Restoration of right-of-way to original condition upon permit expiration",
    ],
    restrictions=[
        "Maximum 6-month duration without renewal",
        "No occupancy within 15 feet of fire hydrant",
        "No occupancy blocking building egress, ADA ramps, or transit stops",
        "Occupancy in Center City requires additional CCID notification",
        "No overnight storage of materials without additional approval",
        "Must comply with Philadelphia Stormwater Management requirements if impervious surface is placed",
    ],
    seasonal_limitations=[
        "Sidewalk occupancy in commercial corridors restricted during holiday season (November 15 - January 2)",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "I-1", "I-2", "I-3",
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSD-1", "RSD-2", "RSD-3",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
    ],
    applicable_property_types=["sidewalk", "street"],
)

FOOD_VENDING_PERMIT = PermitType(
    id="food_vending_permit",
    name="Food Vending / Mobile Food Facility Permit",
    issuing_agency="Philadelphia Department of Public Health -- Environmental Health Services / Department of Licenses & Inspections",
    description=(
        "Required for all food vending from mobile units (food trucks, "
        "carts, trailers) and temporary food stands on public property "
        "or rights-of-way in Philadelphia. Includes both the health "
        "department food facility permit and the L&I vending license."
    ),
    application_process=[
        "Obtain Philadelphia Business Privilege License from the Department of Revenue",
        "Register for BIRT (Business Income & Receipts Tax) with the Department of Revenue",
        "Submit Mobile Food Facility Plan Review Application to the Department of Public Health",
        "Pass Department of Public Health plan review (menu, equipment layout, water/waste systems)",
        "Schedule and pass Department of Public Health mobile food facility inspection",
        "Obtain Food Establishment License from Department of Public Health",
        "Apply for Vending License from Department of Licenses & Inspections (L&I)",
        "Submit proposed vending location(s) to L&I for location approval",
        "Pay all applicable fees (health license, vending license, location fees)",
        "Complete ServSafe or equivalent food safety certification for at least one operator",
    ],
    timeline_days=30,
    cost_range={"min": 250.0, "max": 1500.0},
    requirements=[
        "Philadelphia Business Privilege License (annual)",
        "Department of Public Health Food Establishment License (annual)",
        "L&I Vending License (annual)",
        "ServSafe or equivalent food handler certification",
        "Commissary agreement with licensed commissary kitchen for food prep and vehicle servicing",
        "Fire extinguisher (Class K for cooking operations)",
        "Handwashing station with hot and cold running water",
        "Waste water containment -- no discharge to storm drains",
        "Menu and pricing posted visibly",
    ],
    restrictions=[
        "No vending within 200 feet of a school during school hours without school district permission",
        "No vending within 50 feet of a restaurant entrance (Philadelphia Code 9-209)",
        "No vending on Chestnut Street between 2nd and 18th Streets (Center City Food Truck Zone restrictions apply)",
        "Vending limited to approved locations -- no roaming sales in prohibited zones",
        "No vending in Fairmount Park without separate Parks & Recreation concession agreement",
        "Must move vehicle at end of operating hours -- no overnight parking at vending location",
        "Propane tanks must comply with Philadelphia Fire Code Chapter 61",
    ],
    seasonal_limitations=[
        "Some vending locations are seasonal-only (Penn's Landing, Kelly Drive) -- April through October",
        "Winter vending at Love Park / JFK Plaza subject to Christmas Village exclusivity agreements (November-December)",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "I-1", "I-2",
        "SP-ENT", "SP-STA",
    ],
    applicable_property_types=["sidewalk", "street", "plaza", "parking_lot", "park"],
)

TEMPORARY_STRUCTURE_PERMIT = PermitType(
    id="temporary_structure_permit",
    name="Temporary Structure / Tent Permit",
    issuing_agency="Department of Licenses & Inspections (L&I)",
    description=(
        "Required for erection of any temporary structure on public or "
        "private property in Philadelphia, including tents over 400 square "
        "feet, stages, platforms, bleachers, scaffolding, shipping container "
        "installations, and other non-permanent constructions."
    ),
    application_process=[
        "Submit Temporary Structure Permit Application to L&I with structural plans",
        "Provide engineer-stamped drawings for structures over 400 square feet or over 12 feet in height",
        "Submit fire protection plan (flame-retardant certification for tent fabric, exit signage, extinguisher placement)",
        "Provide proof of general liability insurance ($1M per occurrence)",
        "Schedule pre-erection site inspection with L&I",
        "Erect structure and schedule final L&I inspection before occupancy",
        "Receive Certificate of Temporary Occupancy",
    ],
    timeline_days=21,
    cost_range={"min": 200.0, "max": 2000.0},
    requirements=[
        "Structural engineering plans stamped by Pennsylvania-licensed PE for structures over 400 SF or 12 feet height",
        "Flame-retardant certification for all fabric and membrane materials (NFPA 701 compliance)",
        "Fire extinguishers: minimum 2A:10BC rated, one per 75 feet of travel distance",
        "Illuminated exit signage with battery backup",
        "General liability insurance: $1,000,000 per occurrence",
        "Wind load calculations for temporary structures (minimum 90 mph per Philadelphia Building Code)",
        "Electrical work must be performed by licensed Philadelphia electrician with separate electrical permit",
    ],
    restrictions=[
        "Maximum 180-day duration without renewal as permanent structure",
        "No temporary structures within 10 feet of property line without fire separation",
        "Occupancy load must be posted and not exceeded",
        "Structures on public property require separate right-of-way or park use permit",
        "No temporary structures in floodplain without additional FEMA compliance review",
        "Structures over 15 feet height may require Zoning Board variance",
    ],
    seasonal_limitations=[
        "Tent permits during winter months (December-February) require additional wind and snow load calculations",
        "Heated tents require Philadelphia Fire Department approval and on-site fire watch",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "I-1", "I-2", "I-3",
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSD-1", "RSD-2", "RSD-3",
        "SP-PO-A", "SP-PO-P", "SP-ENT", "SP-STA",
    ],
    applicable_property_types=["park", "street", "sidewalk", "plaza", "parking_lot", "vacant_lot"],
)

BLOCK_PARTY_PERMIT = PermitType(
    id="block_party_permit",
    name="Block Party Permit",
    issuing_agency="Philadelphia Streets Department",
    description=(
        "Permit for neighborhood block parties involving temporary closure "
        "of a residential street block. Philadelphia's block party permit "
        "is a simplified street closure process for community-organized "
        "social events on residential streets."
    ),
    application_process=[
        "Obtain Block Party Permit Application from Streets Department or download from phila.gov",
        "Collect signatures from at least 75% of residents on the affected block",
        "Submit completed application with signatures to the Streets Department at least 30 days before event",
        "Include date, time (start and end), and block location (cross streets)",
        "Pay permit fee (nominal -- subsidized for community events)",
        "Receive approved permit and temporary No Parking signs",
        "Post No Parking signs 48 hours before event",
        "Set up barricades at block ends on day of event (barricades provided by Streets Department upon request)",
    ],
    timeline_days=30,
    cost_range={"min": 0.0, "max": 50.0},
    requirements=[
        "Signatures from 75% of households on the block",
        "Designated block captain / event coordinator",
        "Barricades at each end of closed block (available from Streets Department)",
        "Emergency vehicle access maintained -- barricades must be moveable",
        "Block captain responsible for noise compliance and cleanup",
    ],
    restrictions=[
        "Residential streets only -- no arterial or collector streets",
        "Maximum duration: 6:00 AM to midnight (same day)",
        "No commercial sales without separate vending permits",
        "Maximum 3 block parties per block per calendar year",
        "No amplified music after 10:00 PM",
        "Alcohol is technically prohibited on public streets (Philadelphia Code 10-604) -- enforcement at police discretion",
        "No bounce houses or inflatables extending into adjacent properties without owner consent",
    ],
    seasonal_limitations=[
        "Block parties most commonly permitted May through October",
        "Streets Department may deny permits during periods of heavy road construction in the area",
    ],
    applicable_zoning=[
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSD-1", "RSD-2", "RSD-3",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
    ],
    applicable_property_types=["street"],
)

FARMERS_MARKET_PERMIT = PermitType(
    id="farmers_market_permit",
    name="Farmers Market / Open-Air Market Permit",
    issuing_agency="Philadelphia Department of Public Health / Department of Licenses & Inspections",
    description=(
        "Required for operating a farmers market, flea market, or "
        "open-air market on public or private property in Philadelphia. "
        "Covers market operator licensing, individual vendor health "
        "permits, and site-specific approvals for recurring market events."
    ),
    application_process=[
        "Submit Market Operator Application to the Department of Licenses & Inspections",
        "Provide market operations plan including vendor layout, traffic flow, waste management, and hours",
        "Submit site plan to Streets Department if market occupies public right-of-way",
        "Obtain Department of Public Health Temporary Food Facility permits for each food vendor",
        "Provide proof of market-wide general liability insurance ($1M per occurrence)",
        "Submit vendor roster with individual vendor business licenses to L&I",
        "Obtain zoning certification or use registration if market is on private property",
        "Pay market operator license fee",
        "Schedule Department of Public Health pre-opening inspection for food vendors",
    ],
    timeline_days=45,
    cost_range={"min": 200.0, "max": 2000.0},
    requirements=[
        "Market Operator License from L&I",
        "Department of Public Health permits for each food vendor",
        "Individual vendor Philadelphia Business Privilege Licenses",
        "General liability insurance: $1,000,000 per occurrence for market operator",
        "Handwashing stations: minimum 1 per 10 food vendors",
        "Trash and recycling receptacles at 50-foot intervals throughout market",
        "ADA-compliant layout with 5-foot minimum aisle widths",
        "Market manager on-site during all operating hours",
    ],
    restrictions=[
        "Markets on public property require Managing Director's Office special event approval if over 75 attendees expected",
        "No permanent structures -- all vendor installations must be removable same-day",
        "Food vendors must operate under tent/canopy with overhead protection per Health Code",
        "No sale of prepared cannabis products (state law)",
        "Scale vendors (selling by weight) must have Philadelphia Weights & Measures sealed scales",
        "Parking impacts must be mitigated per Streets Department requirements",
    ],
    seasonal_limitations=[
        "Outdoor markets typically operate May through November",
        "Year-round markets require heated structure plan and winter weather contingency plan",
        "Holiday markets (November-December) in Center City subject to Commerce Department coordination",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "RM-1", "RM-2", "RM-3", "RM-4",
        "SP-PO-A", "SP-PO-P", "SP-ENT",
    ],
    applicable_property_types=["sidewalk", "street", "plaza", "parking_lot", "park", "vacant_lot"],
)

PUBLIC_ART_PERMIT = PermitType(
    id="public_art_permit",
    name="Public Art Installation Permit",
    issuing_agency="Philadelphia Art Commission / Office of Arts, Culture and the Creative Economy (OACCE)",
    description=(
        "Required for installation of any artwork, mural, sculpture, "
        "or artistic installation on city-owned property or visible from "
        "the public right-of-way. The Philadelphia Art Commission (est. "
        "1911) reviews all art on city property per the Philadelphia "
        "Home Rule Charter Section 3-910."
    ),
    application_process=[
        "Submit Preliminary Application to the Philadelphia Art Commission with concept renderings and site photos",
        "Present project at Art Commission monthly public meeting (first Wednesday of each month)",
        "Receive preliminary approval or revision requests from the Commission",
        "Submit Final Application with detailed fabrication drawings, material specifications, and installation plan",
        "Present final design at subsequent Art Commission meeting for final approval",
        "Obtain structural permit from L&I if installation requires foundation, anchoring, or electrical",
        "Obtain right-of-way or park use permit from relevant department for the installation site",
        "Coordinate installation timing with site-controlling agency",
        "Schedule post-installation inspection with Art Commission staff",
    ],
    timeline_days=90,
    cost_range={"min": 0.0, "max": 500.0},
    requirements=[
        "Art Commission approval (two-phase: preliminary and final review)",
        "Detailed fabrication drawings and material specifications",
        "Structural engineering review for installations over 6 feet tall or weighing over 500 pounds",
        "Maintenance plan for duration of installation",
        "De-installation plan and timeline",
        "General liability insurance: $1,000,000 per occurrence if on city property",
        "Artist or commissioning organization must carry property damage insurance for the artwork",
    ],
    restrictions=[
        "No installation without Art Commission final approval -- no exceptions for city property",
        "Murals on private property visible from public right-of-way require Art Commission review if building receives any city funding",
        "Installations in historic districts require additional Historical Commission Certificate of Appropriateness",
        "No permanent installations without City Council ordinance authorizing permanent placement",
        "Light-based installations must not create traffic hazards (no flashing or pulsing lights near intersections)",
        "Sound installations must comply with Philadelphia noise ordinance (10-403)",
        "Temporary installations limited to 2-year maximum without renewal",
    ],
    seasonal_limitations=[
        "Art Commission does not meet in August -- plan submissions accordingly",
        "Outdoor installations of water-based or freezing-sensitive materials should account for Philadelphia winters",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "I-1", "I-2",
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSD-1", "RSD-2", "RSD-3",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
        "SP-PO-A", "SP-PO-P", "SP-ENT", "SP-STA", "SP-INS",
    ],
    applicable_property_types=["park", "street", "sidewalk", "plaza", "parking_lot", "vacant_lot"],
)

SIDEWALK_CAFE_PERMIT = PermitType(
    id="sidewalk_cafe_permit",
    name="Sidewalk Cafe Permit",
    issuing_agency="Philadelphia Streets Department / Department of Licenses & Inspections",
    description=(
        "Required for restaurants, bars, and cafes to operate outdoor "
        "dining on the public sidewalk or in a streetery (on-street "
        "dining platform). Philadelphia expanded the sidewalk cafe program "
        "post-2020, and the Streets Department now administers both "
        "traditional sidewalk seating and streetery permits."
    ),
    application_process=[
        "Submit Sidewalk Cafe Application to the Streets Department",
        "Provide dimensioned site plan showing cafe area, furniture layout, and clear pedestrian path (minimum 5 feet)",
        "Demonstrate compliance with ADA accessibility requirements for cafe area",
        "Obtain L&I Food Establishment License (if not already licensed)",
        "Submit proof of PLCB-licensed premises extension for outdoor alcohol service (if applicable)",
        "Provide proof of general liability insurance ($1M per occurrence) naming City as additional insured",
        "Pay annual sidewalk cafe license fee based on frontage and square footage",
        "For streeteries: submit engineered platform drawings and obtain L&I structural approval",
        "Schedule Streets Department site inspection before opening cafe area",
    ],
    timeline_days=30,
    cost_range={"min": 300.0, "max": 2500.0},
    requirements=[
        "Minimum 5-foot clear pedestrian path on sidewalk maintained at all times",
        "ADA-compliant cafe layout with accessible seating",
        "General liability insurance: $1,000,000 per occurrence naming City as additional insured",
        "Philadelphia Food Establishment License (current)",
        "PLCB extension of premises for outdoor alcohol service (if serving alcohol)",
        "Cafe furniture must be removable -- no permanent anchoring to sidewalk",
        "Planters, barriers, or railings required to delineate cafe area from pedestrian path",
        "No encroachment within 5 feet of fire hydrant, utility vault, or subway ventilation grate",
    ],
    restrictions=[
        "Cafe area cannot extend beyond property frontage without adjacent property owner consent",
        "No permanent roof or enclosed structure -- open-air or removable umbrella/canopy only",
        "Operating hours: 7:00 AM to 11:00 PM Sunday-Thursday, 7:00 AM to midnight Friday-Saturday (unless neighborhood-specific restrictions apply)",
        "Streeteries must not obstruct sight triangles at intersections",
        "Streeteries must include reflective markers and wheel stops conforming to Streets Department specifications",
        "No cafe seating within 15 feet of bus stop zone",
        "All furniture must be brought inside or secured nightly",
    ],
    seasonal_limitations=[
        "Traditional sidewalk cafes typically operate April through November",
        "Year-round operation requires winter weather furniture management plan",
        "Streeteries may require removal during snow emergencies (Streets Department Snow Emergency Routes)",
        "Heated outdoor dining requires Philadelphia Fire Department approval for propane heaters",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "SP-ENT",
    ],
    applicable_property_types=["sidewalk", "street"],
)

NOISE_VARIANCE_PERMIT = PermitType(
    id="noise_variance_permit",
    name="Noise Variance Permit",
    issuing_agency="Department of Licenses & Inspections (L&I) -- Code Enforcement",
    description=(
        "Required when any public space activation will generate noise "
        "exceeding the thresholds established in Philadelphia Code "
        "10-403. Covers amplified music, PA systems, construction "
        "noise outside standard hours, and any sustained sound exceeding "
        "65 dB(A) at the nearest residential property line."
    ),
    application_process=[
        "Submit Noise Variance Application to L&I at least 15 days before event/activity",
        "Provide noise impact analysis showing expected dB levels at property lines and nearest residences",
        "Include sound system specifications and directional speaker placement plan",
        "Specify noise mitigation measures (sound barriers, directional speakers, volume limiters)",
        "Provide notification plan for adjacent residents and businesses",
        "Pay variance application fee",
        "If approved, receive variance with conditions (maximum dB levels, permitted hours, monitoring requirements)",
    ],
    timeline_days=15,
    cost_range={"min": 50.0, "max": 300.0},
    requirements=[
        "Noise impact assessment or sound study",
        "Sound system specifications",
        "Designated on-site sound engineer or monitor",
        "Contact information posted at event for noise complaints",
        "Compliance with approved dB limits -- subject to L&I enforcement inspection",
    ],
    restrictions=[
        "Maximum variance: 80 dB(A) at nearest residential property line",
        "No variance grants past midnight in residential areas (RM, RSD, RSA zones)",
        "No variance for continuous construction noise -- separate construction noise waiver required",
        "Variance does not override noise provisions in other permits (park use, special event)",
        "Repeat violations may result in denial of future variance applications",
    ],
    seasonal_limitations=[
        "Applications during summer months (June-August) may receive additional scrutiny due to open-window season",
    ],
    applicable_zoning=[
        "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
        "CA-1", "CA-2", "ICMX",
        "I-1", "I-2", "I-3",
        "RM-1", "RM-2", "RM-3", "RM-4",
        "RSD-1", "RSD-2", "RSD-3",
        "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
        "SP-PO-A", "SP-PO-P", "SP-ENT", "SP-STA",
    ],
    applicable_property_types=["park", "street", "sidewalk", "plaza", "parking_lot", "vacant_lot"],
)

COMMERCIAL_ACTIVITY_IN_PARKS_PERMIT = PermitType(
    id="commercial_activity_parks_permit",
    name="Commercial Activity in Parks Permit",
    issuing_agency="Philadelphia Parks & Recreation / Fairmount Park Conservancy",
    description=(
        "Required for any commercial activity within Philadelphia park "
        "properties, including fitness classes, tours, photography "
        "sessions, food/beverage sales, equipment rental, and organized "
        "commercial recreation. Separate from the general Park Use Permit, "
        "which covers non-commercial activities."
    ),
    application_process=[
        "Submit Commercial Activity in Parks Application to Parks & Recreation",
        "Provide business plan or activity description including frequency, duration, and expected participants",
        "Submit proof of Philadelphia Business Privilege License and BIRT registration",
        "Provide proof of general liability insurance ($1M per occurrence) and professional liability if applicable",
        "Demonstrate that activity does not conflict with existing park concession agreements",
        "Pay commercial activity permit fee (based on revenue tier)",
        "Execute Commercial Activity License Agreement",
        "Schedule orientation with park district manager",
    ],
    timeline_days=30,
    cost_range={"min": 100.0, "max": 1500.0},
    requirements=[
        "Philadelphia Business Privilege License",
        "BIRT registration",
        "General liability insurance: $1,000,000 per occurrence naming City as additional insured",
        "Professional liability insurance for fitness/instruction activities",
        "Revenue reporting to Parks & Recreation quarterly",
        "Compliance with park rules and designated activity zones",
        "No exclusive use -- park remains open to public during commercial activity",
    ],
    restrictions=[
        "No exclusive use of park space -- public access must be maintained",
        "No competition with existing park concession agreements (check Fairmount Park Conservancy concession map)",
        "No commercial activity in nature preserves or ecologically sensitive areas",
        "Fitness boot camps limited to groups of 20 without additional crowd management",
        "No motorized equipment or vehicles on park grounds without separate vehicle access permit",
        "Permit holder must collect and remove all waste generated by activity",
    ],
    seasonal_limitations=[
        "Some park areas closed seasonally for turf recovery or wildlife nesting",
        "Water-adjacent activities (Boathouse Row, Schuylkill Banks) may be restricted during high-water events",
    ],
    applicable_zoning=[
        "SP-PO-A", "SP-PO-P",
    ],
    applicable_property_types=["park"],
)


# ---------------------------------------------------------------------------
# Master permit list
# ---------------------------------------------------------------------------

PERMIT_TYPES: list[PermitType] = [
    FILM_PERMIT,
    SPECIAL_EVENT_PERMIT,
    TEMPORARY_USE_PERMIT,
    ENCROACHMENT_PERMIT,
    STREET_CLOSURE_PERMIT,
    PARK_USE_PERMIT,
    VACANT_LAND_GARDEN_LICENSE,
    RIGHT_OF_WAY_PERMIT,
    FOOD_VENDING_PERMIT,
    TEMPORARY_STRUCTURE_PERMIT,
    BLOCK_PARTY_PERMIT,
    FARMERS_MARKET_PERMIT,
    PUBLIC_ART_PERMIT,
    SIDEWALK_CAFE_PERMIT,
    NOISE_VARIANCE_PERMIT,
    COMMERCIAL_ACTIVITY_IN_PARKS_PERMIT,
]

PERMIT_INDEX: dict[str, PermitType] = {p.id: p for p in PERMIT_TYPES}


# ---------------------------------------------------------------------------
# Decision-tree routing
# ---------------------------------------------------------------------------

# Maps (activation_type, parcel_type) -> list of permit IDs required.
# Order matters: the first permit in the list is the primary permit;
# subsequent entries are secondary/supporting permits.

_PATHWAY_MATRIX: dict[tuple[str, str], list[str]] = {
    # -- Events ---------------------------------------------------------------
    ("event", "park"):            ["park_use_permit", "special_event_permit", "noise_variance_permit"],
    ("event", "vacant_lot"):      ["temporary_use_permit", "special_event_permit", "noise_variance_permit"],
    ("event", "street"):          ["street_closure_permit", "special_event_permit", "noise_variance_permit"],
    ("event", "sidewalk"):        ["right_of_way_permit", "special_event_permit", "noise_variance_permit"],
    ("event", "plaza"):           ["special_event_permit", "noise_variance_permit"],
    ("event", "parking_lot"):     ["special_event_permit", "right_of_way_permit", "noise_variance_permit"],

    # -- Food vendor ----------------------------------------------------------
    ("food_vendor", "park"):      ["food_vending_permit", "commercial_activity_parks_permit"],
    ("food_vendor", "vacant_lot"):["food_vending_permit", "temporary_use_permit"],
    ("food_vendor", "street"):    ["food_vending_permit", "right_of_way_permit"],
    ("food_vendor", "sidewalk"):  ["food_vending_permit", "encroachment_permit"],
    ("food_vendor", "plaza"):     ["food_vending_permit"],
    ("food_vendor", "parking_lot"):["food_vending_permit", "right_of_way_permit"],

    # -- Art installation -----------------------------------------------------
    ("art_installation", "park"):       ["public_art_permit", "park_use_permit"],
    ("art_installation", "vacant_lot"): ["public_art_permit", "temporary_use_permit"],
    ("art_installation", "street"):     ["public_art_permit", "encroachment_permit", "street_closure_permit"],
    ("art_installation", "sidewalk"):   ["public_art_permit", "encroachment_permit"],
    ("art_installation", "plaza"):      ["public_art_permit"],
    ("art_installation", "parking_lot"):["public_art_permit", "right_of_way_permit"],

    # -- Community garden -----------------------------------------------------
    ("community_garden", "park"):       ["park_use_permit", "commercial_activity_parks_permit"],
    ("community_garden", "vacant_lot"): ["vacant_land_garden_license", "temporary_use_permit"],
    ("community_garden", "street"):     [],  # Not feasible -- handled via warnings
    ("community_garden", "sidewalk"):   [],  # Not feasible
    ("community_garden", "plaza"):      ["temporary_use_permit"],
    ("community_garden", "parking_lot"):["temporary_use_permit"],

    # -- Pop-up market --------------------------------------------------------
    ("pop_up_market", "park"):          ["park_use_permit", "farmers_market_permit", "commercial_activity_parks_permit"],
    ("pop_up_market", "vacant_lot"):    ["temporary_use_permit", "farmers_market_permit"],
    ("pop_up_market", "street"):        ["street_closure_permit", "farmers_market_permit"],
    ("pop_up_market", "sidewalk"):      ["right_of_way_permit", "farmers_market_permit", "encroachment_permit"],
    ("pop_up_market", "plaza"):         ["farmers_market_permit", "special_event_permit"],
    ("pop_up_market", "parking_lot"):   ["right_of_way_permit", "farmers_market_permit"],

    # -- Performance ----------------------------------------------------------
    ("performance", "park"):            ["park_use_permit", "noise_variance_permit"],
    ("performance", "vacant_lot"):      ["temporary_use_permit", "noise_variance_permit"],
    ("performance", "street"):          ["street_closure_permit", "special_event_permit", "noise_variance_permit"],
    ("performance", "sidewalk"):        ["right_of_way_permit", "noise_variance_permit"],
    ("performance", "plaza"):           ["special_event_permit", "noise_variance_permit"],
    ("performance", "parking_lot"):     ["right_of_way_permit", "special_event_permit", "noise_variance_permit"],

    # -- Film shoot -----------------------------------------------------------
    ("film_shoot", "park"):             ["film_permit", "park_use_permit"],
    ("film_shoot", "vacant_lot"):       ["film_permit", "temporary_use_permit"],
    ("film_shoot", "street"):           ["film_permit", "street_closure_permit"],
    ("film_shoot", "sidewalk"):         ["film_permit", "right_of_way_permit"],
    ("film_shoot", "plaza"):            ["film_permit"],
    ("film_shoot", "parking_lot"):      ["film_permit", "right_of_way_permit"],

    # -- Temporary structure --------------------------------------------------
    ("temporary_structure", "park"):       ["temporary_structure_permit", "park_use_permit"],
    ("temporary_structure", "vacant_lot"): ["temporary_structure_permit", "temporary_use_permit"],
    ("temporary_structure", "street"):     ["temporary_structure_permit", "street_closure_permit", "right_of_way_permit"],
    ("temporary_structure", "sidewalk"):   ["temporary_structure_permit", "encroachment_permit"],
    ("temporary_structure", "plaza"):      ["temporary_structure_permit"],
    ("temporary_structure", "parking_lot"):["temporary_structure_permit", "right_of_way_permit"],

    # -- Block party ----------------------------------------------------------
    ("block_party", "park"):            ["park_use_permit"],
    ("block_party", "vacant_lot"):      ["temporary_use_permit", "block_party_permit"],
    ("block_party", "street"):          ["block_party_permit"],
    ("block_party", "sidewalk"):        ["block_party_permit"],
    ("block_party", "plaza"):           ["special_event_permit"],
    ("block_party", "parking_lot"):     ["block_party_permit", "right_of_way_permit"],

    # -- Sidewalk cafe --------------------------------------------------------
    ("sidewalk_cafe", "park"):          [],  # Not applicable -- handled via warnings
    ("sidewalk_cafe", "vacant_lot"):    [],  # Not applicable
    ("sidewalk_cafe", "street"):        ["sidewalk_cafe_permit", "encroachment_permit"],
    ("sidewalk_cafe", "sidewalk"):      ["sidewalk_cafe_permit"],
    ("sidewalk_cafe", "plaza"):         ["sidewalk_cafe_permit"],
    ("sidewalk_cafe", "parking_lot"):   [],  # Not applicable
}

# Zoning-category helpers
_RESIDENTIAL_ZONES = {
    "RM-1", "RM-2", "RM-3", "RM-4",
    "RSD-1", "RSD-2", "RSD-3",
    "RSA-1", "RSA-2", "RSA-3", "RSA-4", "RSA-5",
}
_COMMERCIAL_ZONES = {
    "CMX-1", "CMX-2", "CMX-2.5", "CMX-3", "CMX-4", "CMX-5",
    "CA-1", "CA-2",
}
_INDUSTRIAL_ZONES = {"I-1", "I-2", "I-3", "ICMX"}
_SPECIAL_ZONES = {"SP-PO-A", "SP-PO-P", "SP-INS", "SP-STA", "SP-AIR", "SP-ENT"}

VALID_PARCEL_TYPES = {"park", "vacant_lot", "street", "sidewalk", "plaza", "parking_lot"}
VALID_ACTIVATION_TYPES = {
    "event", "food_vendor", "art_installation", "community_garden",
    "pop_up_market", "performance", "film_shoot", "temporary_structure",
    "block_party", "sidewalk_cafe",
}


def _zoning_warnings(zoning: str, activation_type: str, permits: list[PermitType]) -> list[str]:
    """Generate zoning-specific warnings."""
    warnings: list[str] = []

    if zoning and zoning not in _RESIDENTIAL_ZONES | _COMMERCIAL_ZONES | _INDUSTRIAL_ZONES | _SPECIAL_ZONES:
        warnings.append(
            f"Zoning district '{zoning}' is not recognized. Verify the zoning "
            f"classification at atlas.phila.gov before applying for permits."
        )

    # Check each permit's applicable zoning
    for permit in permits:
        if zoning and zoning not in permit.applicable_zoning:
            warnings.append(
                f"The '{permit.name}' may not be available in zoning district "
                f"'{zoning}'. A Zoning Board of Adjustment variance or special "
                f"exception may be required. Contact L&I Zoning Unit at "
                f"(215) 686-2525."
            )

    if zoning in _RESIDENTIAL_ZONES:
        if activation_type in ("food_vendor", "pop_up_market", "sidewalk_cafe"):
            warnings.append(
                "Commercial food/market activities in residential zoning districts "
                "typically require a Zoning Board special exception or variance. "
                "Budget an additional 60-90 days for the zoning process."
            )
        if activation_type == "event":
            warnings.append(
                "Events in residential areas are subject to stricter noise limits. "
                "Amplified sound must not exceed 65 dB(A) at the property line and "
                "must cease by 10:00 PM."
            )

    if zoning in _INDUSTRIAL_ZONES and activation_type in ("community_garden", "block_party"):
        warnings.append(
            "Community and residential activities in industrial zones may have "
            "environmental or safety constraints. Contact the Department of "
            "Public Health Environmental Engineering unit for site-specific guidance."
        )

    if zoning in {"SP-PO-A", "SP-PO-P"}:
        warnings.append(
            "This parcel is in a Special Purpose Park/Open Space district. "
            "Additional approval from the Fairmount Park Commission or "
            "Philadelphia Parks & Recreation is likely required beyond the "
            "standard permit process."
        )

    return warnings


def get_permit_pathway(
    parcel_type: str,
    zoning: str,
    activation_type: str,
) -> dict:
    """
    Decision tree that returns the complete permit pathway for a given
    public space activation in Philadelphia.

    Parameters
    ----------
    parcel_type : str
        One of: "park", "vacant_lot", "street", "sidewalk", "plaza",
        "parking_lot"
    zoning : str
        Philadelphia zoning district code (e.g. "CMX-2", "RM-1",
        "SP-PO-A"). Pass empty string if unknown.
    activation_type : str
        One of: "event", "food_vendor", "art_installation",
        "community_garden", "pop_up_market", "performance",
        "film_shoot", "temporary_structure", "block_party",
        "sidewalk_cafe"

    Returns
    -------
    dict
        {
            "permits_required": [PermitType, ...],
            "total_timeline_days": int,
            "total_cost_range": {"min": float, "max": float},
            "steps": [
                {
                    "order": int,
                    "permit_name": str,
                    "permit_id": str,
                    "action": str,
                    "timeline_days": int,
                    "cost": {"min": float, "max": float},
                },
                ...
            ],
            "warnings": [str, ...],
        }
    """
    warnings: list[str] = []

    # -- Input validation -----------------------------------------------------
    parcel_type = parcel_type.strip().lower()
    activation_type = activation_type.strip().lower()
    zoning = zoning.strip().upper() if zoning else ""

    if parcel_type not in VALID_PARCEL_TYPES:
        raise ValueError(
            f"Invalid parcel_type '{parcel_type}'. Must be one of: "
            f"{', '.join(sorted(VALID_PARCEL_TYPES))}"
        )
    if activation_type not in VALID_ACTIVATION_TYPES:
        raise ValueError(
            f"Invalid activation_type '{activation_type}'. Must be one of: "
            f"{', '.join(sorted(VALID_ACTIVATION_TYPES))}"
        )

    # -- Look up the pathway --------------------------------------------------
    key = (activation_type, parcel_type)
    permit_ids = _PATHWAY_MATRIX.get(key, [])

    if not permit_ids:
        # Infeasible combination
        warnings.append(
            f"A '{activation_type.replace('_', ' ')}' activation on a "
            f"'{parcel_type.replace('_', ' ')}' property type is not a "
            f"standard permitted use in Philadelphia. Contact the Managing "
            f"Director's Office at (215) 686-0790 to discuss alternative "
            f"approaches or special approvals."
        )
        return {
            "permits_required": [],
            "total_timeline_days": 0,
            "total_cost_range": {"min": 0.0, "max": 0.0},
            "steps": [],
            "warnings": warnings,
        }

    permits: list[PermitType] = []
    for pid in permit_ids:
        permit = PERMIT_INDEX.get(pid)
        if permit is not None:
            permits.append(permit)

    # -- Build sequenced steps ------------------------------------------------
    # Permits are processed roughly in sequence. Some can be parallelized,
    # but for conservative timeline estimation we sequence them, with
    # certain groupings running concurrently.

    # Group permits by phase:
    #   Phase 1 -- site/land access (temporary_use, park_use, vacant_land_garden)
    #   Phase 2 -- primary activity permits (film, event, food, art, market, cafe, block_party)
    #   Phase 3 -- supporting permits (street_closure, right_of_way, encroachment, temp_structure)
    #   Phase 4 -- supplemental permits (noise_variance, commercial_activity_parks)

    _PHASE_MAP: dict[str, int] = {
        "temporary_use_permit": 1,
        "park_use_permit": 1,
        "vacant_land_garden_license": 1,
        "film_permit": 2,
        "special_event_permit": 2,
        "food_vending_permit": 2,
        "public_art_permit": 2,
        "farmers_market_permit": 2,
        "sidewalk_cafe_permit": 2,
        "block_party_permit": 2,
        "street_closure_permit": 3,
        "right_of_way_permit": 3,
        "encroachment_permit": 3,
        "temporary_structure_permit": 3,
        "noise_variance_permit": 4,
        "commercial_activity_parks_permit": 4,
    }

    # Sort permits by phase, preserving order within the same phase
    permits_by_phase: dict[int, list[PermitType]] = {}
    for p in permits:
        phase = _PHASE_MAP.get(p.id, 5)
        permits_by_phase.setdefault(phase, []).append(p)

    steps: list[dict] = []
    order = 1
    total_timeline = 0
    total_cost_min = 0.0
    total_cost_max = 0.0

    for phase_num in sorted(permits_by_phase.keys()):
        phase_permits = permits_by_phase[phase_num]

        # Within a phase, permits can be pursued concurrently.
        # Timeline = max of the permits in this phase (concurrent).
        # Cost = sum of all permits in this phase.
        phase_max_timeline = 0

        for p in phase_permits:
            action = _build_action_description(p, activation_type, parcel_type)
            steps.append({
                "order": order,
                "permit_name": p.name,
                "permit_id": p.id,
                "action": action,
                "timeline_days": p.timeline_days,
                "cost": {"min": p.cost_range["min"], "max": p.cost_range["max"]},
            })
            order += 1
            total_cost_min += p.cost_range["min"]
            total_cost_max += p.cost_range["max"]
            if p.timeline_days > phase_max_timeline:
                phase_max_timeline = p.timeline_days

        total_timeline += phase_max_timeline

    # -- Generate warnings ----------------------------------------------------
    warnings.extend(_zoning_warnings(zoning, activation_type, permits))

    # Parcel-specific warnings
    if parcel_type == "vacant_lot":
        warnings.append(
            "Vacant lots may have environmental contamination (lead, asbestos, "
            "petroleum). A Phase I Environmental Site Assessment is recommended "
            "before any public activation. Contact the Philadelphia Department "
            "of Public Health Environmental Engineering at (215) 685-7496."
        )

    if parcel_type == "park" and activation_type in ("food_vendor", "pop_up_market"):
        warnings.append(
            "Food and market activities in Philadelphia parks must not conflict "
            "with existing concession agreements managed by the Fairmount Park "
            "Conservancy. Check the concession map at myphillypark.org before "
            "applying."
        )

    if activation_type == "community_garden" and parcel_type == "vacant_lot":
        warnings.append(
            "The Philadelphia Land Bank requires community engagement through "
            "the Registered Community Organization (RCO) process. Find your "
            "RCO at phila.gov/departments/department-of-planning-and-development."
        )

    if total_timeline > 60:
        warnings.append(
            f"This activation pathway has an estimated timeline of "
            f"{total_timeline} days. Consider beginning the permit process "
            f"at least {total_timeline + 30} days before your target "
            f"activation date to account for potential delays."
        )

    # Insurance stacking warning
    insurance_permits = [p for p in permits if any("insurance" in r.lower() for r in p.requirements)]
    if len(insurance_permits) > 1:
        warnings.append(
            "Multiple permits require general liability insurance naming the "
            "City as additional insured. One policy can typically satisfy all "
            "permits -- confirm with your insurance broker that the certificate "
            "lists all required additional insureds and permit numbers."
        )

    return {
        "permits_required": permits,
        "total_timeline_days": total_timeline,
        "total_cost_range": {"min": total_cost_min, "max": total_cost_max},
        "steps": steps,
        "warnings": warnings,
    }


def _build_action_description(
    permit: PermitType,
    activation_type: str,
    parcel_type: str,
) -> str:
    """Build a human-readable action description for a permit step."""
    action_templates: dict[str, str] = {
        "film_permit": (
            "Apply for a Film Permit from the Greater Philadelphia Film "
            "Office. Submit application with insurance, location plan, and "
            "traffic management details."
        ),
        "special_event_permit": (
            "Apply for a Special Event Permit from the Managing Director's "
            "Office. Submit event plan, security plan, insurance, and site "
            "layout. Attend inter-agency meeting if over 1,000 attendees."
        ),
        "temporary_use_permit": (
            "Apply for a Temporary Use License from the Philadelphia Land "
            "Bank or Department of Public Property. Submit site plan, "
            "community support letter, and insurance documentation."
        ),
        "encroachment_permit": (
            "Apply for an Encroachment Permit from the Streets Department "
            "Right-of-Way Unit. Provide survey showing clearances and "
            "pedestrian path compliance."
        ),
        "street_closure_permit": (
            "Apply for a Street Closure Permit from the Streets Department "
            "Traffic Engineering Division. Submit traffic management plan "
            "and coordinate with SEPTA and emergency services."
        ),
        "park_use_permit": (
            "Apply for a Park Use Permit from Philadelphia Parks & "
            "Recreation. Submit activity description, attendance estimate, "
            "and site plan."
        ),
        "vacant_land_garden_license": (
            "Apply for a Community Garden License through PHS and the "
            "Philadelphia Land Bank. Form garden committee, obtain RCO "
            "support, and schedule soil testing."
        ),
        "right_of_way_permit": (
            "Apply for a Right-of-Way Occupancy Permit from the Streets "
            "Department. Provide dimensioned site plan showing occupancy "
            "area and pedestrian clearance."
        ),
        "food_vending_permit": (
            "Apply for a Food Vending Permit from the Department of Public "
            "Health and L&I. Obtain business license, pass health inspection, "
            "and secure approved vending location."
        ),
        "temporary_structure_permit": (
            "Apply for a Temporary Structure Permit from L&I. Submit "
            "engineer-stamped structural plans, fire protection plan, and "
            "insurance documentation."
        ),
        "block_party_permit": (
            "Apply for a Block Party Permit from the Streets Department. "
            "Collect signatures from 75% of block residents and submit "
            "application at least 30 days in advance."
        ),
        "farmers_market_permit": (
            "Apply for a Farmers Market Permit from the Department of "
            "Public Health and L&I. Submit market operations plan, vendor "
            "roster, and health permits for all food vendors."
        ),
        "public_art_permit": (
            "Apply for Public Art Installation approval from the "
            "Philadelphia Art Commission. Present concept at public meeting, "
            "obtain preliminary approval, then submit final design."
        ),
        "sidewalk_cafe_permit": (
            "Apply for a Sidewalk Cafe Permit from the Streets Department. "
            "Submit dimensioned site plan showing cafe layout with minimum "
            "5-foot pedestrian clearance."
        ),
        "noise_variance_permit": (
            "Apply for a Noise Variance Permit from L&I. Submit noise "
            "impact analysis and sound mitigation plan."
        ),
        "commercial_activity_parks_permit": (
            "Apply for a Commercial Activity in Parks Permit from Parks & "
            "Recreation. Submit business plan, insurance, and demonstrate "
            "no conflict with existing concessions."
        ),
    }
    return action_templates.get(
        permit.id,
        f"Apply for {permit.name} from {permit.issuing_agency}.",
    )


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def get_all_permits() -> list[dict]:
    """Return all permit types as serializable dictionaries."""
    results = []
    for p in PERMIT_TYPES:
        results.append({
            "id": p.id,
            "name": p.name,
            "issuing_agency": p.issuing_agency,
            "description": p.description,
            "application_process": p.application_process,
            "timeline_days": p.timeline_days,
            "cost_range": p.cost_range,
            "requirements": p.requirements,
            "restrictions": p.restrictions,
            "seasonal_limitations": p.seasonal_limitations,
            "applicable_zoning": p.applicable_zoning,
            "applicable_property_types": p.applicable_property_types,
        })
    return results


def get_permit_by_id(permit_id: str) -> Optional[dict]:
    """Look up a single permit type by ID."""
    p = PERMIT_INDEX.get(permit_id)
    if p is None:
        return None
    return {
        "id": p.id,
        "name": p.name,
        "issuing_agency": p.issuing_agency,
        "description": p.description,
        "application_process": p.application_process,
        "timeline_days": p.timeline_days,
        "cost_range": p.cost_range,
        "requirements": p.requirements,
        "restrictions": p.restrictions,
        "seasonal_limitations": p.seasonal_limitations,
        "applicable_zoning": p.applicable_zoning,
        "applicable_property_types": p.applicable_property_types,
    }


def search_permits(
    property_type: Optional[str] = None,
    zoning: Optional[str] = None,
    keyword: Optional[str] = None,
) -> list[dict]:
    """
    Search permits by property type, zoning district, or keyword.

    Returns matching permits as serializable dictionaries.
    """
    results = []
    for p in PERMIT_TYPES:
        # Property type filter
        if property_type and property_type.lower() not in p.applicable_property_types:
            continue

        # Zoning filter
        if zoning and zoning.upper() not in p.applicable_zoning:
            continue

        # Keyword search across name, description, and requirements
        if keyword:
            keyword_lower = keyword.lower()
            searchable = (
                p.name.lower()
                + " " + p.description.lower()
                + " " + " ".join(r.lower() for r in p.requirements)
                + " " + " ".join(r.lower() for r in p.restrictions)
            )
            if keyword_lower not in searchable:
                continue

        results.append({
            "id": p.id,
            "name": p.name,
            "issuing_agency": p.issuing_agency,
            "description": p.description,
            "timeline_days": p.timeline_days,
            "cost_range": p.cost_range,
        })

    return results


def serialize_pathway(pathway: dict) -> dict:
    """
    Convert a pathway result (from get_permit_pathway) into a fully
    JSON-serializable dictionary, converting PermitType dataclass
    instances to plain dicts.
    """
    serialized_permits = []
    for p in pathway.get("permits_required", []):
        if isinstance(p, PermitType):
            serialized_permits.append({
                "id": p.id,
                "name": p.name,
                "issuing_agency": p.issuing_agency,
                "description": p.description,
                "application_process": p.application_process,
                "timeline_days": p.timeline_days,
                "cost_range": p.cost_range,
                "requirements": p.requirements,
                "restrictions": p.restrictions,
                "seasonal_limitations": p.seasonal_limitations,
                "applicable_zoning": p.applicable_zoning,
                "applicable_property_types": p.applicable_property_types,
            })
        else:
            serialized_permits.append(p)

    return {
        "permits_required": serialized_permits,
        "total_timeline_days": pathway["total_timeline_days"],
        "total_cost_range": pathway["total_cost_range"],
        "steps": pathway["steps"],
        "warnings": pathway["warnings"],
    }
