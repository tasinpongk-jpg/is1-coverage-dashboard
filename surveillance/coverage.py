"""Coverage list — static, no cross-project import.

The 231-name FOOD/PROP/PFREIT + AGRI/CONS/CONMAT coverage. Vendored from
set_mcp/server.py so the CI workflow has no dependency on the MCP server.
Keep this in sync with the canonical list in set_mcp/server.py if that ever
diverges.
"""

from __future__ import annotations

COVERAGE: dict[str, list[str]] = {
    "AGRI": [
        "GFPT", "LEE", "NER", "PCE", "PPPM", "SMO", "STA", "TEGH", "TFM",
        "TL", "TRUBB", "UPOIC", "UVAN", "VPO",
    ],
    "FOOD": [
        "AAI", "APURE", "ASIAN", "BR", "BRR", "BTG", "CBG", "CFRESH",
        "CH", "CHAO", "CHOTI", "CM", "COCOCO", "CPF", "CPI", "F&D", "FM",
        "HTC", "ICHI", "ITC", "JDF", "KBS", "KCG", "KSL", "KTIS", "LST",
        "M", "MADAME", "MALEE", "NRF", "NSL", "OKJ", "OSP", "PB", "PLUS",
        "PM", "PQS", "PRG", "RBF", "SAPPE", "SAUCE", "SNNP", "SNP",
        "SORKON", "SSF", "SST", "SUN", "TC", "TFG", "TFMAMA", "TIPCO",
        "TKN", "TU", "TVO", "TWPC", "XBIO", "ZEN",
    ],
    "CONS": [
        "APCS", "BJCHI", "BKD", "CIVIL", "CK", "CNT", "DEMCO", "EMC",
        "ITD", "JR", "NL", "NWR", "PLE", "PREB", "PYLON", "RT", "SEAFCO",
        "SOLAR", "SQ", "SRICHA", "STECON", "STI", "STPI", "SYNTEC",
        "TEAMG", "TEKA", "TPOLY", "TRC", "TRITN", "TTCL", "UNIQ", "WGE",
    ],
    "CONMAT": [
        "CCP", "DCC", "DCON", "DRT", "EPG", "GEL", "PPP", "Q-CON", "SCC",
        "SCCC", "SCGD", "SCP", "SKN", "STECH", "TASCO", "TOA", "TPIPL",
        "UMI", "VNG", "WIIK", "WINDOW",
    ],
    "PROP": [
        "A", "A5", "AKS", "AMATA", "AMATAV", "ANAN", "AP", "ASW", "AWC",
        "BLAND", "BRI", "BROCK", "CGD", "CI", "CMC", "CPN", "ESTAR",
        "EVER", "FPT", "GLAND", "J", "JCK", "KC", "KUN", "LALIN", "LH",
        "LPN", "MBK", "MJD", "MK", "NCH", "NNCL", "NOBLE", "NVD", "ORI",
        "ORN", "PEACE", "PF", "PIN", "PLAT", "PRECHA", "PRIN", "PROUD",
        "PSH", "QH", "RABBIT", "RICHY", "RML", "ROJNA", "S", "SA",
        "SAMCO", "SC", "SENA", "SIRI", "SPALI", "STELLA", "UV", "WHA",
        "WIN",
    ],
    "PFREIT": [
        "AIMCG", "ALLY", "AMATAR", "AXTRART", "B-WORK", "BOFFICE",
        "CPNCG", "CPNREIT", "CPTREIT", "CTARAF", "FTREIT", "FUTURERT",
        "GVREIT", "HPF", "HYDROGEN", "IMPACT", "ISSARA", "KPNREIT",
        "KTBSTMR", "LHRREIT", "LHSC", "LUXF", "M-PAT", "M-STOR", "MII",
        "MIPF", "MJLF", "MNIT", "MNIT2", "MNRF", "POPF", "PROSPECT",
        "QHBREIT", "QHOP", "SIRIPRT", "SPRIME", "SSPF", "SSTRT", "TIF1",
        "TLHPF", "TNPF", "TPRIME", "TTLPF", "TU-PF", "WHABT", "WHAIR",
        "WHART",
    ],
}

ALL_TICKERS: list[str] = [t for tks in COVERAGE.values() for t in tks]
SECTOR_OF: dict[str, str] = {tk: sec for sec, tks in COVERAGE.items() for tk in tks}
