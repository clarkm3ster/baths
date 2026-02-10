"""
Citation Parser — Extracts structured components from legal citation strings.

Handles: US Code, CFR, Federal Register, PA Statutes, PA Regulations,
case law, constitutional amendments.
"""
import re


def parse_citation(citation: str) -> dict:
    """Parse a citation string into structured components."""
    result = {
        "source_type": "unknown",
        "title_number": None,
        "chapter": None,
        "part": None,
        "section": None,
        "subsection": None,
    }

    # US Code: "42 U.S.C. § 1396d(r)"
    usc = re.match(r"(\d+)\s+U\.S\.C\.\s+§\s*(\S+)", citation)
    if usc:
        result["source_type"] = "usc"
        result["title_number"] = usc.group(1)
        section_full = usc.group(2)
        sec_match = re.match(r"([^(]+)(.*)", section_full)
        if sec_match:
            result["section"] = sec_match.group(1)
            result["subsection"] = sec_match.group(2) or None
        else:
            result["section"] = section_full
        return result

    # CFR with Part: "42 CFR Part 2"
    cfr_part = re.match(r"(\d+)\s+CFR\s+Part\s+(\d+)", citation)
    if cfr_part:
        result["source_type"] = "cfr"
        result["title_number"] = cfr_part.group(1)
        result["part"] = cfr_part.group(2)
        return result

    # CFR with section: "42 CFR § 438.206"
    cfr_sec = re.match(r"(\d+)\s+CFR\s+§\s*(\S+)", citation)
    if cfr_sec:
        result["source_type"] = "cfr"
        result["title_number"] = cfr_sec.group(1)
        sec = cfr_sec.group(2)
        if "." in sec:
            parts = sec.split(".", 1)
            result["part"] = parts[0]
            result["section"] = parts[1]
        else:
            result["section"] = sec
        return result

    # CFR Parts range: "45 CFR Parts 160 and 164"
    cfr_parts = re.match(r"(\d+)\s+CFR\s+Parts?\s+(.+)", citation)
    if cfr_parts:
        result["source_type"] = "cfr"
        result["title_number"] = cfr_parts.group(1)
        result["part"] = cfr_parts.group(2)
        return result

    # Federal Register
    fr = re.match(r"(\d+)\s+FR\s+(\d+)", citation)
    if fr:
        result["source_type"] = "fr"
        result["title_number"] = fr.group(1)
        result["section"] = fr.group(2)
        return result

    # PA Statute
    pa_stat = re.match(r"(\d+)\s+Pa\.C\.S\.\s+§\s*(\S+)", citation)
    if pa_stat:
        result["source_type"] = "pa_statute"
        result["title_number"] = pa_stat.group(1)
        result["section"] = pa_stat.group(2)
        return result

    # PA Regulation
    pa_reg = re.match(r"(\d+)\s+Pa\.\s+Code\s+§\s*(\S+)", citation)
    if pa_reg:
        result["source_type"] = "pa_reg"
        result["title_number"] = pa_reg.group(1)
        result["section"] = pa_reg.group(2)
        return result

    # Constitutional Amendment
    const = re.match(r"U\.S\.\s+Const\.\s+amend\.\s+(\w+)", citation)
    if const:
        result["source_type"] = "constitution"
        result["section"] = const.group(1)
        return result

    # Case law
    case = re.match(r"(.+?),\s+(\d+)\s+U\.S\.\s+(\d+)", citation)
    if case:
        result["source_type"] = "case_law"
        result["section"] = case.group(2)
        result["subsection"] = case.group(3)
        return result

    return result


def determine_source_type(citation: str) -> str:
    """Determine the source type from a citation string."""
    return parse_citation(citation)["source_type"]
