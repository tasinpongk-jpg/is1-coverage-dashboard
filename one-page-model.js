// One-Page Summary data model — pure, no DOM. Shared by one-page.html and
// tests/onepage-completeness.mjs so the test checks exactly what the page renders.
(function (root) {
  var ONEPAGE_SOURCES = [
    'ticker-summary', 'company-reports', 'visits', 'disclosure-pulse', 'unusual-trading',
    'sec-form59', 'external-news', 'trading-signs', 'sec-enforcement', 'bond-summary',
    'oppday-minutes', 'vault-ticker-notes', 'source-coverage'
  ];

  var num = function (v) { return typeof v === 'number' && isFinite(v) ? v : null; };
  var arr = function (v) { return Array.isArray(v) ? v : []; };
  var byTk = function (list, tk, field) {
    return arr(list).filter(function (x) { return x && String(x[field || 'tk'] || '').toUpperCase() === tk; });
  };
  function clip(s, n) {
    s = (s || '').replace(/\s+/g, ' ').trim();
    if (s.length <= n) return s;
    var cut = s.slice(0, n);
    var sp = cut.lastIndexOf(' ');
    return (sp > n * 0.6 ? cut.slice(0, sp) : cut).replace(/[,;:\s]+$/, '') + '…';
  }
  var SEV_RANK = { critical: 0, high: 0, material: 1, medium: 1, low: 2, routine: 2 };
  function latestPeriod(notes) {
    return arr(notes).map(function (n) { return n.period || ''; }).filter(Boolean).sort().pop() || '';
  }
  function periodLabel(h) {
    if (!h.months || h.months >= 12) return 'FY' + h.year;
    if (h.months === 3 && /^Q[1-4]$/.test(h.quarter || '')) return h.quarter + '/' + h.year;
    return h.months + 'M/' + h.year;
  }

  function buildOnePageModel(tk, D, opts) {
    D = D || {};
    opts = opts || {};
    tk = String(tk || '').toUpperCase();
    var ts = D['ticker-summary'] || {};
    var t = arr(ts.tickers).filter(function (x) { return x.tk === tk; })[0];
    if (!tk || !t) return null;

    var asOf = ts.asOf || '';
    var report = ((D['company-reports'] || {}).reports || {})[tk] || null;
    var visit = byTk((D.visits || {}).rows, tk)[0] || null;
    var signs = byTk((D['trading-signs'] || {}).items, tk)
      .sort(function (a, b) { return (b.effective_date || '').localeCompare(a.effective_date || ''); });
    var coverage = byTk((D['source-coverage'] || {}).rows, tk)[0] || null;
    var vault = ((D['vault-ticker-notes'] || {}).tickers || {})[tk] || {};
    var opp = byTk((D['oppday-minutes'] || {}).summaries, tk, 'ticker')[0] || null;
    var issuer = byTk((D['bond-summary'] || {}).issuers, tk)[0] || null;

    var identity = {
      tk: tk, name: t.name || '', sector: t.sector || '', segment: t.segment || '', rm: t.rm || '',
      tone: (report && report.tone) || (visit && visit.tone) || '',
      priority: (visit && visit.priority) || '',
      tradingSign: signs[0] ? { sign: signs[0].sign, date: signs[0].effective_date, reason: signs[0].reason } : null,
      logoUrl: t.logoUrl || '', asOf: asOf
    };

    var stats = {
      last: num(t.last), pct1d: num(t.pct1d), pctYtd: num(t.pctYtd), hi52: num(t.hi52), lo52: num(t.lo52),
      mktcapBn: num(t.mktcap) != null ? t.mktcap / 1e9 : null,
      pe: num(t.pe), pbv: num(t.pbv), dy: num(t.dy), freeFloat: num(t.freeFloat), foreignRoom: num(t.foreignRoom)
    };

    // thesis: company report wins; visit-log thesis is a fallback and may be an auto-draft
    var thesis = '', thesisIsDraft = false;
    if (report && report.thesis) thesis = report.thesis;
    else if (visit && visit.thesis) {
      thesis = visit.thesis.replace(/\s*\*\(draft[^)]*\)\*\s*$/i, '').trim();
      thesisIsDraft = !!visit.thesisDraft;
    }
    var business = clip((report && report.business) || t.businessType || '', 320);

    // financials: last 3 full years + a newer partial period if one exists
    // SET labels some year-to-date rows as quarter "6M"/"9M" while reporting months=12
    var hl = arr(t.highlights).map(function (h) {
      var m = /^(\d+)M$/.exec(h.quarter || '');
      return m && +m[1] < 12 ? Object.assign({}, h, { months: +m[1] }) : h;
    }).sort(function (a, b) {
      return (a.year - b.year) || ((a.months || 12) - (b.months || 12));
    });
    // some SET rows are placeholders for a year not yet reported (all figures null)
    hl = hl.filter(function (h) { return num(h.revenue) != null || num(h.netProfit) != null; });
    var fy = hl.filter(function (h) { return !h.months || h.months >= 12; });
    var rows = fy.slice(-3);
    var lastFy = rows.length ? rows[rows.length - 1].year : -Infinity;
    var partial = hl.filter(function (h) { return h.months && h.months < 12 && h.year > lastFy; }).pop();
    if (partial) rows.push(partial);
    var financials = {
      rows: rows.map(function (h) {
        return {
          period: periodLabel(h), partial: !!(h.months && h.months < 12),
          revenue: num(h.revenue), netProfit: num(h.netProfit), npm: num(h.npm),
          roe: num(h.roe), deRatio: num(h.deRatio), eps: num(h.eps)
        };
      }),
      snapshot: arr(report && report.financialSnapshot)
    };

    var seen = {};
    var risks = arr(report && report.watchItems).concat(arr(visit && visit.flags))
      .filter(function (s) { var k = (s || '').trim().toLowerCase(); if (!k || seen[k]) return false; seen[k] = 1; return true; })
      .map(function (s) { return { text: s.replace(/^(HIGH|FLAG)\s*[:—-]\s*/i, ''), high: /^HIGH\b/i.test(s) }; })
      .sort(function (a, b) { return (b.high ? 1 : 0) - (a.high ? 1 : 0); });

    var disc = byTk((D['disclosure-pulse'] || {}).filings, tk);
    var events = [];
    disc.slice().sort(function (a, b) {
      var ra = SEV_RANK[(a.severity || 'low').toLowerCase()], rb = SEV_RANK[(b.severity || 'low').toLowerCase()];
      return (ra - rb) || (b.ts || '').localeCompare(a.ts || '');
    }).forEach(function (f) {
      events.push({ kind: 'disclosure', date: (f.ts || '').slice(0, 10), text: f._summary || f.title || '',
        url: f.url || '', severity: (f.severity || 'low').toLowerCase() });
    });
    byTk((D['unusual-trading'] || {}).byTicker, tk).forEach(function (u) {
      arr(u.summary).forEach(function (s) {
        events.unshift({ kind: 'alert', date: ((D['unusual-trading'] || {}).asOf || '').slice(0, 10), text: s, url: '', severity: u.highestSeverity || 'medium' });
      });
    });
    arr((D['sec-form59'] || {}).items).filter(function (i) { return String(i.tk || i.ticker || '').toUpperCase() === tk; })
      .forEach(function (i) {
        events.unshift({ kind: 'form59', date: String(i.date || i.ts || '').slice(0, 10),
          text: [i.name || i.person, i.side || i.type, i.shares != null ? i.shares + ' sh' : '', i.price != null ? '@' + i.price : ''].filter(Boolean).join(' '),
          url: i.url || '', severity: 'medium' });
      });
    signs.forEach(function (s) {
      events.unshift({ kind: 'sign', date: s.effective_date || '', text: s.sign + ' — ' + (s.reason || ''), url: '', severity: 'high' });
    });
    arr((D['sec-enforcement'] || {}).items).filter(function (i) { return String(i.matched_ticker || '').toUpperCase() === tk; })
      .forEach(function (i) {
        events.unshift({ kind: 'enforcement', date: i.action_date || '', text: (i.enforcement_type ? i.enforcement_type + ': ' : '') + clip(i.action_type || i.facts || '', 160), url: '', severity: 'high' });
      });
    byTk((D['external-news'] || {}).items, tk)
      .sort(function (a, b) { return (b.ts || '').localeCompare(a.ts || ''); }).slice(0, 3)
      .forEach(function (n) {
        events.push({ kind: 'news', date: (n.ts || '').slice(0, 10), text: (n.source ? n.source + ': ' : '') + (n.title || ''), url: n.url || '', severity: 'low' });
      });
    // priority order so fit-to-page trimming drops routine filings first (sort is stable)
    var evRank = function (e) {
      if (e.kind === 'disclosure') return SEV_RANK[e.severity] === 2 ? 3 : 1;
      return e.kind === 'news' ? 2 : 0;
    };
    events.sort(function (a, b) { return evRank(a) - evRank(b); });

    var debt = null;
    if (issuer) {
      var next = arr(issuer.bonds).filter(function (b) { return b.maturityDate && b.maturityDate >= asOf; })
        .sort(function (a, b) { return a.maturityDate.localeCompare(b.maturityDate); })[0];
      debt = {
        rating: issuer.rating || '', outstandingBn: num(issuer.totalOutstanding) != null ? issuer.totalOutstanding / 1000 : null,
        longCount: issuer.longCount || 0, shortCount: issuer.shortCount || 0,
        nextMaturity: next ? { symbol: next.symbol, date: next.maturityDate, amountMn: num(next.outstanding) } : null
      };
    }

    var firms = [];
    arr(t.auditors).forEach(function (a) { if (a.company && firms.indexOf(a.company) < 0) firms.push(a.company); });
    var governance = {
      cgScore: num(t.cgScore), esgRating: t.esgRating || '', cacFlag: !!t.cacFlag,
      auditOpinion: t.auditOpinion || '', auditorFirm: firms.join(', '),
      dividendPolicy: clip(t.dividendPolicy || '', 200),
      fiscalYearEnd: t.fiscalYearEnd || '', listedDate: t.listedDate || ''
    };

    var qs = arr(report && report.questions).length ? arr(report.questions) : arr(visit && visit.questions);
    var specific = qs.filter(function (q) { return !/^What changed behind:/i.test(q); });
    var meeting = {
      lastVisit: (visit && visit.lastVisit) || '', nextAction: (visit && visit.nextAction) || '',
      questions: specific.length >= 3 ? specific : qs
    };

    var cc = (coverage && coverage.currentCoverage) || {};
    var lp = (coverage && coverage.latestPeriods) || {};
    var mdaP = latestPeriod(vault.mda) || lp.mda || '';
    var fsP = latestPeriod(vault.fsNotes) || lp.fsNotes || '';
    var completeness = [
      { key: 'price', ok: stats.last != null, detail: asOf },
      { key: 'valuation', ok: stats.pe != null || stats.pbv != null, detail: '' },
      { key: 'financials', ok: financials.rows.length > 0, detail: financials.rows.length ? financials.rows[financials.rows.length - 1].period : '' },
      { key: 'report', ok: !!report, detail: report && report.generated ? report.generated.slice(0, 10) : '' },
      { key: 'thesis', ok: !!thesis && !thesisIsDraft, detail: thesisIsDraft ? 'draft' : '' },
      { key: 'opp', ok: !!opp || arr(vault.calls).length > 0, detail: opp ? 'Opp Day' : (arr(vault.calls).length ? arr(vault.calls).length + ' call' : '') },
      { key: 'mda', ok: !!mdaP, detail: mdaP, current: cc.mda },
      { key: 'fsNotes', ok: !!fsP, detail: fsP, current: cc.fsNotes },
      { key: 'auditor', ok: !!(cc.auditor || lp.auditor || governance.auditOpinion), detail: lp.auditor || '' },
      { key: 'disclosures90d', ok: disc.length > 0, detail: String(disc.length) },
      { key: 'bonds', ok: true, detail: debt ? (debt.longCount + debt.shortCount) + '' : 'none' },
      { key: 'visit', ok: !!(visit && visit.lastVisit), detail: (visit && visit.lastVisit) || '' }
    ];
    var target = (coverage && coverage.targetPeriod) || '';
    completeness.forEach(function (c) {
      c.labelKey = 'onepage.cc.' + c.key;
      // filings older than the coverage target quarter are present but stale
      if ((c.key === 'mda' || c.key === 'fsNotes') && c.ok && target && c.detail < target) c.stale = true;
    });

    var missingRequired = [];
    if (!identity.name) missingRequired.push('name');
    if (stats.last == null) missingRequired.push('price');
    if (!thesis && !business) missingRequired.push('thesisOrBusiness');
    if (!financials.rows.length) missingRequired.push('financials');

    return {
      identity: identity, stats: stats, thesis: thesis, thesisIsDraft: thesisIsDraft, business: business,
      financials: financials, risks: risks, events: events, debt: debt, governance: governance, meeting: meeting,
      completeness: completeness,
      targetPeriod: target,
      missingCurrent: arr(coverage && coverage.missingCurrent),
      qualityFlagsCount: arr(report && report.qualityFlags).length,
      missingRequired: missingRequired
    };
  }

  var api = { buildOnePageModel: buildOnePageModel, ONEPAGE_SOURCES: ONEPAGE_SOURCES };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else { root.buildOnePageModel = buildOnePageModel; root.ONEPAGE_SOURCES = ONEPAGE_SOURCES; }
})(typeof window !== 'undefined' ? window : this);
