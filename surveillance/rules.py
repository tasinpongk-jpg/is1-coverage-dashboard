"""Rules-based pre-classifier for SET disclosures.

Goal: cut Haiku API calls by ~80% by deterministically classifying disclosures
whose headlines follow standard SET templates. Falls through to Haiku for
genuinely ambiguous content.

Output schema matches `classifier.Classification` exactly so this is a drop-in
replacement for the easy cases. `match_rules()` returns:
  - Classification    -> rule matched, no Haiku call needed
  - None              -> ambiguous, fall through to Haiku

Rules are evaluated TOP-DOWN, FIRST-MATCH-WINS. Order matters: more specific
critical patterns must come before broader routine ones (e.g. "Resolutions ...
omit dividend" is critical, "Resolution of the Exercise of XYZ-W2" is routine).

Validated against 938 historical Haiku-labeled rows + 335K row 5y dataset.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from classifier import Classification


# ---------------------------------------------------------------------------
# Rule definition
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    severity: str
    category: str
    summary_template: str
    suggested_action: str
    rationale: str
    summary_th_template: str = ""


_HL_MAX = 90  # truncate headlines in auto-summary


# ---------------------------------------------------------------------------
# CRITICAL — most specific patterns FIRST
# ---------------------------------------------------------------------------

_CRITICAL_RULES: list[Rule] = [
    # SET-initiated clarification — broadest catch (header always starts with "Clarification")
    Rule(
        name="set_clarification",
        pattern=re.compile(
            r"^Clarification\b.*\b("
            r"requested by SET|"
            r"as requested|"
            r"on the (Disposal|Acquisition|Change of Operational|Change in|Information|"
            r"News|Material Information)|"
            r"of (the )?(news|information|material information|additional information|"
            r"financial information|Information Regarding)|"
            r"on (the )?Change of Operational Performance Exceeding 20|"
            r"on (the )?(announcement|disclosure)"
            r")",
            re.IGNORECASE,
        ),
        severity="critical",
        category="set_clarification",
        summary_template="{symbol} filed a clarification: {hl}",
        summary_th_template="{symbol} ยื่นคำชี้แจง: {hl}",
        suggested_action="Open the disclosure PDF and the underlying news article before market open; brief sector head.",
        rationale="Clarification filing — typically SET-mandated; treat as critical per rubric.",
    ),
    # Trading-sign / suspension / delisting / free-float / Auto Pause
    Rule(
        name="trading_sign_posted",
        pattern=re.compile(
            r"\b(SET\s+(temporarily\s+)?posted|"
            r"(SP|NP|NC|ST|CB|H|P)\s*sign\s+(posted|added|lifted|remained|imposed|removed)|"
            r"(SP|NP|NC|ST|CB|H|P)\s+sign\s+(posted|on)|"
            r"posted\s+the\s+(SP|NP|NC|ST|CB|H|P)\s+sign|"
            r"Trading\s+Suspension|"
            r"is\s+the\s+last\s+day\s+of\s+trading|"
            r"SET\s+delists|"
            r"delisting\s+of|"
            r"free\s+float\s+qualification|"
            r"Auto\s+Pause)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="trading_sign",
        summary_template="Trading-sign / suspension event for {symbol}: {hl}",
        summary_th_template="เหตุการณ์เครื่องหมายซื้อขาย/พักการซื้อขายของ {symbol}: {hl}",
        suggested_action="Read the full announcement immediately; confirm impact on the covered name and notify desk.",
        rationale="Trading-sign / suspension / delisting events — automatic critical per rubric.",
    ),
    # Senior-exec resignation (CEO/CFO/Chair/President/MD)
    Rule(
        name="exec_resignation",
        pattern=re.compile(
            r"^(Notification\s+of\s+(the\s+)?)?Resignation\s+of\s+(the\s+)?"
            r"(Chief\s+(Executive|Financial)\s+Officer|CEO|CFO|"
            r"Chairman|Chair\b|President\b|Managing\s+Director)|"
            r"^Changing\s+of\s+(CEO|CFO|Chief\s+(Executive|Financial)\s+Officer)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="director_mgmt_change",
        summary_template="Senior-exec resignation / change at {symbol}: {hl}",
        summary_th_template="ผู้บริหารระดับสูง {symbol} ลาออก/เปลี่ยนแปลง: {hl}",
        suggested_action="Call IR within the hour; check for related operational issues or pending disclosures.",
        rationale="Unexpected CEO/CFO/Chair resignation — automatic critical per rubric.",
    ),
    # Capital reduction
    Rule(
        name="capital_reduction",
        pattern=re.compile(
            r"^Decreasing\s+of\s+the\s+company'?s\s+paid-up\s+capital",
            re.IGNORECASE,
        ),
        severity="critical",
        category="capital_change",
        summary_template="{symbol} announces capital reduction: {hl}",
        summary_th_template="{symbol} ประกาศลดทุนจดทะเบียนชำระแล้ว: {hl}",
        suggested_action="Open the resolution PDF; check rationale (loss-offset vs cash distribution) and shareholder approval requirement.",
        rationale="Paid-up capital reduction — material capital event per rubric, automatic critical.",
    ),
    # Dividend omission — STANDALONE headline only (the pure announcement, not bundled in BOD resolution)
    # Haiku rates BOD-bundled headlines as material because the body covers more than just omission.
    Rule(
        name="dividend_omission",
        pattern=re.compile(
            r"^(Omission\s+of\s+Dividend\s+Payment|"
            r"Cancellation\s+of\s+Dividend\s+Payment|"
            r"No\s+Dividend\s+Payment)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="dividend",
        summary_template="{symbol} omitting dividend: {hl}",
        summary_th_template="{symbol} งดจ่ายเงินปันผล: {hl}",
        suggested_action="Open the resolution; identify driver (loss, cash needs, capital action) and any guidance change.",
        rationale="Standalone dividend omission announcement — automatic critical per rubric.",
    ),
    # Tender offer / takeover declarations
    Rule(
        name="tender_offer",
        pattern=re.compile(
            r"\b(Tender\s+Offer|"
            r"Form\s+247-?[34]|"
            r"Form\s+250-?[12]|"
            r"Declaration\s+of\s+Intention\s+to\s+Acquire\s+(Securities|Shares)|"
            r"Business\s+Takeover|"
            r"Receipt\s+of\s+a\s+Tender\s+Offer)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="ma_acquisition_disposal",
        summary_template="{symbol} tender-offer / takeover disclosure: {hl}",
        summary_th_template="{symbol} เปิดเผยข้อมูลคำเสนอซื้อ/ครอบงำกิจการ: {hl}",
        suggested_action="Open the form immediately; identify offeror, price, conditions, and tender period.",
        rationale="Tender-offer / takeover-intent filings are always critical regardless of size.",
    ),
    # M&A — material asset / business / subsidiary transactions
    Rule(
        name="ma_disposal_acquisition",
        pattern=re.compile(
            r"\b(Information\s+Memorandum\s+on\s+(Disposal|Acquisition)\s+of\s+Assets|"
            r"Disposal\s+of\s+Assets\s+and\s+Connected\s+Transactions|"
            r"Acquisition\s+of\s+(a\s+new\s+indirect\s+)?subsidiary|"
            r"Share\s+Acquisition\s+in\b|"
            r"Divestment\s+of\s+an\s+Investment\s+in\s+a\s+Subsidiary|"
            r"Disposal\s+of\s+Assets\s+in\s+Subsidiary\s+Company|"
            r"Notification\s+of\s+Disposal\s+of\s+Assets|"
            r"Cessation\s+of\s+Subsidiary\s+Status|"
            r"Termination\s+of\s+Subsidiary\s+Status|"
            r"acquire\s+additional\s+.*\s+properties\s+from)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="ma_acquisition_disposal",
        summary_template="{symbol} M&A / asset transaction: {hl}",
        summary_th_template="{symbol} รายการได้มา/จำหน่ายไปซึ่งสินทรัพย์: {hl}",
        suggested_action="Open the IFA opinion / Info Memo; check transaction size vs total assets and connected-party flags.",
        rationale="Material acquisition or disposal of assets — escalate per rubric.",
    ),
    # Connected transactions / RPT — IFA opinions OR explicit "connected transaction" wording
    Rule(
        name="connected_transaction",
        pattern=re.compile(
            r"\b(Independent\s+Financial\s+Advisor|IFA)\b.*\b(Disposal|Acquisition|Connected|Related)|"
            r"\b(Acknowledged\s+the\s+Connected\s+Transaction|"
            r"Notification\s+for\s+the\s+Purchase\s+of.*\s+from)\b|"
            r"\bRelated\s+Party\s+Transaction\s+for\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="connected_transaction",
        summary_template="{symbol} connected/related-party transaction: {hl}",
        summary_th_template="{symbol} รายการที่เกี่ยวโยงกัน: {hl}",
        suggested_action="Read the IFA opinion / Info Memo in full; note fairness conclusion and dissenting points before vote.",
        rationale="Connected/related-party transaction or IFA opinion — always critical.",
    ),
    # REIT/Trust manager change
    Rule(
        name="reit_manager_change",
        pattern=re.compile(
            r"\b(appointment\s+of\s+new\s+REIT\s+Manager|"
            r"new\s+Trustee|"
            r"change\s+of\s+(the\s+)?Trustee|"
            r"replacement\s+of\s+REIT\s+Manager)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="director_mgmt_change",
        summary_template="REIT manager / trustee change at {symbol}: {hl}",
        summary_th_template="การเปลี่ยนแปลงผู้จัดการกองทรัสต์/ทรัสตี: {hl}",
        suggested_action="Open the disclosure; identify outgoing/incoming entity, fee structure changes, and unitholder vote requirement.",
        rationale="REIT-manager or trustee change — critical per PFREIT rubric.",
    ),
    # BOD / Board Meeting resolutions bundled with No Dividend / capital change
    # Accepts "BOD Meeting" or "Board Meeting" or "Board of Directors' Meeting"
    Rule(
        name="bod_no_dividend",
        pattern=re.compile(
            r"\b(BOD|Board\s+Meeting|Board\s+of\s+Directors'?\s+Meeting).*Resolution.*\b("
            r"No\s+Dividend|omit\s+dividend|"
            r"decrease.*increase\s+capital|"
            r"allocation\s+of\s+newly\s+issued\s+shares)\b|"
            r"^Notification\s+of\s+Board\s+Meeting\s+No\.\s*\d+/\d+\s+Resolutions:\s+"
            r"Approval\s+of\s+\d{4}\s+Financial\s+Statements?,?\s+No\s+Dividend",
            re.IGNORECASE,
        ),
        severity="critical",
        category="capital_change",
        summary_template="{symbol} BOD bundled resolution (no dividend / capital action): {hl}",
        summary_th_template="{symbol} มติคณะกรรมการ (งดปันผล/ทุน): {hl}",
        suggested_action="Read the full BOD resolution; multiple material actions stacked — quantify cumulative impact.",
        rationale="BOD bundled resolution combining no-dividend with capital action — critical.",
    ),
    # Submission of Offer to Buy/Lease asset of a fund (REIT-specific tender event)
    Rule(
        name="submission_of_offer_fund",
        pattern=re.compile(
            r"^(Result\s+of\s+the\s+)?Submission\s+of\s+(the\s+)?Offer\s+to\s+(Buy|Lease)\s+"
            r"(or\s+Lease\s+)?the\s+Asset\s+of\s+(the\s+)?Fund",
            re.IGNORECASE,
        ),
        severity="critical",
        category="ma_acquisition_disposal",
        summary_template="{symbol} fund-asset offer/tender disclosure: {hl}",
        summary_th_template="{symbol} ยื่นข้อเสนอซื้อ/เช่าทรัพย์สินของกองทุน: {hl}",
        suggested_action="Read the disclosure; identify offeror, price, and timeline for unitholder action.",
        rationale="Fund-asset offer-to-buy/lease — material capital event for the fund — critical.",
    ),
    # Financial assistance to connected persons (RPT, can be material loan/guarantee)
    Rule(
        name="financial_assistance_rpt",
        pattern=re.compile(
            r"\b(Financial\s+Assistance\s+(to|from|Limit)|"
            r"Extension\s+of\s+Financial\s+Assistance|"
            r"Increase\s+in\s+Financial\s+Assistance|"
            r"Financial\s+Assistance\s+to\s+Connected\s+Person)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="connected_transaction",
        summary_template="{symbol} financial assistance / inter-company loan: {hl}",
        summary_th_template="{symbol} ให้ความช่วยเหลือทางการเงินแก่บุคคลที่เกี่ยวโยง: {hl}",
        suggested_action="Open the disclosure; identify counterparty, loan amount, terms, and connected-party flags.",
        rationale="Financial assistance disclosure (often connected-party loan/guarantee) — critical per rubric.",
    ),
    # Performance-swing >20% mandatory clarification
    Rule(
        name="performance_swing_clarification",
        pattern=re.compile(
            r"^Clarification\s+on\s+the\s+Change\s+of\s+Operational\s+Performance\s+Exceeding\s+20",
            re.IGNORECASE,
        ),
        severity="critical",
        category="set_clarification",
        summary_template="{symbol} mandatory >20% performance-swing clarification: {hl}",
        summary_th_template="{symbol} คำชี้แจงผลการดำเนินงานเปลี่ยนแปลงเกิน 20%: {hl}",
        suggested_action="Open the disclosure; quantify the YoY/QoQ swing and identify the driver.",
        rationale="SET-mandated clarification when results swing >20% — automatic critical.",
    ),
]


# ---------------------------------------------------------------------------
# MATERIAL
# ---------------------------------------------------------------------------

_MATERIAL_RULES: list[Rule] = [
    # MD&A
    Rule(
        name="mda",
        pattern=re.compile(
            r"^Management\s+Discussion\s+and\s+Analysis\b",
            re.IGNORECASE,
        ),
        severity="material",
        category="earnings",
        summary_template="{symbol} released MD&A: {hl}",
        summary_th_template="{symbol} เผยแพร่คำอธิบายและการวิเคราะห์ของฝ่ายจัดการ: {hl}",
        suggested_action="Read the MD&A in full; flag drivers and any guidance changes for the morning meeting.",
        rationale="MD&A release for a covered name — material per rubric.",
    ),
    # F45 financial performance — covers Reviewed/Audited/Unreviewed/Revised forms
    Rule(
        name="financial_performance_f45",
        pattern=re.compile(
            r"^(Audited\s+|Unreviewed\s+)?(Financial\s+Performance\s+(Quarter|Yearly)|"
            r"Quarter\s+\d/\d{4}\s+and\s+Consolidated\s+F/S)\b.*\(F45\)",
            re.IGNORECASE,
        ),
        severity="material",
        category="earnings",
        summary_template="{symbol} filed F45 financial performance: {hl}",
        summary_th_template="{symbol} ยื่นแบบ F45 ผลประกอบการทางการเงิน: {hl}",
        suggested_action="Compare reported numbers vs prior period; flag any 20%+ swings for clarification check.",
        rationale="F45 quarterly/yearly financial performance — material per rubric.",
    ),
    # Financial Statement (the full Reviewed/Audited statements)
    Rule(
        name="financial_statement",
        pattern=re.compile(
            r"^Financial\s+Statement\s+(Quarter|Yearly)\b",
            re.IGNORECASE,
        ),
        severity="material",
        category="earnings",
        summary_template="{symbol} released financial statements: {hl}",
        summary_th_template="{symbol} เผยแพร่งบการเงิน: {hl}",
        suggested_action="Pull income-statement and balance-sheet deltas vs prior period; flag for morning review.",
        rationale="Quarterly/Yearly financial statement filing — material per rubric.",
    ),
    # Director / management resignation / change / combined "resignation and appointment"
    # Accepts: Notice/Notification of/on, optional "the", optional intervening "and appointment/election"
    # NOTE: "Chief Accountant" change is empirically labeled routine by Haiku — handled in routine rules.
    Rule(
        name="director_resignation",
        pattern=re.compile(
            r"^(Notice|Notification)\s+(of|on)\s+(the\s+)?"
            r"(Resignation|Changes?)\s+(?:and\s+(?:appointment|election)\s+)?(of|in)\s+"
            r"(a\s+)?(the\s+)?(Director|Directors?|Executives?|"
            r"Audit\s+Committee\s+member|"
            r"(a\s+)?Member\s+of\s+the\s+Audit\s+Committee|"
            r"Sub-?Committee)|"
            r"^Resignation\s+of\s+(an?\s+)?Directors?\b",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} board / management change: {hl}",
        summary_th_template="{symbol} เปลี่ยนแปลงคณะกรรมการ/ผู้บริหาร: {hl}",
        suggested_action="Identify outgoing vs incoming; check if independent-director composition is still compliant.",
        rationale="Director or audit committee composition change — material per rubric.",
    ),
    # Acting CFO/CEO/Chief X appointments — Haiku rates these material (governance signal)
    Rule(
        name="acting_appointment",
        pattern=re.compile(
            r"^(Notification\s+of\s+(the\s+)?)?Appointment\s+of\s+(CEO|CFO|Chief\s+\S+\s+Officer|"
            r"Acting\s+(CEO|CFO|Chief))",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} executive appointment: {hl}",
        summary_th_template="{symbol} แต่งตั้งผู้บริหาร: {hl}",
        suggested_action="Note the new appointment; check for related governance changes.",
        rationale="Senior-exec appointment (acting or permanent) — material per rubric.",
    ),
    # Director / management appointment (NEW director, NOT re-election of existing or sub-committee positions)
    # Re-election of expiring-term directors and sub-committee position assignments are routine (handled below)
    Rule(
        name="director_appointment",
        pattern=re.compile(
            r"^(Notification\s+of\s+)?(election\s+of\s+the\s+position\s+of\s+Directors|"
            r"(the\s+)?Appointment\s+of\s+(an?\s+)?(Independent\s+)?Director(?!s\s+to\s+replace|s\s+for\s+Sub)|"
            r"appointment\s+of\s+the\s+Sub-?Committees|"
            r"Board\s+of\s+Directors'?\s+Resolution\s+for\s+Appointment\s+of\s+director)",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} board / management appointment: {hl}",
        summary_th_template="{symbol} แต่งตั้งกรรมการ/ผู้บริหาร: {hl}",
        suggested_action="Note the new appointment; check independence status if relevant.",
        rationale="Board / sub-committee appointment — material per rubric.",
    ),
    # Information Memorandum (catch-all, after RPT/M&A criticals above)
    Rule(
        name="information_memorandum",
        pattern=re.compile(
            r"^Information\s+Memorandum",
            re.IGNORECASE,
        ),
        severity="material",
        category="information_memo",
        summary_template="{symbol} information memorandum: {hl}",
        summary_th_template="{symbol} สารสนเทศ: {hl}",
        suggested_action="Read the memorandum; identify the underlying transaction or filing.",
        rationale="Information memorandum filing — material per rubric.",
    ),
    # Trust unitholder resolutions (REIT) — material by default; specific actions caught above
    Rule(
        name="trust_unitholder_resolutions",
        pattern=re.compile(
            r"^Notification\s+of\s+(the\s+)?[Rr]esolutions\s+of\s+(the\s+)?Meeting\s+of\s+"
            r"(the\s+)?(Trust\s+)?Unitholders",
            re.IGNORECASE,
        ),
        severity="material",
        category="agm_resolution",
        summary_template="{symbol} trust unitholder resolutions: {hl}",
        summary_th_template="{symbol} มติที่ประชุมผู้ถือหน่วยลงทุน: {hl}",
        suggested_action="Read the resolutions; identify approved actions (acquisitions, capital changes, manager changes).",
        rationale="REIT/Trust unitholder resolution — material; specific actions like M&A or capital change handled above.",
    ),
    # Treasury / share repurchase program updates (start, end, completion)
    Rule(
        name="share_repurchase_program",
        pattern=re.compile(
            r"\b(End\s+of\s+the\s+Share\s+Repurchase\s+Project|"
            r"completion\s+of\s+(the\s+)?Share\s+Repurchase|"
            r"Share\s+Repurchase\s+Project\s+for\s+Financial\s+Management|"
            r"Resolution\s+of\s+the\s+Board.*Share\s+Repurchase)\b",
            re.IGNORECASE,
        ),
        severity="material",
        category="capital_change",
        summary_template="{symbol} share repurchase program update: {hl}",
        summary_th_template="{symbol} โครงการซื้อหุ้นคืน: {hl}",
        suggested_action="Note the cumulative shares repurchased and remaining authorization.",
        rationale="Share repurchase program update — material per rubric.",
    ),
    # Capital extension / discount offset
    Rule(
        name="capital_offset_extension",
        pattern=re.compile(
            r"^Extension\s+of\s+the\s+Period\s+for\s+Offsetting\s+the\s+Discount\s+on\s+Share\s+Capital",
            re.IGNORECASE,
        ),
        severity="material",
        category="capital_change",
        summary_template="{symbol} share-capital discount offset extension: {hl}",
        summary_th_template="{symbol} ขยายเวลาตัดบัญชีส่วนต่ำมูลค่าหุ้น: {hl}",
        suggested_action="Note the new offset period; no immediate action required.",
        rationale="Accounting extension on capital discount — material but procedural.",
    ),
]


# ---------------------------------------------------------------------------
# ROUTINE
# ---------------------------------------------------------------------------

_MATERIAL_AGM_RULES: list[Rule] = [
    # BOD resolution declaring dividend payment (the dividend declaration itself, not omission)
    Rule(
        name="bod_dividend_declaration",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+resolution\s+of\s+the\s+Board\s+of\s+Directors'?\s+Meeting\s+"
            r"regarding\s+the\s+payment\s+of\s+(an?\s+)?dividend",
            re.IGNORECASE,
        ),
        severity="material",
        category="dividend",
        summary_template="{symbol} BOD declared dividend: {hl}",
        summary_th_template="{symbol} คณะกรรมการอนุมัติจ่ายเงินปันผล: {hl}",
        suggested_action="Note dividend amount and yield; calendar X-D date when notification of book closed date follows.",
        rationale="BOD resolution declaring dividend payment — material per rubric.",
    ),
    # Generic shareholders' resolution release — Haiku-labeled empirically as MATERIAL by default.
    # Specific critical actions (capital reduction, dividend omission, M&A, RPT) are caught above.
    Rule(
        name="shareholders_resolution",
        pattern=re.compile(
            r"^Shareholders'?\s+meeting'?s?\s+resolution|"
            r"^(Notification\s+of\s+(the\s+)?)?(R|r)esolutions?\s+of\s+(the\s+)?"
            r"(\d{4}\s+)?(Annual\s+General\s+Meeting|General\s+Meeting|"
            r"Extraordinary\s+General\s+Meeting|Shareholders'?\s+Annual\s+General\s+Meeting)|"
            r"^Notification\s+of\s+the\s+resolutions?\s+of\s+the\s+Annual\s+General\s+Meeting",
            re.IGNORECASE,
        ),
        severity="material",
        category="agm_resolution",
        summary_template="{symbol} shareholders' meeting resolutions: {hl}",
        summary_th_template="{symbol} มติที่ประชุมผู้ถือหุ้น: {hl}",
        suggested_action="Read the resolutions list; flag any capital, dividend, or related-party items.",
        rationale="AGM/EGM resolution release — material per rubric; specific critical actions are caught by patterns above.",
    ),
]

_MATERIAL_RULES = _MATERIAL_RULES + _MATERIAL_AGM_RULES


_ROUTINE_RULES: list[Rule] = [
    # AGM/EGM convening notice — broad set of phrasings (publication / disclosure / uploading / dissemination / invitation)
    Rule(
        name="agm_convening_notice",
        pattern=re.compile(
            r"^(Publication|Disclosure|Uploading|Dissemination|Publishing|Publicizing|"
            r"Notification\s+convening\s+date|Notification\s+of\s+Publication)\s+(of|on)\s+"
            r"(the\s+)?(Notice|Invitation\s+Letter|Invitation|invitation)\s+(of|to|for)\s+(the\s+)?"
            r"(\d{4}\s+)?(Annual\s+General\s+Meeting|Extraordinary\s+General\s+Meeting|"
            r"General\s+Meeting|Public\s+Presentation|Earnings\s+Call|"
            r"Meeting\s+of\s+Trust\s+Unitholders|Meeting\s+of\s+(the\s+)?Unitholders)|"
            r"^Notification\s+of\s+the\s+(Annual\s+General|General|Extraordinary)\s+Meeting\s+of\s+Shareholders|"
            r"^Disclosure\s+of\s+the\s+Invitation\s+Letter\s+to\s+the\s+Annual\s+General\s+Meeting|"
            r"^(Publication|Uploading|Disclosure)\s+of\s+the\s+(notice|invitation)\s+of\s+the\s+Annual\s+General\s+Meeting|"
            r"^Disclosure\s+of\s+the\s+Notice\s+for\s+\d{4}\s+Annual\s+General\s+Meeting|"
            r"^Publicizing\s+an\s+Invitation\s+Letter|"
            r"^Dissemination\s+of\s+invitation\s+letter",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} convening notice: {hl}",
        summary_th_template="{symbol} หนังสือเชิญประชุม: {hl}",
        suggested_action="Calendar the meeting date; no immediate action.",
        rationale="Convening notice — only the resolutions passed AT the meeting are material.",
    ),
    # Earnings call / Public Presentation convening notice
    Rule(
        name="earnings_call_invite",
        pattern=re.compile(
            r"^(Invitation\s+to|Notification\s+(convening\s+date\s+of|for(\s+\S+'?s)?))\s+"
            r"(the\s+)?(Earnings\s+Call|Public\s+Presentation)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} earnings-call / opportunity-day invitation: {hl}",
        summary_th_template="{symbol} เชิญร่วมประชุมแถลงผลประกอบการ: {hl}",
        suggested_action="Calendar the date.",
        rationale="Convening notice for earnings call / public presentation — actual event is the material trigger.",
    ),
    # Chief Accountant change (Haiku rates routine — accountant change is procedural)
    Rule(
        name="chief_accountant_change",
        pattern=re.compile(
            r"^(Notification\s+(of|on)\s+(the\s+)?)?Changing\s+of\s+Chief\s+Accountant",
            re.IGNORECASE,
        ),
        severity="routine",
        category="director_mgmt_change",
        summary_template="{symbol} chief accountant change: {hl}",
        summary_th_template="{symbol} เปลี่ยนแปลงสมุหบัญชี: {hl}",
        suggested_action="No action required.",
        rationale="Chief accountant change — routine procedural.",
    ),
    # Schedule of AGM / dividend payment (BOD scheduling, no actual decisions yet)
    Rule(
        name="agm_schedule",
        pattern=re.compile(
            r"^Schedule\s+of\s+(the\s+)?Annual\s+General\s+Meeting\s+of\s+Shareholders",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM schedule announced: {hl}",
        summary_th_template="{symbol} กำหนดวันประชุมผู้ถือหุ้น: {hl}",
        suggested_action="Calendar the AGM date.",
        rationale="AGM-scheduling notification — routine; the resolutions passed at the meeting are the material event.",
    ),
    # Disclosure of invitation / notice for AGM (broader pattern catching abbreviated forms)
    Rule(
        name="agm_invitation_disclosure",
        pattern=re.compile(
            r"^Disclosure\s+of\s+(Invitation\s+Notice|the\s+Notice|Documents)\s+for\s+(the\s+)?\d{4}\s+"
            r"(Annual\s+General\s+Meeting|AGM)|"
            r"^To\s+inform\s+the\s+date\s+and\s+agendas?\s+of\s+(the\s+)?Annual\s+General\s+Meeting",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM invitation/notice disclosure: {hl}",
        summary_th_template="{symbol} เปิดเผยหนังสือเชิญประชุมผู้ถือหุ้น: {hl}",
        suggested_action="No action required.",
        rationale="AGM invitation/notice/document disclosure — routine.",
    ),
    # Letter of invitation / publication / publicity of AGM-related notices on website (full or AGM-abbreviated)
    Rule(
        name="agm_publicity_invitation",
        pattern=re.compile(
            r"^(Publication|Publicity)\s+(of\s+|the\s+)?(the\s+)?"
            r"(letter\s+of\s+invitation|invitation|Notice\s+on\s+arrangement|Notice)\s+"
            r"(to|of|on\s+arrangement\s+of)\s+the\s+\d{4}\s+(Annual\s+General\s+Meeting|AGM)|"
            r"^Publication\s+(of\s+the\s+|the\s+)?(Notice|invitation)\s+of\s+the\s+\d{4}\s+(AGM|Annual\s+General\s+Meeting)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM letter of invitation / publication: {hl}",
        summary_th_template="{symbol} เผยแพร่หนังสือเชิญประชุมผู้ถือหุ้น: {hl}",
        suggested_action="No action required.",
        rationale="Pre-AGM letter / publicity of invitation — routine.",
    ),
    # Right to Subscribe / Subscription channel publications (post-RO procedural)
    Rule(
        name="subscription_procedural",
        pattern=re.compile(
            r"^Publication\s+of\s+(Additional\s+Channel\s+for\s+Submission\s+of\s+Subscription\s+Information|"
            r"the\s+Notification\s+of\s+the\s+Right\s+to\s+Subscribe\s+for\s+the\s+Newly\s+Issued\s+Ordinary\s+Shares)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="capital_change",
        summary_template="{symbol} subscription procedural disclosure: {hl}",
        summary_th_template="{symbol} ประกาศช่องทางการจองซื้อ/สิทธิจองซื้อ: {hl}",
        suggested_action="No action required.",
        rationale="Post-RO procedural disclosure (subscription channel, right-to-subscribe) — routine.",
    ),
    # Public presentation report
    Rule(
        name="public_presentation",
        pattern=re.compile(
            r"^Report\s+of\s+the\s+Public\s+Presentation",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} opportunity-day report: {hl}",
        summary_th_template="{symbol} รายงาน Opportunity Day: {hl}",
        suggested_action="No action required; logged for periodic review.",
        rationale="Opportunity-day public-presentation report — routine.",
    ),
    # AGM/EGM minutes — all variants (Publication / Disclosure / on website / EGM)
    Rule(
        name="agm_minutes",
        pattern=re.compile(
            r"^(Publication|Disclosure)\s+(on|of)\s+(the\s+)?Minutes\s+(of|on)\s+(the\s+)?"
            r"(\d{4}\s+)?(Annual\s+General\s+Meeting|Extraordinary\s+General\s+Meeting|"
            r"AGM|EGM)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM/EGM minutes published: {hl}",
        summary_th_template="{symbol} เผยแพร่รายงานการประชุมผู้ถือหุ้น: {hl}",
        suggested_action="No action required; minutes archived for the meeting.",
        rationale="Post-meeting minutes publication — routine; resolutions already triaged.",
    ),
    # F24-1 audit committee form filings (composition disclosure, NOT change)
    # Tightened: must include "(F24-1)" or pure form-filing language without resignation/change verbs
    Rule(
        name="f24_1_audit_committee",
        pattern=re.compile(
            r"\(F24-?1\)|"
            r"^Form\s+(to\s+Report|for\s+Reporting)\s+(on\s+Names\s+of\s+Members\s+and\s+Scope\s+of\s+Work\s+of\s+)?"
            r"(the\s+)?Audit\s+Committee|"
            r"^Audit\s+Committee\s+Members\s+and\s+their\s+Mandate|"
            r"^Renewal\s+for\s+the\s+term\s+of\s+(the\s+)?Audit\s+Committee|"
            r"^Notification\s+of\s+Appointment\s+of\s+Sub-Committee\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} F24-1 / audit-committee filing: {hl}",
        summary_th_template="{symbol} แบบ F24-1 รายงานคณะกรรมการตรวจสอบ: {hl}",
        suggested_action="No action required; composition disclosure logged.",
        rationale="F24-1 audit-committee composition filing — routine when no change verb present.",
    ),
    # Warrant exercise notification
    Rule(
        name="warrant_exercise_notification",
        pattern=re.compile(
            r"^Notification\s+(of\s+)?(the\s+)?[Ee]xercise\s+of\s+[A-Z]+-W\d|"
            r"^Resolution\s+of\s+the\s+Exercise\s+of\s+\d+",
            re.IGNORECASE,
        ),
        severity="routine",
        category="warrant_exercise",
        summary_template="{symbol} warrant exercise notification: {hl}",
        summary_th_template="{symbol} แจ้งการใช้สิทธิวอร์แรนต์: {hl}",
        suggested_action="No action required; exercise event logged.",
        rationale="Standard warrant-exercise notification with no surprise — routine.",
    ),
    # Warrant / share-issue F53-5 result reports
    Rule(
        name="warrant_exercise_result",
        pattern=re.compile(
            r"^Report\s+on\s+the\s+results\s+of\s+(the\s+Exercise\s+of|"
            r"sale\s+of\s+common\s+shares)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} warrant/share-issue result (F53-5): {hl}",
        summary_th_template="{symbol} รายงานผลการใช้สิทธิ/เสนอขายหุ้น: {hl}",
        suggested_action="Note the take-up rate; no immediate action.",
        rationale="F53-5 result-of-exercise filing — routine.",
    ),
    # New shares listing (post-warrant, post-RO, etc.)
    Rule(
        name="new_shares_listing",
        pattern=re.compile(
            r"^New\s+shares\s+of\s+\S+\s+to\s+be\s+traded\s+on",
            re.IGNORECASE,
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} new shares listing: {hl}",
        summary_th_template="{symbol} หุ้นใหม่เริ่มซื้อขาย: {hl}",
        suggested_action="No action required.",
        rationale="Standard new-shares listing notice (post-exercise/RO) — routine.",
    ),
    # Asset appraisal value (REITs/PFs)
    Rule(
        name="asset_appraisal",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+Asset\s+Appraisal\s+Value",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} periodic asset appraisal: {hl}",
        summary_th_template="{symbol} รายงานการประเมินมูลค่าทรัพย์สิน: {hl}",
        suggested_action="Note the appraisal cadence; no immediate action.",
        rationale="Periodic asset-appraisal disclosure for property funds/REITs — routine.",
    ),
    # First-10 unitholders disclosure
    Rule(
        name="top10_unitholders",
        pattern=re.compile(
            r"^Announcement\s+of\s+the\s+first\s+10\s+unit\s+holders",
            re.IGNORECASE,
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} top-10 unitholders disclosure: {hl}",
        summary_th_template="{symbol} รายชื่อผู้ถือหน่วยลงทุน 10 อันดับแรก: {hl}",
        suggested_action="No action required; periodic disclosure.",
        rationale="Routine top-10 unitholder roster disclosure for funds.",
    ),
    # Book closed date for routine dividend
    Rule(
        name="book_closed_date",
        pattern=re.compile(
            r"^Notification\s+of\s+Book\s+Closed\s+Date",
            re.IGNORECASE,
        ),
        severity="routine",
        category="dividend",
        summary_template="{symbol} dividend book-closed date: {hl}",
        summary_th_template="{symbol} กำหนดวันปิดสมุดทะเบียนรับสิทธิเงินปันผล: {hl}",
        suggested_action="Calendar the X-D date; no immediate action.",
        rationale="Routine record-date notification (dividend already approved) — routine.",
    ),
    # REIT/Fund distribution payment (scheduled)
    Rule(
        name="reit_distribution",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+distribution\s+payment\s+for\s+the\s+period",
            re.IGNORECASE,
        ),
        severity="routine",
        category="dividend",
        summary_template="{symbol} scheduled distribution: {hl}",
        summary_th_template="{symbol} แจ้งการจ่ายผลประโยชน์ตอบแทน: {hl}",
        suggested_action="No action required; scheduled distribution logged.",
        rationale="Scheduled REIT distribution at expected cadence — routine per PFREIT rubric.",
    ),
    # Resumption of market making
    Rule(
        name="market_making_resumption",
        pattern=re.compile(
            r"^Notification\s+on\s+resumption\s+of\s+market\s+making",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} market-making resumption: {hl}",
        summary_th_template="{symbol} กลับมาทำหน้าที่ดูแลสภาพคล่อง: {hl}",
        suggested_action="No action required.",
        rationale="Routine market-making operational notice.",
    ),
    # Right adjustment of warrants (post-dividend, post-RO etc.) — routine
    Rule(
        name="warrant_right_adjustment",
        pattern=re.compile(
            r"^Right\s+Adjustment\s+of\s+\S+-W\d",
            re.IGNORECASE,
        ),
        severity="routine",
        category="warrant_exercise",
        summary_template="{symbol} warrant right adjustment: {hl}",
        summary_th_template="{symbol} ปรับสิทธิวอร์แรนต์: {hl}",
        suggested_action="No action required; mechanical adjustment.",
        rationale="Warrant right adjustment (mechanical, post-dividend or post-issuance) — routine.",
    ),
    # Notification of Publication of the Minutes — broader minutes pattern
    Rule(
        name="agm_minutes_notification",
        pattern=re.compile(
            r"^Notification\s+of\s+Publication\s+of\s+the\s+Minutes\s+of\s+the\s+\d{4}\s+Annual\s+General\s+Meeting",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM minutes published: {hl}",
        summary_th_template="{symbol} เผยแพร่รายงานการประชุมผู้ถือหุ้นประจำปี: {hl}",
        suggested_action="No action required; minutes archived for the meeting.",
        rationale="Post-AGM minutes publication notification — routine.",
    ),
    # Website notification housekeeping
    Rule(
        name="website_change_notification",
        pattern=re.compile(
            r"^Notification\s+of\s+Change\s+to\s+the\s+Company'?s\s+Website",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} company website change: {hl}",
        summary_th_template="{symbol} เปลี่ยนแปลงเว็บไซต์บริษัท: {hl}",
        suggested_action="No action required.",
        rationale="Operational website change — routine housekeeping.",
    ),
    # Re-election of expiring-term directors (term-replacement, not new appointment)
    Rule(
        name="director_reelection",
        pattern=re.compile(
            r"^(Notification\s+of\s+)?(the\s+)?Appointment\s+of\s+directors?\s+to\s+replace\s+"
            r"directors?\s+whose\s+terms?\s+(are\s+)?due\s+to\s+expire|"
            r"^The\s+Appointment\s+of\s+Directors?\s+for\s+Sub-?committees'?\s+Positions",
            re.IGNORECASE,
        ),
        severity="routine",
        category="director_mgmt_change",
        summary_template="{symbol} routine director re-election / sub-committee assignment: {hl}",
        summary_th_template="{symbol} แต่งตั้งกรรมการครบวาระเดิม / ตำแหน่งคณะอนุกรรมการ: {hl}",
        suggested_action="No action required.",
        rationale="Re-election of expiring-term directors or sub-committee assignment — routine per rubric.",
    ),
    # Annual report / Form 56-1 publication
    Rule(
        name="annual_report_publication",
        pattern=re.compile(
            r"^Publication\s+of\s+the\s+Annual\s+Report\s+\d{4}|"
            r"^Publication\s+of\s+(the\s+)?Form\s+56-?1\s+One\s+Report|"
            r"\bForm\s+56-?1\s+One\s+Report\b.*\bWebsite\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} 56-1 One Report / annual report publication: {hl}",
        summary_th_template="{symbol} เผยแพร่แบบ 56-1 One Report: {hl}",
        suggested_action="No action required; archived for the period.",
        rationale="Annual 56-1 report publication on website — routine periodic disclosure.",
    ),
    # AGM document disclosure (notice/agenda/documents on website etc.)
    Rule(
        name="agm_documents_website",
        pattern=re.compile(
            r"^(Disclosure|Publication|Posting)\s+(of|the)\s+(documents|the\s+Notice|"
            r"Notice)\s+(for|of)\s+(the\s+)?\d{4}\s+Annual\s+General\s+Meeting|"
            r"^The\s+Notice\s+of\s+the\s+\d{4}\s+(Annual\s+)?General\s+Meeting\s+of\s+Shareholders\s+on\s+the\s+Company'?s\s+website|"
            r"^To\s+inform\s+the\s+date\s+and\s+agendas?\s+for\s+\d{4}\s+Annual\s+General\s+Meeting",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM documents disclosure: {hl}",
        summary_th_template="{symbol} เผยแพร่เอกสารประชุมผู้ถือหุ้น: {hl}",
        suggested_action="No action required.",
        rationale="Pre-AGM document disclosure (notice, agenda, materials) — routine.",
    ),
    # Shareholder rights to propose agenda (pre-AGM rights notice)
    Rule(
        name="shareholder_propose_rights",
        pattern=re.compile(
            r"\bgive\s+the\s+rights?\s+of\s+Shareholders?\s+to\s+Propose\s+agenda|"
            r"\bShareholders?\s+to\s+Propose\s+(an\s+)?agenda",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} shareholder agenda-proposal rights notice: {hl}",
        summary_th_template="{symbol} เปิดให้ผู้ถือหุ้นเสนอวาระการประชุม: {hl}",
        suggested_action="No action required.",
        rationale="Pre-AGM disclosure of shareholder agenda-proposal rights — routine.",
    ),
]


# Combine in priority order: critical first, then material, then routine
_ALL_RULES: list[Rule] = _CRITICAL_RULES + _MATERIAL_RULES + _ROUTINE_RULES


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def match_rules(
    *,
    symbol: str,
    headline_en: str | None,
    headline_th: str | None = None,
) -> Classification | None:
    """Run rules against a disclosure. Returns Classification on confident match,
    None if it falls through to Haiku.

    Currently matches against the EN headline only — TH-only filings always
    fall through to Haiku since template strings differ in Thai.
    """
    if not headline_en:
        return None  # TH-only -> Haiku

    text = headline_en.strip()
    hl = text[:_HL_MAX] + ("…" if len(text) > _HL_MAX else "")

    for rule in _ALL_RULES:
        if rule.pattern.search(text):
            return Classification(
                severity=rule.severity,                          # type: ignore[arg-type]
                category=rule.category,                          # type: ignore[arg-type]
                summary_en=rule.summary_template.format(symbol=symbol, hl=hl),
                summary_th=(rule.summary_th_template or rule.summary_template).format(
                    symbol=symbol, hl=hl
                ),
                suggested_action=rule.suggested_action,
                rationale=f"[rule:{rule.name}] {rule.rationale}",
            )
    return None


def match_rules_with_diagnostics(
    *,
    symbol: str,
    headline_en: str | None,
    headline_th: str | None = None,
) -> tuple[Classification | None, str | None]:
    """Like match_rules() but also returns the rule name (or None for fall-through)."""
    if not headline_en:
        return None, None
    text = headline_en.strip()
    hl = text[:_HL_MAX] + ("…" if len(text) > _HL_MAX else "")
    for rule in _ALL_RULES:
        if rule.pattern.search(text):
            cls = Classification(
                severity=rule.severity,                          # type: ignore[arg-type]
                category=rule.category,                          # type: ignore[arg-type]
                summary_en=rule.summary_template.format(symbol=symbol, hl=hl),
                summary_th=(rule.summary_th_template or rule.summary_template).format(
                    symbol=symbol, hl=hl
                ),
                suggested_action=rule.suggested_action,
                rationale=f"[rule:{rule.name}] {rule.rationale}",
            )
            return cls, rule.name
    return None, None


def rule_count() -> int:
    return len(_ALL_RULES)
