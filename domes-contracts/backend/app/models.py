from sqlalchemy import Column, String, Integer, Boolean, Text
from app.database import Base


class Template(Base):
    """Agreement template — the blueprint for generating a specific type of legal agreement."""
    __tablename__ = "templates"

    id = Column(String, primary_key=True)
    agreement_type = Column(String, index=True)  # BAA, DUA, MOU, IDSA, QSOA, HIPAA_consent, FERPA_consent, compact, joint_funding
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    governing_laws = Column(Text, default="[]")  # JSON list
    required_provisions = Column(Text, default="[]")  # JSON list of required sections
    variable_fields = Column(Text, default="[]")  # JSON list of {{placeholder}} fields
    body_template = Column(Text, default="")  # template text with {{placeholders}}


class Agreement(Base):
    """A generated agreement — a concrete document linking two parties to close a gap."""
    __tablename__ = "agreements"

    id = Column(String, primary_key=True)
    template_id = Column(String, index=True)
    agreement_type = Column(String, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="draft")  # draft, in_review, executed
    gap_id = Column(Integer, nullable=True)  # links to domes-datamap gap
    system_a_id = Column(String, default="")
    system_b_id = Column(String, default="")
    party_a_name = Column(String, default="")
    party_b_name = Column(String, default="")
    governing_laws = Column(Text, default="[]")  # JSON
    required_signatories = Column(Text, default="[]")  # JSON
    data_elements = Column(Text, default="[]")  # JSON: what data will be shared
    privacy_provisions = Column(Text, default="[]")  # JSON
    key_terms = Column(Text, default="[]")  # JSON
    body_text = Column(Text, default="")  # rendered agreement text
    compliance_status = Column(String, default="unchecked")  # valid, issues_found, unchecked
    compliance_flags = Column(Text, default="[]")  # JSON
    created_at = Column(String, default="")
    updated_at = Column(String, default="")


class ComplianceRule(Base):
    """A regulatory requirement that agreements must satisfy."""
    __tablename__ = "compliance_rules"

    id = Column(String, primary_key=True)
    law = Column(String, index=True)  # HIPAA, 42_CFR_Part_2, FERPA, CJIS, state
    requirement = Column(String, nullable=False)
    description = Column(Text, default="")
    applies_to = Column(Text, default="[]")  # JSON: which agreement types
    severity = Column(String, default="required")  # required, recommended
    provision_text = Column(Text, default="")  # model language to include


class ConsentForm(Base):
    """A person-authorizable consent form to close a specific gap."""
    __tablename__ = "consent_forms"

    id = Column(String, primary_key=True)
    gap_id = Column(Integer, nullable=True)
    consent_type = Column(String, index=True)  # HIPAA_authorization, CFR42_consent, FERPA_release, general_release
    title = Column(String, nullable=False)
    governing_law = Column(String, default="")
    description = Column(Text, default="")
    body_text = Column(Text, default="")
    required_fields = Column(Text, default="[]")  # JSON: fields the person must fill
    status = Column(String, default="draft")  # draft, ready
    created_at = Column(String, default="")
