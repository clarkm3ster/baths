"""Seed data: agreement templates, compliance rules, and consent form templates.

Every gap from domes-datamap has a legal pathway to close it.
This seeds the template library and compliance framework.
"""

import json
from sqlalchemy.orm import Session
from app.models import Template, ComplianceRule, ConsentForm


def seed_all(db: Session) -> dict[str, int]:
    if db.query(Template).count() > 0:
        return {"templates": 0, "rules": 0, "consent_forms": 0}

    templates = _seed_templates(db)
    rules = _seed_compliance_rules(db)
    consent_forms = _seed_consent_forms(db)
    db.commit()
    return {"templates": templates, "rules": rules, "consent_forms": consent_forms}


def _j(lst: list) -> str:
    return json.dumps(lst)


# ---------------------------------------------------------------------------
# AGREEMENT TEMPLATES
# ---------------------------------------------------------------------------

def _seed_templates(db: Session) -> int:
    templates = [
        Template(
            id="tpl_baa",
            agreement_type="BAA",
            name="Business Associate Agreement",
            description="Required under HIPAA when a covered entity shares protected health information (PHI) with a business associate. Establishes permitted uses, safeguards, breach notification, and termination provisions.",
            governing_laws=_j(["HIPAA", "HITECH Act", "45 CFR Part 160", "45 CFR Part 164"]),
            required_provisions=_j([
                "Permitted uses and disclosures of PHI",
                "Safeguards to prevent unauthorized use or disclosure",
                "Breach notification requirements",
                "Individual rights (access, amendment, accounting)",
                "Return or destruction of PHI upon termination",
                "Subcontractor requirements",
                "Term and termination provisions"
            ]),
            variable_fields=_j([
                "covered_entity_name", "business_associate_name",
                "effective_date", "permitted_uses", "data_elements",
                "safeguard_requirements", "breach_notification_timeline",
                "term_length", "governing_state"
            ]),
            body_template="""BUSINESS ASSOCIATE AGREEMENT

This Business Associate Agreement ("Agreement") is entered into as of {{effective_date}} by and between:

COVERED ENTITY: {{covered_entity_name}} ("Covered Entity")
BUSINESS ASSOCIATE: {{business_associate_name}} ("Business Associate")

RECITALS

WHEREAS, Covered Entity and Business Associate desire to enter into an arrangement whereby Business Associate will provide services involving the use or disclosure of Protected Health Information ("PHI") as defined by the Health Insurance Portability and Accountability Act of 1996 ("HIPAA"), as amended by the Health Information Technology for Economic and Clinical Health Act ("HITECH Act");

WHEREAS, Covered Entity and Business Associate intend to protect the privacy and provide for the security of PHI in compliance with HIPAA, the HITECH Act, and their implementing regulations at 45 CFR Parts 160 and 164;

NOW, THEREFORE, in consideration of the mutual promises and covenants herein, the parties agree as follows:

ARTICLE I — DEFINITIONS

Terms used but not otherwise defined in this Agreement shall have the same meaning as those terms in the HIPAA Rules (45 CFR Parts 160 and 164).

1.1 "Breach" means the acquisition, access, use, or disclosure of PHI in a manner not permitted under the Privacy Rule that compromises the security or privacy of the PHI, as defined in 45 CFR § 164.402.

1.2 "Protected Health Information" or "PHI" means individually identifiable health information transmitted or maintained in any form or medium, as defined in 45 CFR § 160.103.

ARTICLE II — OBLIGATIONS OF BUSINESS ASSOCIATE

2.1 Permitted Uses and Disclosures. Business Associate may use or disclose PHI only as follows:
{{permitted_uses}}

2.2 Data Elements. The PHI subject to this Agreement includes:
{{data_elements}}

2.3 Safeguards. Business Associate shall implement administrative, physical, and technical safeguards that reasonably and appropriately protect the confidentiality, integrity, and availability of PHI, including:
{{safeguard_requirements}}

2.4 Reporting. Business Associate shall report to Covered Entity any use or disclosure of PHI not provided for by this Agreement of which it becomes aware, including any Breach of Unsecured PHI, without unreasonable delay and in no case later than {{breach_notification_timeline}} calendar days after discovery.

2.5 Subcontractors. Business Associate shall ensure that any subcontractor that creates, receives, maintains, or transmits PHI on behalf of Business Associate agrees in writing to the same restrictions and conditions that apply to Business Associate.

2.6 Access. Business Associate shall make PHI available to individuals in accordance with 45 CFR § 164.524.

2.7 Amendment. Business Associate shall make PHI available for amendment and incorporate amendments in accordance with 45 CFR § 164.526.

2.8 Accounting of Disclosures. Business Associate shall make available information required to provide an accounting of disclosures in accordance with 45 CFR § 164.528.

ARTICLE III — TERM AND TERMINATION

3.1 Term. This Agreement shall be effective as of {{effective_date}} and shall remain in effect for {{term_length}}, unless terminated earlier as provided herein.

3.2 Termination for Cause. Covered Entity may terminate this Agreement if Covered Entity determines that Business Associate has violated a material term of this Agreement.

3.3 Effect of Termination. Upon termination, Business Associate shall return or destroy all PHI received from, or created or received by Business Associate on behalf of, Covered Entity.

ARTICLE IV — GENERAL PROVISIONS

4.1 Governing Law. This Agreement shall be governed by the laws of the State of {{governing_state}} and applicable federal law.

4.2 Amendment. This Agreement may not be amended except by written agreement signed by both parties.

4.3 Survival. The obligations of Business Associate under Article III, Section 3.3, shall survive termination of this Agreement.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

COVERED ENTITY: {{covered_entity_name}}
By: ________________________________
Name:
Title:
Date:

BUSINESS ASSOCIATE: {{business_associate_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
        Template(
            id="tpl_dua",
            agreement_type="DUA",
            name="Data Use Agreement",
            description="Governs the sharing of limited data sets or de-identified data between organizations. Required under HIPAA for limited data set disclosures and commonly used for research and public health purposes.",
            governing_laws=_j(["HIPAA", "45 CFR § 164.514(e)", "state privacy laws"]),
            required_provisions=_j([
                "Permitted uses of the data",
                "Limitations on who can use or receive data",
                "Prohibition on re-identification",
                "Safeguards for data protection",
                "Reporting of unauthorized use",
                "Term and termination"
            ]),
            variable_fields=_j([
                "data_provider_name", "data_recipient_name",
                "effective_date", "data_description", "permitted_purposes",
                "security_requirements", "term_length", "governing_state"
            ]),
            body_template="""DATA USE AGREEMENT

This Data Use Agreement ("Agreement") is entered into as of {{effective_date}} by and between:

DATA PROVIDER: {{data_provider_name}} ("Provider")
DATA RECIPIENT: {{data_recipient_name}} ("Recipient")

RECITALS

WHEREAS, Provider maintains data that Recipient seeks to use for {{permitted_purposes}};

WHEREAS, the parties wish to establish the terms under which such data will be shared, used, and protected;

ARTICLE I — DATA DESCRIPTION

1.1 The data subject to this Agreement includes:
{{data_description}}

1.2 Provider shall remove the following direct identifiers before disclosure: names, postal addresses (other than town/city, state, and zip code), telephone numbers, fax numbers, email addresses, Social Security numbers, medical record numbers, health plan beneficiary numbers, account numbers, certificate/license numbers, vehicle identifiers and serial numbers, device identifiers, web URLs, IP addresses, biometric identifiers, full-face photographs, and any other unique identifying number, characteristic, or code.

ARTICLE II — PERMITTED USES

2.1 Recipient may use or disclose the data ONLY for:
{{permitted_purposes}}

2.2 Recipient shall NOT use or disclose the data for any other purpose.

2.3 Recipient shall NOT attempt to identify or contact individuals whose data is included in the data set.

2.4 Recipient shall NOT re-identify the data or use the data in combination with other data to identify individuals.

ARTICLE III — SAFEGUARDS

3.1 Recipient shall implement the following safeguards:
{{security_requirements}}

3.2 Recipient shall limit access to the data to those persons who need access to accomplish the permitted uses.

3.3 Recipient shall report to Provider any unauthorized use or disclosure of the data within 10 business days of discovery.

ARTICLE IV — TERM AND TERMINATION

4.1 This Agreement is effective as of {{effective_date}} for a period of {{term_length}}.

4.2 Either party may terminate upon 30 days written notice.

4.3 Upon termination, Recipient shall return or destroy all data received under this Agreement.

ARTICLE V — GENERAL PROVISIONS

5.1 Governing Law. State of {{governing_state}} and applicable federal law.

5.2 No third-party beneficiaries. This Agreement does not create rights in any third party.

IN WITNESS WHEREOF:

DATA PROVIDER: {{data_provider_name}}
By: ________________________________
Name:
Title:
Date:

DATA RECIPIENT: {{data_recipient_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
        Template(
            id="tpl_mou",
            agreement_type="MOU",
            name="Memorandum of Understanding",
            description="Establishes a framework for interagency cooperation and data sharing. Less formal than a contract but creates documented expectations for how agencies will work together to share information and coordinate services.",
            governing_laws=_j(["Varies by jurisdiction and agencies involved"]),
            required_provisions=_j([
                "Purpose and scope of cooperation",
                "Roles and responsibilities of each party",
                "Data sharing provisions",
                "Privacy and confidentiality protections",
                "Dispute resolution",
                "Duration and review schedule"
            ]),
            variable_fields=_j([
                "agency_a_name", "agency_b_name", "effective_date",
                "purpose", "scope", "data_to_share", "responsibilities_a",
                "responsibilities_b", "privacy_protections", "review_period",
                "term_length", "governing_state"
            ]),
            body_template="""MEMORANDUM OF UNDERSTANDING

Between {{agency_a_name}} and {{agency_b_name}}

Effective Date: {{effective_date}}

I. PURPOSE

This Memorandum of Understanding ("MOU") establishes a framework for cooperation between {{agency_a_name}} ("Agency A") and {{agency_b_name}} ("Agency B") for the purpose of:

{{purpose}}

II. SCOPE

This MOU covers the following activities and information sharing:
{{scope}}

III. DATA SHARING

3.1 The parties agree to share the following data elements, subject to applicable privacy laws:
{{data_to_share}}

3.2 All data sharing shall comply with applicable federal and state privacy laws including but not limited to HIPAA, FERPA, 42 CFR Part 2, and the Privacy Act, as applicable.

IV. ROLES AND RESPONSIBILITIES

4.1 {{agency_a_name}} shall:
{{responsibilities_a}}

4.2 {{agency_b_name}} shall:
{{responsibilities_b}}

V. PRIVACY AND CONFIDENTIALITY

5.1 Both parties shall:
{{privacy_protections}}

5.2 Neither party shall disclose shared information to any third party without the prior written consent of the providing party, except as required by law.

VI. GOVERNANCE

6.1 The parties shall designate a liaison from each agency to oversee implementation.

6.2 The parties shall meet at least {{review_period}} to review the effectiveness of this MOU.

6.3 Disputes shall be resolved through good-faith negotiation between agency leadership.

VII. TERM

7.1 This MOU is effective as of {{effective_date}} for a period of {{term_length}}.

7.2 Either party may terminate upon 60 days written notice.

7.3 This MOU may be renewed by mutual written agreement.

VIII. GENERAL

8.1 This MOU does not create any legally enforceable obligations or transfer of funds.

8.2 Governed by the laws of the State of {{governing_state}}.

8.3 Nothing in this MOU shall be construed to supersede applicable federal or state law.

SIGNATURES:

{{agency_a_name}}
By: ________________________________
Name:
Title:
Date:

{{agency_b_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
        Template(
            id="tpl_idsa",
            agreement_type="IDSA",
            name="Interagency Data Sharing Agreement",
            description="A formal agreement between government agencies to share specific data for defined purposes. More detailed and enforceable than an MOU, with specific data elements, security requirements, and compliance obligations.",
            governing_laws=_j(["HIPAA", "Privacy Act", "state data sharing statutes"]),
            required_provisions=_j([
                "Specific data elements to be shared",
                "Legal authority for sharing",
                "Purpose and use limitations",
                "Security and technical requirements",
                "Individual rights and redress",
                "Audit and oversight provisions",
                "Breach notification procedures",
                "Term and termination"
            ]),
            variable_fields=_j([
                "agency_a_name", "agency_b_name", "effective_date",
                "legal_authority", "purpose", "data_elements_a_to_b",
                "data_elements_b_to_a", "transmission_method",
                "security_requirements", "audit_frequency",
                "breach_notification_timeline", "term_length", "governing_state"
            ]),
            body_template="""INTERAGENCY DATA SHARING AGREEMENT

This Interagency Data Sharing Agreement ("Agreement") is entered into by and between:

AGENCY A: {{agency_a_name}}
AGENCY B: {{agency_b_name}}

Effective Date: {{effective_date}}

I. LEGAL AUTHORITY

This Agreement is entered into pursuant to:
{{legal_authority}}

II. PURPOSE

The purpose of this data sharing is:
{{purpose}}

The parties shall not use shared data for any purpose not specified herein.

III. DATA ELEMENTS

3.1 {{agency_a_name}} shall provide to {{agency_b_name}}:
{{data_elements_a_to_b}}

3.2 {{agency_b_name}} shall provide to {{agency_a_name}}:
{{data_elements_b_to_a}}

3.3 Data shall not include information beyond what is minimally necessary for the stated purpose.

IV. TRANSMISSION AND SECURITY

4.1 Data shall be transmitted via:
{{transmission_method}}

4.2 Both parties shall implement the following security measures:
{{security_requirements}}

4.3 Access to shared data shall be limited to personnel with a documented need-to-know.

4.4 Each party shall maintain an audit log of all access to shared data.

V. INDIVIDUAL RIGHTS

5.1 Individuals whose data is shared under this Agreement retain all rights provided by applicable law, including the right to access, correct, and request accounting of disclosures.

5.2 Each party shall establish a process for individuals to exercise these rights.

VI. AUDIT AND OVERSIGHT

6.1 Each party may audit the other's compliance with this Agreement {{audit_frequency}}.

6.2 Each party shall designate a Data Sharing Officer responsible for compliance.

VII. BREACH NOTIFICATION

7.1 Each party shall notify the other of any breach of shared data within {{breach_notification_timeline}} hours of discovery.

7.2 The party responsible for the breach shall bear costs of notification and remediation.

VIII. TERM AND TERMINATION

8.1 Effective for {{term_length}} from {{effective_date}}.

8.2 Either party may terminate upon 90 days written notice.

8.3 Upon termination, each party shall return or securely destroy data received from the other party.

IX. GENERAL PROVISIONS

9.1 Governed by the laws of the State of {{governing_state}} and applicable federal law.

9.2 This Agreement may be amended only by written agreement signed by authorized representatives.

SIGNATURES:

{{agency_a_name}}
By: ________________________________
Name:
Title:
Date:

{{agency_b_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
        Template(
            id="tpl_qsoa",
            agreement_type="QSOA",
            name="Qualified Service Organization Agreement",
            description="Required under 42 CFR Part 2 when a substance use disorder (SUD) treatment program shares patient identifying information with an outside organization providing services to the program. More restrictive than a BAA.",
            governing_laws=_j(["42 CFR Part 2", "HIPAA", "SAMHSA guidelines"]),
            required_provisions=_j([
                "Acknowledgment of 42 CFR Part 2 restrictions",
                "Prohibition on re-disclosure",
                "Permitted services",
                "Patient notice requirements",
                "Criminal penalties for violations",
                "Termination for non-compliance"
            ]),
            variable_fields=_j([
                "program_name", "qso_name", "effective_date",
                "services_provided", "patient_information_shared",
                "term_length", "governing_state"
            ]),
            body_template="""QUALIFIED SERVICE ORGANIZATION AGREEMENT

This Qualified Service Organization Agreement ("Agreement") is entered into as of {{effective_date}} by and between:

PROGRAM: {{program_name}} ("Program") — a substance use disorder treatment program subject to 42 CFR Part 2
QUALIFIED SERVICE ORGANIZATION: {{qso_name}} ("QSO")

RECITALS

WHEREAS, Program provides substance use disorder diagnosis, treatment, or referral for treatment;

WHEREAS, QSO provides services to Program that require access to patient identifying information;

WHEREAS, 42 CFR § 2.12(c)(4) permits disclosure of patient identifying information to a qualified service organization without patient consent, provided this Agreement is executed;

ARTICLE I — SERVICES

1.1 QSO shall provide the following services to Program:
{{services_provided}}

1.2 In connection with these services, Program may disclose the following patient information to QSO:
{{patient_information_shared}}

ARTICLE II — 42 CFR PART 2 OBLIGATIONS

2.1 QSO acknowledges that in receiving, storing, processing, or otherwise dealing with any patient identifying information from Program, QSO is fully bound by the provisions of 42 CFR Part 2.

2.2 QSO shall NOT re-disclose any patient identifying information received from Program to any person or entity not authorized under 42 CFR Part 2.

2.3 QSO understands that federal law (42 U.S.C. § 290dd-2) makes violation of 42 CFR Part 2 a criminal offense. Any person who violates any provision of the statute or regulations shall be fined not more than $500 in the case of a first offense, and not more than $5,000 in the case of each subsequent offense.

2.4 The following notice applies to all information shared under this Agreement:

"This information has been disclosed to you from records protected by federal confidentiality rules (42 CFR Part 2). The federal rules prohibit you from making any further disclosure of information in this record that identifies a patient as having or having had a substance use disorder either directly, by reference to publicly available information, or through verification of such identification by another person unless further disclosure is expressly permitted by the written consent of the individual whose information is being disclosed or as otherwise permitted by 42 CFR Part 2. A general authorization for the release of medical or other information is NOT sufficient for this purpose (see § 2.31). The federal rules restrict any use of the information to investigate or prosecute with regard to a crime any patient with a substance use disorder, except as provided at §§ 2.12(c)(5) and 2.65."

ARTICLE III — TERM AND TERMINATION

3.1 Effective for {{term_length}} from {{effective_date}}.

3.2 Program may terminate immediately if QSO violates any provision of 42 CFR Part 2.

3.3 Upon termination, QSO shall return or destroy all patient identifying information.

ARTICLE IV — GENERAL

4.1 Governed by federal law (42 CFR Part 2) and the laws of the State of {{governing_state}}.

SIGNATURES:

PROGRAM: {{program_name}}
By: ________________________________
Name:
Title:
Date:

QUALIFIED SERVICE ORGANIZATION: {{qso_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
        Template(
            id="tpl_hipaa_consent",
            agreement_type="HIPAA_consent",
            name="HIPAA Authorization for Disclosure",
            description="Individual authorization for the release of protected health information under HIPAA. Required when a covered entity discloses PHI for purposes not covered by the treatment, payment, or operations exceptions.",
            governing_laws=_j(["HIPAA", "45 CFR § 164.508"]),
            required_provisions=_j([
                "Specific description of information to be disclosed",
                "Name of person/entity authorized to make disclosure",
                "Name of person/entity authorized to receive information",
                "Purpose of disclosure",
                "Expiration date or event",
                "Right to revoke",
                "Consequences of refusal to sign",
                "Re-disclosure notice"
            ]),
            variable_fields=_j([
                "patient_name", "dob", "disclosing_entity",
                "receiving_entity", "information_description",
                "purpose", "expiration_date"
            ]),
            body_template="""AUTHORIZATION FOR DISCLOSURE OF PROTECTED HEALTH INFORMATION

Patient Name: {{patient_name}}
Date of Birth: {{dob}}

I hereby authorize the following disclosure of my protected health information:

1. ENTITY AUTHORIZED TO DISCLOSE:
{{disclosing_entity}}

2. ENTITY AUTHORIZED TO RECEIVE:
{{receiving_entity}}

3. INFORMATION TO BE DISCLOSED:
{{information_description}}

4. PURPOSE OF DISCLOSURE:
{{purpose}}

5. EXPIRATION:
This authorization expires on {{expiration_date}} or upon the following event: ________________

6. YOUR RIGHTS:
- You have the right to revoke this authorization at any time by submitting a written request to the disclosing entity. Revocation will not apply to information already disclosed in reliance on this authorization.
- You are not required to sign this authorization. Your treatment, payment, enrollment, or eligibility for benefits will NOT be conditioned on signing this authorization, unless the authorization is for research-related treatment.
- Information disclosed pursuant to this authorization may be subject to re-disclosure by the recipient and may no longer be protected by federal privacy law.

7. RE-DISCLOSURE NOTICE:
Information disclosed pursuant to this authorization may be re-disclosed by the recipient and may no longer be protected by HIPAA.

SIGNATURE:

Patient/Authorized Representative: ________________________________
Printed Name: {{patient_name}}
Date: ________________

If signed by authorized representative:
Representative Name: ________________
Relationship to Patient: ________________
Authority to Act: ________________""",
        ),
        Template(
            id="tpl_ferpa_consent",
            agreement_type="FERPA_consent",
            name="FERPA Consent for Disclosure of Education Records",
            description="Parental or eligible student consent for the release of education records under the Family Educational Rights and Privacy Act. Required for any disclosure not covered by FERPA exceptions.",
            governing_laws=_j(["FERPA", "20 U.S.C. § 1232g", "34 CFR Part 99"]),
            required_provisions=_j([
                "Identification of records to be disclosed",
                "Purpose of disclosure",
                "Parties to whom disclosure will be made",
                "Parent/eligible student signature",
                "Date"
            ]),
            variable_fields=_j([
                "student_name", "student_dob", "school_name",
                "records_description", "receiving_party",
                "purpose", "expiration_date"
            ]),
            body_template="""CONSENT FOR DISCLOSURE OF EDUCATION RECORDS
(Family Educational Rights and Privacy Act — FERPA)

Student Name: {{student_name}}
Date of Birth: {{student_dob}}
School/District: {{school_name}}

I, the undersigned parent/guardian/eligible student, hereby consent to the disclosure of the following education records:

1. RECORDS TO BE DISCLOSED:
{{records_description}}

2. DISCLOSED TO:
{{receiving_party}}

3. PURPOSE OF DISCLOSURE:
{{purpose}}

4. EXPIRATION:
This consent expires on {{expiration_date}} or upon the following event: ________________

5. YOUR RIGHTS UNDER FERPA:
- You have the right to inspect and review your child's education records.
- You have the right to request amendment of records you believe are inaccurate.
- You have the right to consent to disclosure of personally identifiable information from education records, except to the extent FERPA authorizes disclosure without consent.
- You have the right to file a complaint with the U.S. Department of Education concerning alleged failures to comply with FERPA.
- This consent is voluntary. You are not required to sign this form.
- You may revoke this consent at any time by providing written notice to the school.

SIGNATURE:

Parent/Guardian/Eligible Student: ________________________________
Printed Name: ________________
Relationship to Student (if parent/guardian): ________________
Date: ________________""",
        ),
        Template(
            id="tpl_42cfr_consent",
            agreement_type="42CFR_consent",
            name="42 CFR Part 2 Consent for Disclosure of SUD Records",
            description="Patient consent for the disclosure of substance use disorder treatment records. Required by federal law (42 CFR Part 2) for any disclosure of SUD patient identifying information, with specific required elements that exceed HIPAA requirements.",
            governing_laws=_j(["42 CFR Part 2", "42 U.S.C. § 290dd-2", "SAMHSA guidance"]),
            required_provisions=_j([
                "Name of patient",
                "Specific name or general designation of program making disclosure",
                "How much and what kind of information to be disclosed",
                "Name of individual or entity to receive disclosure",
                "Purpose of disclosure",
                "Statement of right to revoke",
                "Expiration date, event, or condition",
                "Signature of patient",
                "Date signed",
                "Re-disclosure prohibition notice"
            ]),
            variable_fields=_j([
                "patient_name", "dob", "program_name",
                "receiving_entity", "information_description",
                "purpose", "expiration_date"
            ]),
            body_template="""CONSENT FOR DISCLOSURE OF SUBSTANCE USE DISORDER TREATMENT RECORDS
(42 CFR Part 2)

Patient Name: {{patient_name}}
Date of Birth: {{dob}}

I, {{patient_name}}, hereby authorize:

1. FROM (name or general designation of program):
{{program_name}}

2. TO (name of individual or organization):
{{receiving_entity}}

3. INFORMATION TO BE DISCLOSED:
{{information_description}}

4. PURPOSE OF DISCLOSURE:
{{purpose}}

5. EXPIRATION:
This consent expires on {{expiration_date}} unless revoked earlier.

6. RIGHT TO REVOKE:
I understand that I may revoke this consent at any time, except to the extent that action has been taken in reliance on it. To revoke, I must provide written notice to the program listed above.

7. I understand that my records are protected under the federal regulations governing Confidentiality of Substance Use Disorder Patient Records, 42 CFR Part 2, and cannot be disclosed without my written consent unless otherwise provided for in the regulations.

8. I understand that I may refuse to sign this consent and that my treatment, payment, enrollment, or eligibility for benefits may not be conditioned upon whether I sign this consent.

9. I understand that any disclosure made pursuant to this consent is bound by the following notice:

"This information has been disclosed to you from records protected by federal confidentiality rules (42 CFR Part 2). The federal rules prohibit you from making any further disclosure of information in this record that identifies a patient as having or having had a substance use disorder either directly, by reference to publicly available information, or through verification of such identification by another person unless further disclosure is expressly permitted by the written consent of the individual whose information is being disclosed or as otherwise permitted by 42 CFR Part 2. A general authorization for the release of medical or other information is NOT sufficient for this purpose (see § 2.31). The federal rules restrict any use of the information to investigate or prosecute with regard to a crime any patient with a substance use disorder, except as provided at §§ 2.12(c)(5) and 2.65."

SIGNATURE:

Patient: ________________________________
Printed Name: {{patient_name}}
Date: ________________""",
        ),
        Template(
            id="tpl_compact",
            agreement_type="compact",
            name="Intergovernmental Compact",
            description="A formal agreement between government entities (state, county, municipal) to cooperate in delivering services and sharing data across jurisdictional boundaries. Typically requires legislative or executive authorization.",
            governing_laws=_j(["State intergovernmental cooperation statutes", "applicable federal law"]),
            required_provisions=_j([
                "Parties and jurisdictions",
                "Purpose and scope",
                "Governance structure",
                "Funding and cost sharing",
                "Data sharing provisions",
                "Privacy protections",
                "Dispute resolution",
                "Amendment and withdrawal"
            ]),
            variable_fields=_j([
                "government_a_name", "government_b_name", "effective_date",
                "purpose", "scope", "governance_structure", "funding_arrangement",
                "data_provisions", "privacy_protections", "term_length",
                "governing_state"
            ]),
            body_template="""INTERGOVERNMENTAL COMPACT

This Intergovernmental Compact ("Compact") is entered into by and between:

{{government_a_name}} ("Party A")
{{government_b_name}} ("Party B")

Effective Date: {{effective_date}}

ARTICLE I — PURPOSE

{{purpose}}

ARTICLE II — SCOPE

{{scope}}

ARTICLE III — GOVERNANCE

3.1 The parties shall establish a joint oversight body consisting of designated representatives from each party.

3.2 Governance structure:
{{governance_structure}}

ARTICLE IV — FUNDING

{{funding_arrangement}}

ARTICLE V — DATA SHARING

5.1 The parties agree to share data as follows:
{{data_provisions}}

5.2 All data sharing shall comply with applicable federal and state privacy laws.

ARTICLE VI — PRIVACY PROTECTIONS

{{privacy_protections}}

ARTICLE VII — TERM AND WITHDRAWAL

7.1 This Compact is effective for {{term_length}} from {{effective_date}}.

7.2 Any party may withdraw upon 180 days written notice.

7.3 Withdrawal does not affect obligations incurred prior to the effective date of withdrawal.

ARTICLE VIII — DISPUTE RESOLUTION

8.1 Disputes shall be resolved through negotiation, then mediation, then binding arbitration.

ARTICLE IX — GENERAL

9.1 Governed by the laws of the State of {{governing_state}}.

9.2 This Compact does not waive sovereign immunity.

SIGNATURES:

{{government_a_name}}
By: ________________________________
Name:
Title:
Date:

{{government_b_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
        Template(
            id="tpl_joint_funding",
            agreement_type="joint_funding",
            name="Joint Funding Agreement",
            description="Agreement for multiple agencies to pool resources to fund shared infrastructure, services, or technology that enables cross-system coordination. Addresses cost allocation, deliverables, and accountability.",
            governing_laws=_j(["State procurement law", "OMB Uniform Guidance (2 CFR Part 200)", "applicable federal grant requirements"]),
            required_provisions=_j([
                "Funding commitments by party",
                "Deliverables and milestones",
                "Cost allocation methodology",
                "Reporting and accountability",
                "Audit rights",
                "Intellectual property ownership",
                "Term and termination"
            ]),
            variable_fields=_j([
                "agency_a_name", "agency_b_name", "effective_date",
                "project_description", "funding_a_amount", "funding_b_amount",
                "total_budget", "deliverables", "timeline",
                "reporting_requirements", "ip_ownership", "term_length",
                "governing_state"
            ]),
            body_template="""JOINT FUNDING AGREEMENT

This Joint Funding Agreement ("Agreement") is entered into by and between:

{{agency_a_name}} ("Agency A")
{{agency_b_name}} ("Agency B")

Effective Date: {{effective_date}}

I. PROJECT DESCRIPTION

{{project_description}}

II. FUNDING COMMITMENTS

2.1 {{agency_a_name}} commits: {{funding_a_amount}}
2.2 {{agency_b_name}} commits: {{funding_b_amount}}
2.3 Total project budget: {{total_budget}}

III. DELIVERABLES

{{deliverables}}

IV. TIMELINE

{{timeline}}

V. REPORTING AND ACCOUNTABILITY

{{reporting_requirements}}

VI. AUDIT

6.1 Each party shall have the right to audit expenditures related to this Agreement.

6.2 Records shall be maintained for 5 years after Agreement termination.

VII. INTELLECTUAL PROPERTY

{{ip_ownership}}

VIII. TERM

8.1 Effective for {{term_length}} from {{effective_date}}.

8.2 Either party may terminate upon 90 days written notice, subject to outstanding financial obligations.

IX. GENERAL

9.1 Governed by the laws of the State of {{governing_state}}.

SIGNATURES:

{{agency_a_name}}
By: ________________________________
Name:
Title:
Date:

{{agency_b_name}}
By: ________________________________
Name:
Title:
Date:""",
        ),
    ]

    for t in templates:
        db.add(t)
    db.flush()
    return len(templates)


# ---------------------------------------------------------------------------
# COMPLIANCE RULES
# ---------------------------------------------------------------------------

def _seed_compliance_rules(db: Session) -> int:
    rules = [
        # HIPAA rules
        ComplianceRule(
            id="hipaa_baa_required",
            law="HIPAA",
            requirement="BAA must be in place before sharing PHI with business associates",
            description="45 CFR § 164.502(e) requires covered entities to obtain satisfactory assurances from business associates that they will appropriately safeguard PHI.",
            applies_to=_j(["BAA"]),
            severity="required",
            provision_text="Business Associate agrees to implement appropriate safeguards as required by 45 CFR § 164.502(e).",
        ),
        ComplianceRule(
            id="hipaa_minimum_necessary",
            law="HIPAA",
            requirement="Only minimum necessary PHI may be disclosed",
            description="45 CFR § 164.502(b) — covered entities must make reasonable efforts to limit PHI to the minimum necessary to accomplish the intended purpose.",
            applies_to=_j(["BAA", "DUA", "IDSA"]),
            severity="required",
            provision_text="Disclosures shall be limited to the minimum necessary information to accomplish the stated purpose.",
        ),
        ComplianceRule(
            id="hipaa_breach_notification",
            law="HIPAA",
            requirement="Breach notification within 60 days",
            description="45 CFR § 164.404 — covered entity must notify affected individuals within 60 days of discovering a breach of unsecured PHI.",
            applies_to=_j(["BAA", "DUA", "IDSA"]),
            severity="required",
            provision_text="In the event of a breach of unsecured PHI, notification shall be provided in accordance with 45 CFR § 164.404, within 60 days of discovery.",
        ),
        ComplianceRule(
            id="hipaa_authorization_elements",
            law="HIPAA",
            requirement="Authorization must contain all required elements per 45 CFR § 164.508",
            description="A valid HIPAA authorization must include: description of information, who may disclose, who may receive, purpose, expiration, right to revoke, signature, and date.",
            applies_to=_j(["HIPAA_consent"]),
            severity="required",
            provision_text="This authorization contains all elements required by 45 CFR § 164.508(c).",
        ),
        ComplianceRule(
            id="hipaa_right_to_revoke",
            law="HIPAA",
            requirement="Individual right to revoke authorization",
            description="45 CFR § 164.508(b)(5) — individual must be informed of right to revoke authorization in writing.",
            applies_to=_j(["HIPAA_consent"]),
            severity="required",
            provision_text="You have the right to revoke this authorization at any time by submitting a written request.",
        ),

        # 42 CFR Part 2 rules
        ComplianceRule(
            id="cfr42_consent_elements",
            law="42 CFR Part 2",
            requirement="Consent must contain all elements per § 2.31",
            description="42 CFR § 2.31 requires: patient name, specific program name, how much/what kind of information, recipient name, purpose, right to revoke, expiration, signature, date.",
            applies_to=_j(["42CFR_consent", "QSOA"]),
            severity="required",
            provision_text="This consent contains all elements required by 42 CFR § 2.31.",
        ),
        ComplianceRule(
            id="cfr42_redisclosure_notice",
            law="42 CFR Part 2",
            requirement="Re-disclosure prohibition notice must accompany all disclosures",
            description="42 CFR § 2.32 — any disclosure must be accompanied by the written prohibition on re-disclosure statement.",
            applies_to=_j(["42CFR_consent", "QSOA"]),
            severity="required",
            provision_text="This information has been disclosed from records protected by federal confidentiality rules (42 CFR Part 2). The federal rules prohibit you from making any further disclosure of this information unless further disclosure is expressly permitted by the written consent of the person to whom it pertains or as otherwise permitted by 42 CFR Part 2.",
        ),
        ComplianceRule(
            id="cfr42_no_general_auth",
            law="42 CFR Part 2",
            requirement="General medical authorization is NOT sufficient",
            description="42 CFR § 2.31 — a general authorization for release of medical or other information is NOT sufficient to authorize disclosure of SUD records.",
            applies_to=_j(["42CFR_consent"]),
            severity="required",
            provision_text="A general authorization for the release of medical or other information is NOT sufficient for this purpose (see § 2.31).",
        ),
        ComplianceRule(
            id="cfr42_criminal_penalty",
            law="42 CFR Part 2",
            requirement="Criminal penalties for unauthorized disclosure",
            description="42 U.S.C. § 290dd-2 — violation is a criminal offense: up to $500 first offense, $5,000 subsequent offenses.",
            applies_to=_j(["42CFR_consent", "QSOA"]),
            severity="required",
            provision_text="Violation of 42 CFR Part 2 is a federal criminal offense punishable by fine.",
        ),

        # FERPA rules
        ComplianceRule(
            id="ferpa_consent_required",
            law="FERPA",
            requirement="Written consent required before disclosing education records",
            description="34 CFR § 99.30 — requires written consent from parent (or eligible student 18+) before disclosing personally identifiable information from education records.",
            applies_to=_j(["FERPA_consent"]),
            severity="required",
            provision_text="Disclosure requires prior written consent of the parent or eligible student in accordance with 34 CFR § 99.30.",
        ),
        ComplianceRule(
            id="ferpa_consent_elements",
            law="FERPA",
            requirement="Consent must specify records, purpose, and parties",
            description="34 CFR § 99.30(b) — consent must be signed and dated, specify records to be disclosed, state purpose, and identify parties to whom disclosure will be made.",
            applies_to=_j(["FERPA_consent"]),
            severity="required",
            provision_text="This consent specifies the records to be disclosed, the purpose, and the recipient, as required by 34 CFR § 99.30(b).",
        ),

        # CJIS rules
        ComplianceRule(
            id="cjis_security_policy",
            law="CJIS",
            requirement="Must comply with FBI CJIS Security Policy",
            description="Any entity accessing criminal justice information must comply with the CJIS Security Policy, including background checks, encryption, and audit requirements.",
            applies_to=_j(["IDSA", "MOU"]),
            severity="required",
            provision_text="All parties accessing criminal justice information shall comply with the FBI CJIS Security Policy, including personnel security, encryption, and audit requirements.",
        ),
        ComplianceRule(
            id="cjis_background_checks",
            law="CJIS",
            requirement="Fingerprint-based background checks for personnel",
            description="All personnel with access to CJI must undergo fingerprint-based background checks.",
            applies_to=_j(["IDSA", "MOU"]),
            severity="required",
            provision_text="All personnel with access to criminal justice information shall undergo fingerprint-based background checks.",
        ),

        # General rules
        ComplianceRule(
            id="general_purpose_limitation",
            law="general",
            requirement="Data use must be limited to stated purpose",
            description="All data sharing agreements must clearly state the purpose and limit use to that purpose.",
            applies_to=_j(["BAA", "DUA", "MOU", "IDSA", "QSOA", "compact", "joint_funding"]),
            severity="required",
            provision_text="Data received under this agreement shall be used only for the purposes stated herein.",
        ),
        ComplianceRule(
            id="general_data_destruction",
            law="general",
            requirement="Data return or destruction upon termination",
            description="Upon termination, shared data must be returned or securely destroyed.",
            applies_to=_j(["BAA", "DUA", "MOU", "IDSA", "QSOA"]),
            severity="required",
            provision_text="Upon termination, all data received under this agreement shall be returned or securely destroyed.",
        ),
        ComplianceRule(
            id="general_security_safeguards",
            law="general",
            requirement="Appropriate security safeguards required",
            description="Receiving party must implement reasonable security measures to protect shared data.",
            applies_to=_j(["BAA", "DUA", "MOU", "IDSA", "compact"]),
            severity="required",
            provision_text="Receiving party shall implement administrative, physical, and technical safeguards to protect shared data.",
        ),
        ComplianceRule(
            id="general_audit_rights",
            law="general",
            requirement="Providing party should retain audit rights",
            description="The party providing data should have the right to audit the receiving party's compliance.",
            applies_to=_j(["BAA", "DUA", "IDSA"]),
            severity="recommended",
            provision_text="Providing party shall have the right to audit receiving party's compliance with this agreement.",
        ),
    ]

    for r in rules:
        db.add(r)
    db.flush()
    return len(rules)


# ---------------------------------------------------------------------------
# CONSENT FORMS (pre-built for known gaps)
# ---------------------------------------------------------------------------

def _seed_consent_forms(db: Session) -> int:
    consent_forms = [
        # Gap 1: DOC <-> MMIS (incarceration -> Medicaid)
        ConsentForm(
            id="consent_doc_mmis",
            gap_id=1,
            consent_type="HIPAA_authorization",
            title="Authorization to Share Correctional Health Records with Medicaid Provider",
            governing_law="HIPAA",
            description="Authorizes the Department of Corrections to share health records with community Medicaid providers upon release.",
            body_text="""AUTHORIZATION FOR DISCLOSURE OF HEALTH INFORMATION
(Correctional Health Records to Community Provider)

I, _________________________, authorize the Department of Corrections Health Services to disclose the following health information to my community health care provider / Medicaid managed care organization:

INFORMATION TO BE DISCLOSED:
- Current medications and dosages
- Active diagnoses and treatment plans
- Recent lab results (within last 6 months)
- Allergies and adverse reactions
- Scheduled follow-up appointments
- Mental health treatment summary (if applicable)
- Substance use treatment summary (if applicable and separately consented under 42 CFR Part 2)

PURPOSE: To ensure continuity of care upon release from incarceration.

DISCLOSED TO: _________________________ (community provider/MCO name)

This authorization expires 90 days after my release date or upon revocation, whichever comes first.

I understand I may revoke this authorization at any time in writing. I understand this authorization is voluntary and treatment will not be conditioned upon signing.

Signature: _________________________ Date: _____________
DOB: _________________ Facility: _________________________
Expected Release Date: _________________""",
            required_fields=_j(["patient_name", "dob", "facility", "release_date", "receiving_provider", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 2: DOC <-> BH Authority (42 CFR Part 2)
        ConsentForm(
            id="consent_doc_bh",
            gap_id=2,
            consent_type="CFR42_consent",
            title="42 CFR Part 2 Consent: Correctional SUD Treatment to Community BH Provider",
            governing_law="42 CFR Part 2",
            description="Authorizes disclosure of substance use disorder treatment records from corrections to community behavioral health providers. Must meet the heightened consent requirements of 42 CFR Part 2.",
            body_text="""CONSENT FOR DISCLOSURE OF SUBSTANCE USE DISORDER TREATMENT RECORDS
(42 CFR Part 2 — Correctional Facility to Community Provider)

I, _________________________, authorize:

FROM: _________________________ (correctional SUD treatment program name)

TO: _________________________ (community behavioral health provider name)

INFORMATION TO BE DISCLOSED:
- SUD diagnosis and treatment history during incarceration
- Medication-assisted treatment (MAT) medications, dosages, and prescribing information
- Treatment attendance and progress summary
- Discharge/transition plan
- Recommended continuing care

PURPOSE: Continuity of substance use disorder treatment upon release from incarceration.

EXPIRATION: This consent expires 90 days after my release date: _____________ or upon written revocation.

I understand that:
1. I may revoke this consent at any time in writing.
2. My treatment will not be conditioned on signing this consent.
3. A general authorization for medical records is NOT sufficient — this specific consent is required.
4. Federal law (42 CFR Part 2) prohibits the recipient from making any further disclosure without my written consent.

RE-DISCLOSURE NOTICE: "This information has been disclosed from records protected by federal confidentiality rules (42 CFR Part 2). The federal rules prohibit you from making any further disclosure of information in this record that identifies a patient as having or having had a substance use disorder either directly, by reference to publicly available information, or through verification of such identification by another person unless further disclosure is expressly permitted by the written consent of the individual whose information is being disclosed or as otherwise permitted by 42 CFR Part 2."

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________""",
            required_fields=_j(["patient_name", "dob", "program_name", "receiving_provider", "release_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 3: Probation <-> BH Authority (compliance-only)
        ConsentForm(
            id="consent_probation_bh",
            gap_id=3,
            consent_type="CFR42_consent",
            title="Limited Disclosure Consent: Treatment Compliance to Probation Officer",
            governing_law="42 CFR Part 2",
            description="Authorizes behavioral health provider to share ONLY attendance/compliance data (not clinical details) with a named probation officer.",
            body_text="""LIMITED DISCLOSURE CONSENT
(Treatment Compliance Information Only — 42 CFR Part 2)

I, _________________________, authorize:

FROM: _________________________ (treatment program name)

TO: _________________________ (probation officer name and agency)

INFORMATION TO BE DISCLOSED (LIMITED TO):
- Whether I am currently enrolled in treatment: YES/NO
- Dates of attendance at scheduled treatment sessions
- Whether I am in compliance with my treatment plan: YES/NO
- If non-compliant, whether non-compliance is due to circumstances beyond my control: YES/NO

THIS CONSENT DOES NOT AUTHORIZE DISCLOSURE OF:
- Diagnosis or clinical details
- Treatment notes or assessments
- Medication information
- Substance use history
- Mental health information
- Any other clinical information

PURPOSE: To allow my probation officer to verify compliance with court-ordered treatment conditions.

EXPIRATION: This consent expires on _____________ (end of supervision period) or upon written revocation.

I understand that:
1. I may revoke this consent at any time in writing.
2. My treatment will not be conditioned on signing this consent.
3. The recipient (probation officer) may NOT re-disclose this information.
4. This limited consent does NOT authorize disclosure of clinical details.

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________
Case Number: _________________________""",
            required_fields=_j(["patient_name", "dob", "program_name", "probation_officer", "agency", "case_number", "supervision_end_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 5: HMIS <-> MMIS (homelessness -> Medicaid)
        ConsentForm(
            id="consent_hmis_mmis",
            gap_id=5,
            consent_type="HIPAA_authorization",
            title="Authorization to Share Housing Status with Medicaid Health Plan",
            governing_law="HIPAA",
            description="Authorizes homeless services provider to share housing status and basic demographic information with Medicaid managed care organization for care coordination.",
            body_text="""AUTHORIZATION TO SHARE HOUSING INFORMATION WITH HEALTH PLAN

I, _________________________, authorize:

FROM: _________________________ (homeless services provider / shelter name)

TO: _________________________ (Medicaid MCO / health plan name)

INFORMATION TO BE DISCLOSED:
- Current housing status (sheltered, unsheltered, transitional, permanent supportive)
- Current location/shelter (if applicable)
- Contact information and best way to reach me
- Case manager name and contact information
- Housing-related needs that affect my health care

PURPOSE: To help my health plan coordinate my care based on my current housing situation, including scheduling, transportation, medication management, and connecting me with appropriate services.

This authorization expires on _____________ or upon written revocation.

I may revoke this authorization at any time in writing. My housing services and health care will not be conditioned upon signing.

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________
Medicaid ID: _________________________""",
            required_fields=_j(["patient_name", "dob", "medicaid_id", "housing_provider", "mco_name", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 6: HMIS <-> BH Authority
        ConsentForm(
            id="consent_hmis_bh",
            gap_id=6,
            consent_type="general_release",
            title="Release for Care Coordination: Housing and Behavioral Health",
            governing_law="HIPAA",
            description="Authorizes information sharing between homeless services and behavioral health providers for care coordination.",
            body_text="""AUTHORIZATION FOR INFORMATION SHARING
(Housing Services and Behavioral Health Care Coordination)

I, _________________________, authorize the following organizations to share information about me for the purpose of coordinating my care:

ORGANIZATION 1: _________________________ (homeless services provider)
ORGANIZATION 2: _________________________ (behavioral health provider)

INFORMATION THAT MAY BE SHARED:
- Demographics and contact information
- Housing status and history
- Service enrollment and engagement
- Care plan and goals
- Appointments and attendance
- Case manager contact information
- Referral information

NOTE: Substance use disorder treatment records are protected by 42 CFR Part 2 and require a separate, specific consent form. This authorization does NOT cover SUD treatment records.

This authorization expires on _____________ or upon written revocation.

I understand I may revoke this authorization at any time in writing. My services will not be conditioned upon signing.

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________""",
            required_fields=_j(["patient_name", "dob", "housing_provider", "bh_provider", "expiration_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 7: PHA <-> MMIS
        ConsentForm(
            id="consent_pha_mmis",
            gap_id=7,
            consent_type="HIPAA_authorization",
            title="Authorization to Share Housing and Health Information",
            governing_law="HIPAA",
            description="Authorizes public housing authority and Medicaid plan to share information about housing needs and health conditions for better service coordination.",
            body_text="""AUTHORIZATION FOR INFORMATION SHARING
(Public Housing Authority and Medicaid Health Plan)

I, _________________________, authorize:

DIRECTION 1 — Housing to Health:
FROM: _________________________ (Housing Authority)
TO: _________________________ (Medicaid MCO)
Information: Housing status, unit type, lease compliance, eviction risk indicators

DIRECTION 2 — Health to Housing:
FROM: _________________________ (Medicaid MCO)
TO: _________________________ (Housing Authority)
Information: Disability accommodations needed, accessibility requirements, proximity to provider needs

PURPOSE: To coordinate housing and health services so that my housing meets my health needs and my health plan knows my housing situation.

This authorization expires on _____________ or upon written revocation.

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________""",
            required_fields=_j(["patient_name", "dob", "housing_authority", "mco_name", "expiration_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 8: IEP <-> BH Authority (FERPA)
        ConsentForm(
            id="consent_iep_bh",
            gap_id=8,
            consent_type="FERPA_release",
            title="FERPA Consent: IEP Records to Behavioral Health Provider",
            governing_law="FERPA",
            description="Parental consent for school to share IEP and related education records with child's behavioral health provider.",
            body_text="""CONSENT FOR DISCLOSURE OF EDUCATION RECORDS
(IEP/Special Education Records to Behavioral Health Provider)

Student Name: _________________________
Date of Birth: _________________________
School/District: _________________________

I, _________________________, as parent/guardian of the above-named student, consent to the disclosure of the following education records:

RECORDS TO BE DISCLOSED:
- Current Individualized Education Program (IEP)
- Most recent evaluation reports
- Current accommodations and modifications
- Related services (speech, OT, PT, counseling)
- Behavioral intervention plan (if applicable)
- Progress monitoring data on IEP goals

DISCLOSED TO: _________________________ (behavioral health provider name)

PURPOSE: To coordinate educational and behavioral health services so that treatment goals and IEP goals are aligned, and to ensure the child's behavioral health provider has complete information about school-based supports.

This consent expires on _____________ or at the end of the current school year, whichever comes first.

I understand:
- This consent is voluntary
- I may revoke it at any time in writing
- My child's educational services will not be conditioned on signing
- I have the right to inspect any records disclosed

Parent/Guardian Signature: _________________________ Date: _____________
Printed Name: _________________________
Relationship to Student: _________________________""",
            required_fields=_j(["student_name", "student_dob", "school_name", "parent_name", "bh_provider", "expiration_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 12: VA <-> HIE
        ConsentForm(
            id="consent_va_hie",
            gap_id=12,
            consent_type="HIPAA_authorization",
            title="VA Authorization to Share Records with Health Information Exchange",
            governing_law="38 USC 5701 / HIPAA",
            description="Authorizes VA to share health records with the state/regional health information exchange for care coordination with community providers.",
            body_text="""AUTHORIZATION FOR DISCLOSURE OF VA HEALTH INFORMATION

I, _________________________, authorize the Department of Veterans Affairs to share my health information with the health information exchange and community providers as specified below:

FROM: VA Medical Center / _________________________ (facility name)

TO: _________________________ (Health Information Exchange name)
AND: _________________________ (community provider name, if applicable)

INFORMATION TO BE DISCLOSED:
- Current medications and dosages
- Active diagnoses and problem list
- Recent lab results
- Allergies and adverse reactions
- Hospital discharge summaries
- Upcoming appointments

PURPOSE: To ensure my community health care providers have access to my VA health information for safe, coordinated care.

This authorization expires on _____________ or upon written revocation.

I understand:
- This is voluntary and will not affect my VA benefits or care
- I may revoke at any time using VA Form 10-5345a
- Community providers who receive my information are bound by HIPAA

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________
Last 4 SSN: _________ VA Patient ID: _________________________""",
            required_fields=_j(["veteran_name", "dob", "ssn_last4", "va_patient_id", "va_facility", "hie_name", "community_provider", "expiration_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
        # Gap 14: SSA <-> BH Authority
        ConsentForm(
            id="consent_ssa_bh",
            gap_id=14,
            consent_type="CFR42_consent",
            title="42 CFR Part 2 Consent: SUD Records to SSA for Disability Determination",
            governing_law="42 CFR Part 2",
            description="Authorizes behavioral health / SUD treatment provider to share treatment records with SSA for the purpose of disability determination.",
            body_text="""CONSENT FOR DISCLOSURE OF SUBSTANCE USE DISORDER TREATMENT RECORDS
(To Social Security Administration for Disability Determination)

I, _________________________, authorize:

FROM: _________________________ (behavioral health / SUD treatment program name)

TO: Social Security Administration
    Disability Determination Services
    _________________________ (address)

INFORMATION TO BE DISCLOSED:
- SUD diagnosis and treatment history
- Functional assessments and limitations
- Treatment attendance and compliance
- Medications prescribed for SUD treatment
- Prognosis and expected duration of condition
- Any co-occurring mental health diagnoses and treatment

PURPOSE: To provide evidence in support of my application for SSI/SSDI disability benefits.

EXPIRATION: This consent expires on _____________ or upon final determination of my disability claim, whichever comes first.

I understand that:
1. I may revoke this consent at any time in writing.
2. My treatment will not be conditioned on signing.
3. SSA may not re-disclose this information except as permitted by 42 CFR Part 2.

RE-DISCLOSURE NOTICE: [42 CFR Part 2 re-disclosure prohibition notice applies]

Signature: _________________________ Date: _____________
Printed Name: _________________________ DOB: _____________
SSN: _________________________
SSA Claim Number: _________________________""",
            required_fields=_j(["patient_name", "dob", "ssn", "ssa_claim_number", "program_name", "expiration_date", "signature", "date"]),
            status="ready",
            created_at="2025-01-01",
        ),
    ]

    for cf in consent_forms:
        db.add(cf)
    db.flush()
    return len(consent_forms)
