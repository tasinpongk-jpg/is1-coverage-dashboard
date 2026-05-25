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
    # TSR / paired-security delisting — "[Month] [N], YYYY is the last trading day of TSR …"
    # Different from warrant_last_trading_day (catches -W\d patterns) and from
    # trading_sign_posted's "is the last day of trading" delisting phrasing. Empirically
    # rated critical/trading_sign by Haiku.
    Rule(
        name="last_trading_day_tsr",
        pattern=re.compile(
            r"\bis\s+the\s+last\s+trading\s+day\s+of\s+(TSR|[A-Z]+-TSR|[A-Z]+\s+and\s+[A-Z]+)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="trading_sign",
        summary_template="{symbol} last trading day of TSR notice: {hl}",
        summary_th_template="{symbol} แจ้งวันซื้อขายวันสุดท้ายของใบสำคัญแสดงสิทธิ TSR: {hl}",
        suggested_action="Open the disclosure; identify counterparties and final-settlement procedure.",
        rationale="Last trading day of TSR / paired-security notice — automatic critical per rubric.",
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
    # Senior-exec resignation (CEO/Chair/President/MD) — RESIGNATION is critical.
    # Standalone "Changing of CFO" is excluded here and handled as material in the
    # changing_of_cfo_standalone material rule, because empirically Haiku rates the
    # standalone CFO change as material (governance signal but not page-the-RM-immediately).
    Rule(
        name="exec_resignation",
        pattern=re.compile(
            r"^(Notification\s+of\s+(the\s+)?)?Resignation\s+of\s+(the\s+)?"
            r"(Chief\s+(Executive|Financial)\s+Officer|CEO|CFO|"
            r"Chairman|Chair\b|President\b|Managing\s+Director)|"
            r"^Changing\s+of\s+(CEO|Chief\s+Executive\s+Officer)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="director_mgmt_change",
        summary_template="Senior-exec resignation / change at {symbol}: {hl}",
        summary_th_template="ผู้บริหารระดับสูง {symbol} ลาออก/เปลี่ยนแปลง: {hl}",
        suggested_action="Call IR within the hour; check for related operational issues or pending disclosures.",
        rationale="Unexpected CEO/CFO resignation or CEO change — automatic critical per rubric.",
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
    # BOD / Board Meeting resolutions bundled with No Dividend / capital change.
    # Accepts "BOD Meeting" or "Board Meeting" or "Board of Directors' Meeting".
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
    # Clarification regarding auditor disclaimer / qualified opinion / going concern
    Rule(
        name="clarification_auditor_disclaimer",
        pattern=re.compile(
            r"^Clarification\s+regarding\s+the\s+auditor'?s\s+report\s+"
            r"(disclaiming|qualifying|with\s+(a\s+)?(disclaimer|qualified))",
            re.IGNORECASE,
        ),
        severity="critical",
        category="auditor_change",
        summary_template="{symbol} clarification on auditor disclaimer/qualified opinion: {hl}",
        summary_th_template="{symbol} คำชี้แจงเรื่องผู้สอบบัญชีไม่แสดงความเห็น/แสดงความเห็นแบบมีเงื่อนไข: {hl}",
        suggested_action="Open the disclosure immediately; read the disclaimer text in full; check for restatement risk; brief desk before market open.",
        rationale="Clarification on auditor disclaimer / qualified opinion — automatic critical (financial-statement reliability red flag).",
    ),
    # Clarification on SEC News release (issuer-side response to SEC news item)
    Rule(
        name="clarification_sec_news_release",
        pattern=re.compile(
            r"^Clarification\s+Regarding\s+the\s+Securities\s+and\s+Exchange\s+Commission'?s\s+News\s+Release",
            re.IGNORECASE,
        ),
        severity="critical",
        category="set_clarification",
        summary_template="{symbol} clarification on SEC News release: {hl}",
        summary_th_template="{symbol} คำชี้แจงต่อข่าวจากสำนักงาน ก.ล.ต.: {hl}",
        suggested_action="Open the disclosure and the underlying SEC news release before market open; brief sector head.",
        rationale="Clarification triggered by an SEC News release — treat as critical per rubric.",
    ),
    # BOD resolution bundled with a Connected Transaction approval (RPT acquisition/disposal)
    Rule(
        name="bod_resolution_connected_transaction",
        pattern=re.compile(
            r"^Notification\s+Of\s+Board\s+Resolution\s+Regarding\s+The\s+Approval\s+Of\s+A\s+Connected\s+Transaction|"
            r"^Notification\s+of\s+the\s+Resolutions\s+of\s+the\s+BOD\s+No\..*\b(Related\s+Company|Connected\s+Person|Disposal\s+of\s+(the\s+)?warehouse)",
            re.IGNORECASE,
        ),
        severity="critical",
        category="connected_transaction",
        summary_template="{symbol} BOD-approved connected-party transaction: {hl}",
        summary_th_template="{symbol} มติคณะกรรมการอนุมัติรายการที่เกี่ยวโยงกัน: {hl}",
        suggested_action="Open the resolution PDF; check counterparty, valuation, IFA opinion, and shareholder-meeting requirement.",
        rationale="BOD resolution approving a connected/related-party transaction — automatic critical.",
    ),
    # BOD bundled resolution naming a specific share acquisition (asset acquisition) as the headline driver.
    Rule(
        name="bod_resolution_share_acquisition",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+BOD\s+Meeting\s+No\..*\bre:\s*Share\s+Acquisition\s+in\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="ma_acquisition_disposal",
        summary_template="{symbol} BOD resolution approving share acquisition: {hl}",
        summary_th_template="{symbol} มติคณะกรรมการอนุมัติเข้าซื้อหุ้น: {hl}",
        suggested_action="Open the resolution PDF; size the acquisition vs total assets; identify counterparty and connected-party flags.",
        rationale="BOD resolution approving a share/asset acquisition — material M&A action, escalate.",
    ),
    # BOD bundled resolution headline that names a Capital Reduction / Increase action explicitly
    Rule(
        name="bod_resolution_capital_action",
        pattern=re.compile(
            r"^Notification\s+of\s+Board\s+Meeting\s+No\..*\bResolutions:.*\b("
            r"Capital\s+Reduction|Capital\s+Increase|Capital\s+Reduction\s+and\s+Increase|"
            r"No\s+Dividend)\b",
            re.IGNORECASE,
        ),
        severity="critical",
        category="capital_change",
        summary_template="{symbol} BOD bundled resolution (capital action / no dividend): {hl}",
        summary_th_template="{symbol} มติคณะกรรมการ (ลด/เพิ่มทุน หรือ งดปันผล): {hl}",
        suggested_action="Read the full BOD resolution; quantify cumulative capital impact and dividend driver.",
        rationale="BOD bundled resolution naming capital reduction/increase or no-dividend — critical.",
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
    # F45 financial performance — covers Reviewed/Audited/Unreviewed/Revised forms.
    # The "Reviewed " prefix is the lowercased-headline variant SET emits at quarter-end
    # (auditors only review, not audit, between annual filings). Without it, Haiku had
    # been picking up "Reviewed financial performance quarter 1 (F45)" — promoted to a rule.
    # Also handles SET's "Audited Yearly financial performance (F45)" word-order variant
    # where the period qualifier ("Yearly"/"Quarter N") sits BETWEEN the audit prefix and
    # "financial performance".
    Rule(
        name="financial_performance_f45",
        pattern=re.compile(
            r"^(Audited\s+|Unreviewed\s+|Reviewed\s+)?"
            r"((Yearly|Quarter(\s+\d)?)\s+)?"
            r"(Financial\s+Performance(\s+(Quarter|Yearly))?|"
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
    # Operating Result Quarter N Ending DD MMM YYYY — same materiality as the F45
    # variant; some funds/issuers use this phrasing instead of "Financial Performance".
    Rule(
        name="operating_result_quarterly",
        pattern=re.compile(
            r"^Operating\s+Result\s+(Quarter|Yearly)\b",
            re.IGNORECASE,
        ),
        severity="material",
        category="earnings",
        summary_template="{symbol} filed quarterly/yearly operating result: {hl}",
        summary_th_template="{symbol} เผยแพร่ผลการดำเนินงานรายไตรมาส/ประจำปี: {hl}",
        suggested_action="Pull the figures vs prior period; flag any 20%+ swings for clarification check.",
        rationale="Operating-result periodic report — material per rubric.",
    ),
    # Financial Statement (the full Reviewed/Audited statements). Includes the
    # "Separated " and "Consolidated " prefixes SET uses to distinguish parent-only
    # vs. group statements — both are the same material event for our purposes.
    Rule(
        name="financial_statement",
        pattern=re.compile(
            r"^(Separated\s+|Consolidated\s+)?Financial\s+Statement\s+(Quarter|Yearly)\b",
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
    # BOD-resolution headline naming dividend payment + AGM schedule (material/dividend).
    # Distinct from `bod_dividend_declaration` above (which captures the pure "regarding
    # the payment of dividend" phrasing). This catches the longer "BOD's Meeting regarding
    # the dividend payment, and the schedule of the AGM" / "Resolutions of BOD's meeting
    # regarding Date and Agenda of AGM and Dividend Payment" / "Resolutions of the Board
    # of Directors Meeting No. ... Set up the AGM ... and Dividend Payment" family.
    # Negative lookahead excludes dividend-omission/suspension phrasings (those are critical
    # and handled by the dividend_omission / bod_no_dividend rules above).
    Rule(
        name="bod_resolution_dividend_agm_schedule",
        pattern=re.compile(
            r"^(?!.*\b(omission\s+of|omit\s+|Suspension\s+of|No\s+Dividend)\b)"
            r"(Notification\s+of\s+(the\s+)?resolution(s)?\s+of\s+(the\s+)?(BOD'?s\s+|Board\s+of\s+Directors'?\s+)?Meeting|"
            r"Resolutions?\s+of\s+(the\s+)?Board\s+of\s+Directors'?\s+meeting|"
            r"(The\s+)?[Rr]esolution\s+of\s+(the\s+)?Board\s+of\s+Directors(\s+regarding|\s+Meeting\s+No)|"
            r"Notification\s+of\s+the\s+resolution\s+again,?\s+Meeting\s+No)"
            r".*\b(dividend\s+payment|Dividend\s+Payment|Non-Annual\s+dividend\s+payment|"
            r"payment\s+of\s+(an?\s+)?dividend)\b",
            re.IGNORECASE,
        ),
        severity="material",
        category="dividend",
        summary_template="{symbol} BOD resolution (dividend + AGM schedule): {hl}",
        summary_th_template="{symbol} มติคณะกรรมการเกี่ยวกับเงินปันผลและกำหนดประชุมผู้ถือหุ้น: {hl}",
        suggested_action="Read the resolution; note dividend amount, X-D date proxy, and calendar the AGM.",
        rationale="BOD resolution bundling dividend payment with AGM scheduling — material per rubric.",
    ),
    # BOD resolution headline naming appointment of subcommittees / directors / executives
    # (Material catch-all for BOD-meeting director/exec composition changes).
    Rule(
        name="bod_resolution_director_subcommittee",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+Resolutions\s+of\s+the\s+Board\s+of\s+Directors'?\s+Meeting\s+"
            r"No\.\s*\d+/\d+\s+regarding\s+the\s+appointment\s+of\s+(subcommittees'?\s+members|"
            r"director|directors|executives|Sub-?Committees|Audit\s+Committee)",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} BOD resolution on subcommittee/director appointment: {hl}",
        summary_th_template="{symbol} มติคณะกรรมการเรื่องแต่งตั้งกรรมการชุดย่อย/กรรมการ: {hl}",
        suggested_action="Note the appointment; check independence and committee composition.",
        rationale="BOD resolution on subcommittee/director appointment — material governance event.",
    ),
    # Notification of Director's Resignation and Appointment — combined event, material.
    Rule(
        name="director_resignation_and_appointment",
        pattern=re.compile(
            r"^Notification\s+of\s+(the\s+)?Director'?s\s+Resignation\s+and\s+Appointment",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} director resignation and replacement appointment: {hl}",
        summary_th_template="{symbol} กรรมการลาออกและแต่งตั้งทดแทน: {hl}",
        suggested_action="Identify outgoing vs incoming; check committee/independence implications.",
        rationale="Director resignation paired with appointment — material governance change.",
    ),
    # Appointment of Chairman of Audit Committee / Nomination Committee — governance signal.
    Rule(
        name="appointment_chairman_committee",
        pattern=re.compile(
            r"^Notification\s+of\s+(the\s+)?Appointment\s+of\s+(the\s+)?Chairman\s+of\s+"
            r"(the\s+)?(Audit\s+Committee|Nomination(\s+and\s+Remuneration)?\s+Committee)",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} chairman appointment to a key committee: {hl}",
        summary_th_template="{symbol} แต่งตั้งประธานคณะกรรมการชุดย่อย: {hl}",
        suggested_action="Note the chairman appointment; check tenure and prior committee role.",
        rationale="Chairman appointment to Audit / Nomination & Remuneration committee — material governance event.",
    ),
    # Appointment of senior executives + change of Person Responsible for Accounting/Finance
    Rule(
        name="senior_exec_appointment_acct",
        pattern=re.compile(
            r"^Appointment\s+of\s+Senior\s+Executives?\s+and\s+Change\s+of\s+the\s+Person\s+Responsible\s+for\s+Accounting",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} senior-exec + accounting-officer change: {hl}",
        summary_th_template="{symbol} แต่งตั้งผู้บริหารและเปลี่ยนผู้รับผิดชอบสายบัญชี: {hl}",
        suggested_action="Identify outgoing vs incoming; check accounting-officer tenure implications.",
        rationale="Senior-exec appointment paired with accounting-officer change — material governance event.",
    ),
    # Changing of CFO (standalone, no "Notification" wrapper). The exec_resignation rule
    # in CRITICAL covers "Changing of CEO/CFO" but only when prefixed by the trigger.
    # Standalone "Changing of CFO" is empirically material (succession often signaled).
    Rule(
        name="changing_of_cfo_standalone",
        pattern=re.compile(
            r"^Changing\s+of\s+CFO\s*$",
            re.IGNORECASE,
        ),
        severity="material",
        category="director_mgmt_change",
        summary_template="{symbol} CFO change: {hl}",
        summary_th_template="{symbol} เปลี่ยนแปลง CFO: {hl}",
        suggested_action="Note the CFO change; check successor's background and effective date.",
        rationale="Standalone CFO change notification — material governance event per rubric.",
    ),
    # Issuance of Debentures — material capital action.
    Rule(
        name="issuance_of_debentures",
        pattern=re.compile(
            r"^Issuance\s+of\s+Debentures\s*$",
            re.IGNORECASE,
        ),
        severity="material",
        category="capital_change",
        summary_template="{symbol} issuance of debentures: {hl}",
        summary_th_template="{symbol} ออกหุ้นกู้: {hl}",
        suggested_action="Read the disclosure; size the debenture vs existing leverage and capture use-of-proceeds.",
        rationale="Debenture issuance — material capital action per rubric.",
    ),
    # Share Repurchase INITIAL reporting form (first/no-ordinal filing, marks program kickoff).
    # Material per rubric — this is the formal "Report on Repurchase of Shares" / "Reporting
    # Share Repurchase Form" filing without the periodic ordinal qualifier. The follow-on
    # periodic filings ("Reporting The Second/Third/Fourth Share Repurchase form...") are
    # handled as a separate routine rule below to match Haiku's empirical labeling.
    Rule(
        name="share_repurchase_form_report",
        pattern=re.compile(
            r"^(Report(ing)?\s+(on\s+(Repurchase\s+of\s+Shares|the\s+First\s+Share\s+Repurchase)|"
            r"Share\s+Repurchase\s+Form)\s+for\s+[Ff]inancial\s+[Mm]anagement\s+[Pp]urpose|"
            r"^Reporting\s+The\s+First\s+Share\s+Repurchase\s+form\s+for\s+financial\s+management\s+purpose)",
            re.IGNORECASE,
        ),
        severity="material",
        category="capital_change",
        summary_template="{symbol} share repurchase initial reporting form: {hl}",
        summary_th_template="{symbol} รายงานการซื้อหุ้นคืนครั้งแรกเพื่อบริหารทางการเงิน: {hl}",
        suggested_action="Note the cumulative shares repurchased and remaining authorization.",
        rationale="Initial share-repurchase reporting form (financial management) — material per rubric.",
    ),
    # Investment-project approval (typically a capex investment in a new facility).
    Rule(
        name="investment_project_approval",
        pattern=re.compile(
            r"^To\s+Inform\s+the\s+Approving\s+an\s+Investment\s+Project",
            re.IGNORECASE,
        ),
        severity="material",
        category="ma_acquisition_disposal",
        summary_template="{symbol} investment-project approval: {hl}",
        summary_th_template="{symbol} อนุมัติโครงการลงทุน: {hl}",
        suggested_action="Open the disclosure; size the project capex, identify counterparty and timeline.",
        rationale="Approval of a new investment project — material per rubric.",
    ),
    # Contract signing for a major construction project — material business event.
    Rule(
        name="contract_signing_construction",
        pattern=re.compile(
            r"^Notification\s+on\s+the\s+Contract\s+Signing\s+for\s+(the\s+)?Construction",
            re.IGNORECASE,
        ),
        severity="material",
        category="ma_acquisition_disposal",
        summary_template="{symbol} construction-contract signing: {hl}",
        summary_th_template="{symbol} ลงนามสัญญาก่อสร้างโครงการ: {hl}",
        suggested_action="Open the disclosure; capture project value, counterparty, and completion timeline.",
        rationale="Major construction-contract signing — material business win per rubric.",
    ),
    # AGM-resolution variant phrasings ("Notification on the Resolutions of the AGM ..." and
    # "Notification of Resolutions of the AGM ..."). The existing shareholders_resolution
    # rule catches "Notification of the resolutions of the AGM" — these two prefix variants
    # ("Notification ON" and "Notification of Resolutions [no 'the']") need their own catch.
    Rule(
        name="agm_resolution_notification_variants",
        pattern=re.compile(
            r"^Notification\s+(on\s+the|of)\s+Resolutions?\s+of\s+(the\s+)?(\d{4}\s+)?"
            r"Annual\s+General\s+Meeting\s+of\s+Shareholders",
            re.IGNORECASE,
        ),
        severity="material",
        category="agm_resolution",
        summary_template="{symbol} AGM resolutions: {hl}",
        summary_th_template="{symbol} มติที่ประชุมสามัญผู้ถือหุ้น: {hl}",
        suggested_action="Read the resolutions list; flag any capital, dividend, or related-party items.",
        rationale="AGM resolution release (variant phrasing) — material per rubric.",
    ),
    # "Disclosure Minute of the AGM" / "Determination of meeting date and agenda" - material
    # AGM resolution variants. Skipping minute publication conflict by anchoring tightly.
    Rule(
        name="agm_resolution_disclosure_minute",
        pattern=re.compile(
            r"^Disclosure\s+Minute\s+of\s+(the\s+)?(\d{4}\s+)?Annual\s+General\s+Meeting\s+of\s+Shareholders",
            re.IGNORECASE,
        ),
        severity="material",
        category="agm_resolution",
        summary_template="{symbol} AGM minutes (resolution-bearing): {hl}",
        summary_th_template="{symbol} เปิดเผยมติที่ประชุมสามัญผู้ถือหุ้น: {hl}",
        suggested_action="Read the resolutions; flag any material capital, dividend or related-party items.",
        rationale="AGM 'Disclosure Minute' phrasing — empirically material per rubric.",
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
    # Warrant exercise result (F53-5) — empirically Haiku labels these warrant_exercise
    # not regulatory_filing. Split the rule: "Exercise of [TICKER]-W" goes to
    # warrant_exercise; "sale of common shares" stays as regulatory_filing.
    Rule(
        name="warrant_exercise_result",
        pattern=re.compile(
            r"^Report\s+on\s+the\s+results\s+of\s+the\s+Exercise\s+of\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="warrant_exercise",
        summary_template="{symbol} warrant exercise result (F53-5): {hl}",
        summary_th_template="{symbol} รายงานผลการใช้สิทธิวอร์แรนต์: {hl}",
        suggested_action="Note the take-up rate; no immediate action.",
        rationale="F53-5 warrant-exercise result filing — routine warrant_exercise per rubric.",
    ),
    # F53-5 result of share-sale (PP / RO / ESOP) — separate routine/regulatory_filing path.
    Rule(
        name="share_sale_result_f53",
        pattern=re.compile(
            r"^Report\s+on\s+the\s+results\s+of\s+sale\s+of\s+common\s+shares",
            re.IGNORECASE,
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} share-issue result (F53-5): {hl}",
        summary_th_template="{symbol} รายงานผลการเสนอขายหุ้น: {hl}",
        suggested_action="Note the take-up rate; no immediate action.",
        rationale="F53-5 share-sale result filing — routine regulatory cadence.",
    ),
    # New shares listing (post-warrant, post-RO, etc.) — empirically Haiku consistently
    # labels these capital_change, not regulatory_filing (this is a balance-sheet event
    # for the issuer rather than a procedural filing).
    Rule(
        name="new_shares_listing",
        pattern=re.compile(
            r"^New\s+shares\s+of\s+\S+\s+to\s+be\s+traded\s+on",
            re.IGNORECASE,
        ),
        severity="routine",
        category="capital_change",
        summary_template="{symbol} new shares listing: {hl}",
        summary_th_template="{symbol} หุ้นใหม่เริ่มซื้อขาย: {hl}",
        suggested_action="No action required.",
        rationale="Standard new-shares listing notice (post-exercise/RO) — routine capital_change.",
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
    # Periodic daily share-repurchase reports. Distinct from the share_repurchase_program
    # rule (which catches the START / END / resolution events as MATERIAL). The
    # daily "Shares Repurchased Report dated X" cadence is operational logging.
    Rule(
        name="shares_repurchased_daily_report",
        pattern=re.compile(
            r"^Shares\s+Repurchased\s+Report\s+dated\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="capital_change",
        summary_template="{symbol} daily share-repurchase report: {hl}",
        summary_th_template="{symbol} รายงานการซื้อหุ้นคืนประจำวัน: {hl}",
        suggested_action="No action required; daily repurchase log.",
        rationale="Daily share-repurchase report during an open program — routine cadence.",
    ),
    # PFREIT NAV-per-unit periodic report. The PFREIT rubric in the system prompt
    # explicitly calls scheduled NAV updates routine.
    Rule(
        name="nav_per_unit_report",
        pattern=re.compile(
            r"^Report\s+(on\s+)?NAV(\s+per\s+unit)?\s+as\s+of\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} periodic NAV-per-unit report: {hl}",
        summary_th_template="{symbol} รายงานมูลค่าทรัพย์สินสุทธิต่อหน่วยลงทุน: {hl}",
        suggested_action="Note the NAV; periodic disclosure logged.",
        rationale="Scheduled REIT/PF NAV-per-unit disclosure — routine per PFREIT rubric.",
    ),
    # Book-closing date for unitholder voting (separate from book-closed-for-dividend rule
    # above, which is dividend-specific). This is the pre-vote register closure.
    Rule(
        name="register_book_closing_unitholder_vote",
        pattern=re.compile(
            r"^Notification\s+of\s+(the\s+)?Closing\s+Date\s+of\s+Register\s+Book\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} register book-closing date notification: {hl}",
        summary_th_template="{symbol} แจ้งกำหนดวันปิดสมุดทะเบียน: {hl}",
        suggested_action="Calendar the closing date.",
        rationale="Register-book closing-date notification for upcoming vote/distribution — routine.",
    ),
    # "No Right Adjustment of [TICKER]-W[N]" — affirmative no-op event paired with a
    # dividend that wasn't large enough to trigger an adjustment. Pairs with the existing
    # warrant_right_adjustment rule.
    Rule(
        name="warrant_no_right_adjustment",
        pattern=re.compile(
            r"^No\s+Right\s+Adjustment\s+of\s+\S+-W\d",
            re.IGNORECASE,
        ),
        severity="routine",
        category="warrant_exercise",
        summary_template="{symbol} warrant no-right-adjustment confirmation: {hl}",
        summary_th_template="{symbol} ยืนยันไม่มีการปรับสิทธิวอร์แรนต์: {hl}",
        suggested_action="No action required; mechanical no-op confirmation.",
        rationale="Confirmation that a recent dividend did not trigger warrant right adjustment — routine.",
    ),
    # Warrant expiry / last trading day. Word order distinct from the critical
    # trading_sign rule's "is the last day of trading" (delisting).
    Rule(
        name="warrant_last_trading_day",
        pattern=re.compile(
            r"\bis\s+the\s+last\s+trading\s+day\s+of\s+\S+-W\d",
            re.IGNORECASE,
        ),
        severity="routine",
        category="warrant_exercise",
        summary_template="{symbol} warrant last-trading-day notice: {hl}",
        summary_th_template="{symbol} แจ้งวันซื้อขายวันสุดท้ายของวอร์แรนต์: {hl}",
        suggested_action="Note expiry; no action required.",
        rationale="Routine warrant-expiry / last-trading-day notification — mechanical.",
    ),
    # Bondholders' meeting notification (debenture investors)
    Rule(
        name="bondholders_meeting_notification",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+\d+/\d+\s+Bondholders'?\s+Meeting",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} bondholders' meeting notification: {hl}",
        summary_th_template="{symbol} แจ้งประชุมผู้ถือหุ้นกู้: {hl}",
        suggested_action="Calendar the bondholder-meeting date if material to credit position.",
        rationale="Bondholders' meeting notification — routine for equity-focused coverage.",
    ),
    # Periodic share-repurchase reports (THE Second / Third / Fourth / Fifth / etc.) —
    # the recurring filing during an open program. Distinct from share_repurchase_form_report
    # above (the initial filing, material). Empirically Haiku rates these as routine.
    Rule(
        name="share_repurchase_periodic_report",
        pattern=re.compile(
            r"^Reporting\s+The\s+(Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|\d+(st|nd|rd|th))\s+"
            r"Share\s+Repurchase\s+form\s+for\s+financial\s+management\s+purpose",
            re.IGNORECASE,
        ),
        severity="routine",
        category="capital_change",
        summary_template="{symbol} periodic share-repurchase report: {hl}",
        summary_th_template="{symbol} รายงานความคืบหน้าการซื้อหุ้นคืน: {hl}",
        suggested_action="No action required; periodic cadence under an existing repurchase program.",
        rationale="Periodic (2nd/3rd/…) share-repurchase reporting form — routine cadence.",
    ),
    # "Report NAV as at <date>" — extends the existing nav_per_unit_report rule which
    # only catches "as of". Cluster majority is info_memo (6/10 = 60%); intentionally
    # accepting the 4 intra-cluster category disagreements to recover 6+ agree wins.
    Rule(
        name="nav_report_as_at",
        pattern=re.compile(
            r"^Report\s+NAV\s+as\s+at\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} periodic NAV report: {hl}",
        summary_th_template="{symbol} รายงานมูลค่าทรัพย์สินสุทธิ: {hl}",
        suggested_action="Note the NAV; periodic disclosure logged.",
        rationale="Scheduled REIT/PF NAV disclosure (Report NAV as at) — routine per PFREIT rubric.",
    ),
    # "Net Asset Value per Unit Report as at" — explicit longer-form NAV header used by
    # some sub-funds. Cluster majority info_memo (4/6 = 67%); accepts 2 intra-cluster
    # category disagreements to recover 4 agree wins.
    Rule(
        name="nav_per_unit_report_as_at",
        pattern=re.compile(
            r"^Net\s+Asset\s+Value\s+per\s+Unit\s+Report\s+as\s+at\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} periodic NAV-per-unit report: {hl}",
        summary_th_template="{symbol} รายงานมูลค่าทรัพย์สินสุทธิต่อหน่วยลงทุน: {hl}",
        suggested_action="Note the NAV; periodic disclosure logged.",
        rationale="Scheduled REIT/PF NAV-per-unit (long-form) disclosure — routine per PFREIT rubric.",
    ),
    # AGM minutes phrasings that cluster to routine/agm_resolution (rather than other) —
    # "Submission of Minutes" and "Disclosure of the Minutes of Meeting of the AGM" forms.
    # Cluster majority agm_resolution; 50-67% within-cluster category agreement so a few
    # intra-cluster disagreements are accepted in exchange for the agree wins.
    Rule(
        name="agm_minutes_agm_resolution",
        pattern=re.compile(
            r"^(Submission\s+of\s+(the\s+)?[Mm]inutes\s+of\s+(the\s+)?(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"Disclosure\s+of\s+(the\s+)?[Mm]inutes\s+of\s+Meeting\s+of\s+the\s+(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"Disclosure\s+of\s+[Mm]inutes\s+of\s+the\s+(\d{4}\s+)?Annual\s+General\s+Meeting)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="agm_resolution",
        summary_template="{symbol} AGM minutes (resolution-doc emphasis): {hl}",
        summary_th_template="{symbol} เปิดเผยรายงานการประชุมผู้ถือหุ้น (มติ): {hl}",
        suggested_action="No action required; resolution-document archive.",
        rationale="AGM minutes (resolution-document phrasing) — routine/agm_resolution per cluster.",
    ),
    # AGM minutes — broad catch-all phrasings that empirically cluster to routine/other.
    # Pairs with the existing `agm_minutes` rule (canonical Publication/Disclosure of
    # Minutes form) and `agm_minutes_notification`. Excludes the Submission of Minutes
    # and Disclosure of Minutes of Meeting forms (those are agm_resolution per cluster).
    Rule(
        name="agm_minutes_broad",
        pattern=re.compile(
            r"^(Announcement\s+of\s+(the\s+)?(M|m)inutes\s+(the\s+|of\s+the\s+)?(\d{4}\s+|No\.\s*\d+/\d+\s+)?(on\s+)?(the\s+Company)?Annual\s+General\s+Meeting|"
            r"Dissemination\s+of\s+(the\s+|of\s+)?[Mm]inutes\s+of\s+(the\s+)?(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"To\s+notify\s+the\s+publication\s+of\s+the\s+[Mm]inutes\s+of\b|"
            r"Notification\s+of\s+Disclosure\s+of\s+(the\s+)?[Mm]inutes\s+of\s+the\s+(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"The\s+[Dd]isclosure\s+of\s+(The|the)\s+[Mm]inutes\s+of\s+the\s+(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"Dissemination\s+of\s+the\s+[Mm]inutes\s+of\s+the\s+(\d{4}\s+)?Two-?way\s+Communication)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM/EGM minutes published: {hl}",
        summary_th_template="{symbol} เผยแพร่รายงานการประชุมผู้ถือหุ้น: {hl}",
        suggested_action="No action required; minutes archived for the meeting.",
        rationale="Post-meeting minutes publication (broad phrasings) — routine.",
    ),
    # NOTE: "Submission of Minutes" / "Disclosure of the Minutes of Meeting of the AGM"
    # phrasings (cluster majority routine/agm_resolution) intentionally NOT promoted —
    # the 50-67% intra-cluster category agreement makes any rule emit too many
    # disagreements. They fall through to LLM until they reach a tighter cluster.
    # Routine notification of a single AGM resolution (not the full set) — the cluster
    # "notification of the resolution of the annual general" was 5 rows all rated
    # routine/agm_resolution, single-resolution-style notice (e.g. dividend confirmation)
    # rather than a full resolutions release.
    Rule(
        name="agm_single_resolution_routine",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+[Rr]esolution\s+of\s+(the\s+)?(\d{4}\s+)?Annual\s+General\s+Meeting\s+of\s+Shareholders\s*("
            r"for\s+the\s+year\s+\d{4})?\s*$",
            re.IGNORECASE,
        ),
        severity="routine",
        category="agm_resolution",
        summary_template="{symbol} single AGM resolution notification: {hl}",
        summary_th_template="{symbol} แจ้งมติที่ประชุมสามัญผู้ถือหุ้น (มติเดี่ยว): {hl}",
        suggested_action="No action required; single-item resolution logged.",
        rationale="Single-resolution AGM notification — routine per rubric.",
    ),
    # Two-way communication schedule / dissemination of the related report / Q&A summaries
    # All PFREIT routine cadence for the annual unitholder report.
    Rule(
        name="two_way_communication_schedule",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+[Ss]chedul(e|ing)\s+(for|of)\s+(the\s+\d{4}\s+|the\s+)?[Tt]wo-?\s*[Ww]ay\s+[Cc]ommunication|"
            r"^Notification\s+of\s+the\s+Dissemination\s+of\s+the\s+Report\s+for\s+the\s+(\d{4}\s+)?Two-?way\s+Communication",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} two-way communication schedule/dissemination: {hl}",
        summary_th_template="{symbol} กำหนดการสื่อสารแบบ Two-way: {hl}",
        suggested_action="No action required; periodic unitholder-communication cadence.",
        rationale="REIT/PF annual two-way unitholder communication schedule — routine per rubric.",
    ),
    # Two-way communication Q&A / summary of significant matters / questions and answers
    # All PFREIT routine unitholder Q&A cadence.
    Rule(
        name="two_way_communication_qa",
        pattern=re.compile(
            r"^(Notification\s+of\s+the\s+result\s+of\s+questions\s+received\s+in|"
            r"Notification\s+of\s+summary\s+of\s+significant\s+(matters|questions)\b|"
            r"Notification\s+on\s+the\s+Results\s+of\s+the\s+Opening\s+for\s+Questions|"
            r"Summary\s+of\s+questions\s+and\s+answers\s+by\s+two\s*-\s*way\s+communication|"
            r"Summary\s+of\s+significant\s+(I|i)ssues\s+by\s+way\s+of\s+questions\s+and\s+answers|"
            r"Disclosure\s+of\s+the\s+summary\s+of\s+questions\s+and\s+answers|"
            r"Disclosure\s+of\s+question\s+and\s+answer\s+from\s+Question\s+Form)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} two-way communication Q&A summary: {hl}",
        summary_th_template="{symbol} สรุปคำถามคำตอบจากการสื่อสาร Two-way: {hl}",
        suggested_action="No action required; periodic unitholder Q&A log.",
        rationale="REIT/PF two-way communication Q&A summary — routine per rubric.",
    ),
    # Dividend / distribution payment + book closing date (REIT/Fund periodic distributions).
    # Pairs with the existing reit_distribution rule (which only matches "distribution
    # payment for the period"). This covers the additional phrasings.
    Rule(
        name="fund_dividend_payment_routine",
        pattern=re.compile(
            r"^(Announcement\s+for\s+Dividend\s+Payment\s+and\s+(the\s+)?Record\s+Date|"
            r"Notification\s+of\s+the\s+dividend\s+payment\s+and\s+book\s+closing\s+date|"
            r"Notification\s+of\s+the\s+Distribution\s+of\s+Returns\s+Payment\s+and\s+Book\s+Closing\s+Date|"
            r"Notification\s+of\s+Distributed?\s+Payment(\s+no\.?\s*\d+/\d+)?\s+and\s+book\s+closing\s+date|"
            r"Notification\s+of\s+Distribution\s+Payment\s+and\s+Book\s+Closing\s+Date|"
            r"Notification\s+of\s+distribution\s+payment\s+of\b|"
            r"Notification\s+of\s+distribution\s+of\s+(WHA|CPN|Issara|Axtra|Sub\s+Sri\s+Thai|the)\b|"
            r"Notification\s+of\s+Distribution\s+of\s+Returns\s+of\b|"
            r"Notification\s+of\s+Distribution\s+of\s+Returns\s+and\s+the\s+\d{4}\s+Two-?Way|"
            r"Notification\s+of\s+Interim\s+Distribution\s+Payment\b|"
            r"Notification\s+of\s+Dividend\s+Payment\s*$|"
            r"Publication\s+of\s+the\s+dividend\s+payment\s+on\s+the\s+Company'?s\s+website\s*$)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="dividend",
        summary_template="{symbol} fund/REIT distribution payment notice: {hl}",
        summary_th_template="{symbol} แจ้งจ่ายผลประโยชน์ตอบแทน/เงินปันผล: {hl}",
        suggested_action="No action required; scheduled distribution logged.",
        rationale="Scheduled REIT/fund distribution / dividend payment notice — routine per PFREIT rubric.",
    ),
    # Top-N major unitholders (already-listed funds, routine periodic register)
    Rule(
        name="major_unitholders_announcement",
        pattern=re.compile(
            r"^Announcement\s+of\s+(\d+\s+Major|the\s+first\s+\d+)\s+[Uu]nit(\s|-)?[Hh]olders|"
            r"^Announcement\s+of\s+the\s+first\s+\d+\s+unit\s+holders",
            re.IGNORECASE,
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} major unitholders disclosure: {hl}",
        summary_th_template="{symbol} รายชื่อผู้ถือหน่วยลงทุนรายใหญ่: {hl}",
        suggested_action="No action required; periodic register disclosure.",
        rationale="Routine major-unitholder register disclosure for funds.",
    ),
    # Details of Assets — narrow to the "Details of Assets" (plural, no date) form only.
    # The "Details of Asset as of <date>" variant has 33% LLM disagreement on category
    # (regulatory_filing vs information_memo) so we leave it unclassified.
    Rule(
        name="details_of_assets",
        pattern=re.compile(
            r"^Details\s+of\s+Assets\s*$|"
            r"^Details\s+of\s+(LH|WHA|CPN|MFC|the)\s+\S+.*Real\s+Estate\s+Investment\s+Trust",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} fund asset details: {hl}",
        summary_th_template="{symbol} รายละเอียดทรัพย์สินของกองทุน: {hl}",
        suggested_action="No action required; periodic asset details logged.",
        rationale="Periodic REIT/fund asset-details disclosure (clean variant) — routine per PFREIT rubric.",
    ),
    # AGM postponement / cancellation / rescheduling notices (routine logistical)
    Rule(
        name="agm_postponement_cancellation",
        pattern=re.compile(
            r"^Notification\s+of\s+(postponement|Cancellation)\s+of\s+(the\s+)?(\d{4}\s+|Previously\s+Scheduled\s+Date\s+for\s+the\s+\d{4}\s+)?Annual\s+General\s+Meeting",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM postponement/cancellation notice: {hl}",
        summary_th_template="{symbol} แจ้งเลื่อน/ยกเลิกประชุมสามัญผู้ถือหุ้น: {hl}",
        suggested_action="Update the AGM calendar; no immediate action.",
        rationale="AGM postponement/cancellation — routine logistical change.",
    ),
    # Subsidiary establishment (non-material, e.g. small SPVs) — empirically Haiku
    # consistently labels these routine when the headline is the plain "establishment of
    # subsidiary company" form (no acquisition / connected-party qualifier).
    Rule(
        name="subsidiary_establishment_routine",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+establishment\s+of\s+subsidiary\s+company\s*$",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} subsidiary establishment notice: {hl}",
        summary_th_template="{symbol} แจ้งการจัดตั้งบริษัทย่อย: {hl}",
        suggested_action="No action required; small SPV / subsidiary established.",
        rationale="Plain subsidiary-establishment notice (no acquisition qualifier) — routine per rubric.",
    ),
    # Head office relocation — routine operational
    Rule(
        name="head_office_relocation",
        pattern=re.compile(
            r"^Notification\s+of\s+Head\s+Office\s+Relocation",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} head office relocation: {hl}",
        summary_th_template="{symbol} แจ้งย้ายสำนักงานใหญ่: {hl}",
        suggested_action="No action required; operational change.",
        rationale="Head-office relocation — routine operational notice.",
    ),
    # Roadshow presentation disclosure (IR material publishing)
    Rule(
        name="roadshow_presentation",
        pattern=re.compile(
            r"^Disclosure\s+of\s+the\s+Roadshow\s+Presentation\s+on\s+the\s+Company'?s\s+Website",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} roadshow presentation disclosed: {hl}",
        summary_th_template="{symbol} เผยแพร่เอกสารโรดโชว์บนเว็บไซต์บริษัท: {hl}",
        suggested_action="No action required; IR material logged.",
        rationale="Roadshow-presentation website publication — routine IR cadence.",
    ),
    # Final-exercise + suspension request (warrant winding down)
    Rule(
        name="warrant_final_exercise_suspension",
        pattern=re.compile(
            r"^Notification\s+the\s+final\s+exercise\s+and\s+request\s+for\s+suspension\s+of\s+\S+-W\d",
            re.IGNORECASE,
        ),
        severity="routine",
        category="warrant_exercise",
        summary_template="{symbol} warrant final exercise / suspension request: {hl}",
        summary_th_template="{symbol} แจ้งการใช้สิทธิครั้งสุดท้ายและขอพักการซื้อขายวอร์แรนต์: {hl}",
        suggested_action="No action required; warrant winding down.",
        rationale="Final-exercise + suspension request for warrant — routine wind-down.",
    ),
    # Publication of the Minutes of AGM — additional phrasings (Uploading of the Minutes,
    # Publicity of the minutes, Disseminate of the minutes, the plain "Minutes of the
    # YYYY AGM" header). The existing agm_minutes_notification rule catches one specific
    # form; this broadens it conservatively.
    Rule(
        name="agm_minutes_publication_broad",
        pattern=re.compile(
            r"^(Uploading\s+of\s+the\s+[Mm]inutes\s+of\s+the\s+(\d{4}\s+|Annual\s+General)|"
            r"Publicity\s+of\s+the\s+[Mm]inutes\s+of\s+the\s+(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"Disseminate\s+(the\s+)?[Mm]inutes\s+of\s+the\s+(\d{4}\s+)?Annual\s+General\s+Meeting|"
            r"Dissemination\s+of\s+the\s+[Mm]inutes\s+and\s+clip\s+file|"
            r"Minutes\s+of\s+the\s+\d{4}\s+Annual\s+General\s+Meeting\s+of\b|"
            r"Notification\s+of\s+the\s+[Mm]inute\s+of\s+the\s+(\d{4}\s+|Annual\s+General))",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM minutes publication: {hl}",
        summary_th_template="{symbol} เผยแพร่รายงานการประชุมสามัญผู้ถือหุ้น: {hl}",
        suggested_action="No action required; minutes archived for the meeting.",
        rationale="Post-AGM minutes publication (additional phrasings) — routine.",
    ),
    # Earnings call presentation slides publication (post-event material, not invitation)
    Rule(
        name="earnings_call_presentation",
        pattern=re.compile(
            r"^Earnings\s+Call\s+for\s+(Q\d|Quarter\s+\d)\s+\d{4}\s+Business\s+and\s+Operating\s+Performance\s+Presentation",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} earnings-call presentation deck: {hl}",
        summary_th_template="{symbol} เอกสารประกอบการประชุมแถลงผลประกอบการ: {hl}",
        suggested_action="No action required; deck archived.",
        rationale="Earnings-call presentation deck publication — routine IR cadence.",
    ),
    # Capital reduction/increase REGISTRATION with the Department of Business Development —
    # the procedural follow-on to the BOD/AGM resolution (already classified material/critical
    # above). Empirically Haiku rates this routine.
    Rule(
        name="capital_change_registration",
        pattern=re.compile(
            r"^Notification\s+of\s+registration\s+of\s+capital\s+(reduction|increase)\s+with\s+the\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="capital_change",
        summary_template="{symbol} capital-change registration with DBD: {hl}",
        summary_th_template="{symbol} จดทะเบียนเปลี่ยนแปลงทุนกับกระทรวงพาณิชย์: {hl}",
        suggested_action="No action required; registration follows an already-approved capital change.",
        rationale="Capital-change registration with DBD (procedural follow-on) — routine.",
    ),
    # Change of company secretary / change of authorized directors / appointment of
    # assistant managing director — sub-executive governance changes empirically rated
    # routine by Haiku (NOT material like director appointment).
    Rule(
        name="sub_executive_change",
        pattern=re.compile(
            r"^(Change\s+of\s+(the\s+)?[Cc]ompany\s+[Ss]ecretary|"
            r"Change\s+of\s+(the\s+)?[Aa]uthorized\s+[Dd]irectors|"
            r"Notification\s+of\s+[Aa]ppointment\s+of\s+(the\s+)?[Aa]ssistant\s+[Mm]anaging\s+[Dd]irector|"
            r"Appointment\s+of\s+Subcommittee\s+Member|"
            r"Notification\s+of\s+progress\s+regarding\s+the\s+nomination\s+and\s+appointment\b)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="director_mgmt_change",
        summary_template="{symbol} sub-executive / committee role change: {hl}",
        summary_th_template="{symbol} เปลี่ยนแปลงเลขานุการ/กรรมการมีอำนาจ/ผู้บริหารระดับรอง: {hl}",
        suggested_action="No action required.",
        rationale="Sub-executive role change (secretary / authorized directors / committee) — routine procedural.",
    ),
    # Change of subsidiary name, company profile updates (routine housekeeping)
    Rule(
        name="company_subsidiary_admin",
        pattern=re.compile(
            r"^Notification\s+of\s+change\s+of\s+subsidiary\s+company\s+name|"
            r"^Change\s+of\s+[Cc]ompany\s+[Pp]rofile",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} company / subsidiary administrative update: {hl}",
        summary_th_template="{symbol} เปลี่ยนแปลงข้อมูลบริษัท/บริษัทย่อย: {hl}",
        suggested_action="No action required; administrative update.",
        rationale="Company-info / subsidiary-name administrative update — routine housekeeping.",
    ),
    # Numbered dividend payment / interim dividend / change in cash distribution frequency
    # — these are scheduled REIT/Fund distribution events.
    Rule(
        name="numbered_dividend_payment_routine",
        pattern=re.compile(
            r"^Notification\s+of\s+the\s+\d+(st|nd|rd|th)\s+[Dd]ividend\s+[Pp]ayment|"
            r"^Notification\s+of\s+Dividend\s+Payment\s+\([Rr]evised\)|"
            r"^Payment\s+of\s+[Ii]nterim\s+[Dd]ividend\s*$",
            re.IGNORECASE,
        ),
        severity="routine",
        category="dividend",
        summary_template="{symbol} scheduled / numbered dividend payment: {hl}",
        summary_th_template="{symbol} จ่ายเงินปันผลตามรอบ/ระหว่างกาล: {hl}",
        suggested_action="No action required; scheduled distribution.",
        rationale="Periodic / numbered REIT/Fund dividend payment — routine per PFREIT rubric.",
    ),
    # NOTE: "Dissemination of dividend payment announcement" / financial-statement
    # publication phrasings intentionally NOT promoted — clusters too LLM-noisy on
    # category (dividend vs other vs earnings split). Fall through to LLM.

    # Interim distribution payment of <FundName> (routine PFREIT cadence)
    Rule(
        name="interim_distribution_payment",
        pattern=re.compile(
            r"^Notification\s+of\s+Interim\s+Distributed?\s+Payment\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="dividend",
        summary_template="{symbol} interim distribution payment: {hl}",
        summary_th_template="{symbol} จ่ายผลประโยชน์ตอบแทนระหว่างกาล: {hl}",
        suggested_action="No action required; interim distribution logged.",
        rationale="Routine REIT/PF interim distribution payment — routine per PFREIT rubric.",
    ),
    # NAV / NAV-per-unit additional headers without "Report" prefix
    Rule(
        name="nav_per_unit_plain",
        pattern=re.compile(
            r"^Net\s+Asset\s+Value\s+per\s+Unit\s+as\s+of\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} NAV-per-unit periodic report: {hl}",
        summary_th_template="{symbol} มูลค่าทรัพย์สินสุทธิต่อหน่วยลงทุน: {hl}",
        suggested_action="No action required; periodic NAV log.",
        rationale="Plain NAV-per-unit periodic disclosure — routine per PFREIT rubric.",
    ),
    # AGM minutes — additional "Annual General Shareholders' Meeting" phrasing (typo
    # for "Annual General Meeting of Shareholders") and "Annual General Shareholders'"
    Rule(
        name="agm_minutes_general_shareholders",
        pattern=re.compile(
            r"^Publication\s+of\s+(the\s+)?Minutes\s+of\s+(Annual\s+General\s+Shareholders'?\s+Meeting|"
            r"the\s+(\d+/)?\d{4}\s+Annual\s+General\s+Shareholders'?\s+Meeting)|"
            r"^Announcement\s+of\s+the\s+[Mm]inutes\s+of\s+Annual\s+General\s+Meeting\s+of\s+Shareholders|"
            r"^Disclosure\s+of\s+the\s+minutes\s+of\s+the\s+Annual\s+General\s+Shareholders'?\s+Meeting|"
            r"^Notification\s+of\s+the\s+Submission\s+of\s+the\s+Minutes\s+of\s+th\s+\d{4}\s+Annual\s+General|"
            r"^Notification\s+of\s+the\s+disclosure\s+of\s+minutes\s+of\s+the\s+\d{4}\s+Annual\s+General|"
            r"^Minute\s+of\s+the\s+Annual\s+General\s+Meeting\s+of\s+Shareholders",
            re.IGNORECASE,
        ),
        severity="routine",
        category="other",
        summary_template="{symbol} AGM minutes published (variant phrasing): {hl}",
        summary_th_template="{symbol} เผยแพร่รายงานการประชุมผู้ถือหุ้นประจำปี: {hl}",
        suggested_action="No action required; minutes archived.",
        rationale="Post-AGM minutes publication (alt phrasings) — routine.",
    ),
    # Earnings conference call — distinct from earnings_call_invite (which catches
    # "Notification convening date of the Earnings Call"). This is the plain
    # "Notification of the JMART GROUP Earnings Conference Call for QN" form.
    Rule(
        name="earnings_conference_call_invite",
        pattern=re.compile(
            r"^Notification\s+of\s+(the\s+)?\S+\s+(GROUP\s+|group\s+)?Earnings\s+Conference\s+Call\s+for\s+Q\d",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} earnings conference call invitation: {hl}",
        summary_th_template="{symbol} แจ้งการประชุมแถลงผลประกอบการ: {hl}",
        suggested_action="Calendar the call date.",
        rationale="Earnings conference call invitation — routine per rubric.",
    ),
    # Notification of Interim Distributed Payment (older phrasing variant)
    # NOTE: SET allows trading on securities / TTCL Securities are not permitted for
    # Short Selling — small operational SET notices that LLM rates routine/trading_sign.
    Rule(
        name="set_trading_admin_routine",
        pattern=re.compile(
            r"^SET\s+allows\s+trading\s+on\s+securities\s+of\b|"
            r"^[A-Z]+\s+Securities\s+are\s+not\s+permitted\s+for\s+Short\s+Selling",
            re.IGNORECASE,
        ),
        severity="routine",
        category="trading_sign",
        summary_template="{symbol} SET trading administrative notice: {hl}",
        summary_th_template="{symbol} ประกาศการซื้อขายจากตลาดหลักทรัพย์: {hl}",
        suggested_action="No action required; administrative trading notice.",
        rationale="SET trading admin notice (cash balance, no short selling, etc.) — routine trading_sign.",
    ),
    # Two-way communication: additional Q&A summary phrasings
    Rule(
        name="two_way_qa_more_variants",
        pattern=re.compile(
            r"^(Summary\s+of\s+inquiries\s+from\s+unitholders\s+regarding\s+the\s+two-way|"
            r"Notification\s+on\s+the\s+summary\s+of\s+questions\s+and\s+concerns|"
            r"Notification\s+of\s+the\s+disclosure\s+of\s+the\s+summary\s+of\s+questions|"
            r"Publication\s+of\s+summary\s+of\s+questions\s+and\s+answers\s+from|"
            r"Notification\s+of\s+summary\s+of\s+questions\s+from\s+unitholders\s+on\b)",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} two-way communication Q&A: {hl}",
        summary_th_template="{symbol} สรุปคำถามคำตอบจาก Two-way communication: {hl}",
        suggested_action="No action required; periodic unitholder Q&A log.",
        rationale="Two-way unitholder Q&A summary (additional phrasings) — routine.",
    ),
    # "Detail of <Fund Name> assets" header (REIT/Fund asset register, plain phrasing).
    # Narrower than the no_match pattern would suggest, because broader phrasings have
    # 50/50 LLM splits on category (information_memo vs regulatory_filing).
    Rule(
        name="asset_details_disclosure",
        pattern=re.compile(
            r"^Detail\s+of\s+\S+\s+.*Real\s+Estate\s+Investment\s+Trust\s+assets",
            re.IGNORECASE,
        ),
        severity="routine",
        category="information_memo",
        summary_template="{symbol} fund asset details disclosure: {hl}",
        summary_th_template="{symbol} เปิดเผยรายละเอียดทรัพย์สินของกองทุน: {hl}",
        suggested_action="No action required; periodic asset register.",
        rationale="REIT/PF asset-details disclosure — routine per PFREIT rubric.",
    ),
    # Routine website publication of a dividend payment already approved by BOD.
    # Distinct from bod_dividend_declaration (material BOD resolution) and from
    # dividend_omission (critical). This is the post-resolution publicity step.
    Rule(
        name="dividend_payment_website_publication",
        pattern=re.compile(
            r"^Publi(cation|sh)\s+(of\s+)?(the\s+)?"
            r"(Dividend\s+Payment(\s+Announcement)?|dividend\s+payment|payment\s+of\s+dividend(\s+announcement)?)"
            r"\b.*\b(on\s+(the\s+)?(Company'?s\s+)?[Ww]ebsite)\b",
            re.IGNORECASE,
        ),
        severity="routine",
        category="dividend",
        summary_template="{symbol} dividend payment published on company website: {hl}",
        summary_th_template="{symbol} เผยแพร่ประกาศจ่ายเงินปันผลบนเว็บไซต์บริษัท: {hl}",
        suggested_action="No action required; already-approved dividend re-published on the company site.",
        rationale="Post-resolution website publication of an already-approved dividend — routine.",
    ),
]


# Combine in priority order: critical first, then material, then routine
_ALL_RULES: list[Rule] = _CRITICAL_RULES + _MATERIAL_RULES + _ROUTINE_RULES


# ---------------------------------------------------------------------------
# THAI-ONLY RULES — for filings that arrive Thai-first (no EN twin yet)
# ---------------------------------------------------------------------------
# Empirically, ~10% of disclosures land TH-first and never get an EN twin on
# the same day (most often quarterly financials in earnings season). Match
# against the TH headline when the EN one is missing.
#
# Keep this list small and conservative. Each rule's TH regex must match
# only patterns where Haiku consistently gave the same label across tickers.

_TH_RULES: list[Rule] = [
    # งบการเงิน [ไตรมาส X | รวม | เฉพาะกิจการ | ระหว่างกาล] = financial statements
    # คำอธิบายและวิเคราะห์ของฝ่ายจัดการ = MD&A
    Rule(
        name="th_financial_statement_or_mda",
        pattern=re.compile(
            r"^(งบการเงิน|คำอธิบายและวิเคราะห์ของฝ่ายจัดการ|"
            r"งบการเงินรวม|งบการเงินเฉพาะกิจการ|"
            r"รายงานผลการดำเนินงาน)",
        ),
        severity="material",
        category="earnings",
        summary_template="{symbol} TH-only financial filing: {hl}",
        summary_th_template="{symbol} ยื่นงบการเงิน/คำอธิบายและวิเคราะห์ของฝ่ายจัดการ: {hl}",
        suggested_action="EN twin usually follows within hours; pull the PDF for analyst review.",
        rationale="Thai-first quarterly financial statement or MD&A — material per rubric.",
    ),
    # Thai BOD meeting resolution announcing dividend payment / financial assistance / AGM —
    # mirror of the EN bod_resolution_dividend_agm_schedule rule on the TH side.
    Rule(
        name="th_bod_resolution_dividend",
        pattern=re.compile(
            r"^แจ้งมติที่ประชุมคณะกรรมการบริษัท\s+เรื่อง\s+(การจ่ายเงินปันผล|"
            r"การให้ความช่วยเหลือทางการเงิน)",
        ),
        severity="material",
        category="dividend",
        summary_template="{symbol} TH BOD resolution (dividend + AGM): {hl}",
        summary_th_template="{symbol} แจ้งมติคณะกรรมการเรื่องการจ่ายเงินปันผลและกำหนดประชุม: {hl}",
        suggested_action="Read the resolution PDF; note dividend amount and calendar the AGM date.",
        rationale="Thai-first BOD resolution declaring dividend payment + AGM schedule — material per rubric.",
    ),
    # Thai-only "การจัดตั้งบริษัทใหม่" — establishment of a new company. Empirically
    # Haiku rates these material/ma_acquisition_disposal when filed Thai-first.
    Rule(
        name="th_new_company_establishment",
        pattern=re.compile(
            r"^การจัดตั้งบริษัทใหม่",
        ),
        severity="material",
        category="ma_acquisition_disposal",
        summary_template="{symbol} TH new-company establishment: {hl}",
        summary_th_template="{symbol} แจ้งการจัดตั้งบริษัทใหม่: {hl}",
        suggested_action="Open the disclosure; identify the new entity, capital and ownership structure.",
        rationale="Thai-first new-company establishment notice — material per rubric.",
    ),
    # SEC News : สรุปแบบ XXX = SEC summary of regulatory form filings (Form 59 = major shareholder,
    # 246-2 = trustee report, 247-6 = tender offer admin, 250-2 = tender result). Daily SEC
    # roll-ups — informational. Specific ticker-level tender offers are caught by tender_offer
    # critical rule on the EN side.
    Rule(
        name="th_sec_news_summary",
        pattern=re.compile(
            r"^SEC\s+News\s*[:：]",
        ),
        severity="routine",
        category="regulatory_filing",
        summary_template="{symbol} SEC News summary: {hl}",
        summary_th_template="{symbol} SEC News สรุปข่าว: {hl}",
        suggested_action="Logged for periodic review; ticker-specific tender offers come via separate disclosure.",
        rationale="SEC News daily summary — routine regulatory log per rubric.",
    ),
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _try_rules(rule_list: list[Rule], text: str, symbol: str) -> tuple[Classification | None, str | None]:
    """Run a rule list against a single piece of text. Returns first match."""
    hl = text[:_HL_MAX] + ("…" if len(text) > _HL_MAX else "")
    for rule in rule_list:
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


def match_rules(
    *,
    symbol: str,
    headline_en: str | None,
    headline_th: str | None = None,
) -> Classification | None:
    """Run rules against a disclosure. Returns Classification on confident match,
    None if it falls through to Haiku.

    Tries EN rules against headline_en first. If no match (or no EN headline),
    falls back to TH-only rules against headline_th.
    """
    if headline_en:
        cls, _ = _try_rules(_ALL_RULES, headline_en.strip(), symbol)
        if cls is not None:
            return cls
    if headline_th:
        cls, _ = _try_rules(_TH_RULES, headline_th.strip(), symbol)
        if cls is not None:
            return cls
    return None


def match_rules_with_diagnostics(
    *,
    symbol: str,
    headline_en: str | None,
    headline_th: str | None = None,
) -> tuple[Classification | None, str | None]:
    """Like match_rules() but also returns the rule name (or None for fall-through)."""
    if headline_en:
        cls, name = _try_rules(_ALL_RULES, headline_en.strip(), symbol)
        if cls is not None:
            return cls, name
    if headline_th:
        cls, name = _try_rules(_TH_RULES, headline_th.strip(), symbol)
        if cls is not None:
            return cls, name
    return None, None


def rule_count() -> int:
    return len(_ALL_RULES) + len(_TH_RULES)
