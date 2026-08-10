import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const read = (name) => readFile(path.join(root, name), "utf8");
const close = (actual, expected, tolerance = 0.001) => {
  assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} not within ${tolerance} of ${expected}`);
};

test("Sector Intelligence v3 preserves the audited perimeter and adds MD&A-backed company drivers", async () => {
  const data = JSON.parse(await read("data/sector-intelligence.json"));
  assert.equal(data.meta.schemaVersion, 3);
  assert.equal(data.meta.effectiveMarketEod, "2026-08-07");
  assert.equal(data.meta.qaVerdict, "PASS");
  assert.deepEqual(Object.keys(data.sectors).sort(), ["FOOD", "PROP"]);
  assert.equal(data.sectors.FOOD.segments.length, 9);
  assert.equal(data.sectors.PROP.segments.length, 5);

  for (const [sectorName, sector] of Object.entries(data.sectors)) {
    close(sector.segments.reduce((sum, row) => sum + row.marketCapSharePct, 0), 100, 0.15);
    for (let i = 1; i < sector.segments.length; i += 1) {
      assert.ok(sector.segments[i - 1].marketCapMb >= sector.segments[i].marketCapMb, `${sectorName} must be sorted by market cap`);
    }
    for (const segment of sector.segments) {
      assert.ok(segment.claims.length >= 12, segment.code + " must expose the full claim register");
      const sourceIds = new Set(segment.sources.map((source) => source.sourceId));
      for (const claim of segment.claims) {
        assert.ok(["fact_calculated","management_explanation","analyst_inference","analyst_test"].includes(claim.kind));
        assert.ok(claim.sourceIds.length > 0);
        for (const sourceId of claim.sourceIds) assert.ok(sourceIds.has(sourceId), segment.code + " unresolved " + sourceId);
      }
      assert.ok(segment.coverage.margin);
      for (const source of segment.sources) {
        assert.ok(source.sourceId && source.kind && source.label && source.role);
        if (source.path) assert.match(source.sha256, /^[a-f0-9]{64}$/);
      }
      for (const company of segment.companies) {
        assert.equal(typeof company.rfoPanel, "boolean");
        assert.equal(typeof company.npatPanel, "boolean");
        assert.equal(typeof company.marginPanel, "boolean");
        assert.ok(Array.isArray(company.rfoOverrideSourceIds));
        assert.ok(Array.isArray(company.npatOverrideSourceIds));
        assert.ok(company.performanceDrivers);
        assert.ok(["high","medium","standard"].includes(company.performanceDrivers.materiality));
        assert.ok(company.performanceDrivers.rfoDrivers.length > 0);
        assert.ok(company.performanceDrivers.npatDrivers.length > 0);
        for (const driver of [
          ...company.performanceDrivers.rfoDrivers,
          ...company.performanceDrivers.npatDrivers,
          ...company.performanceDrivers.specialItems,
        ]) {
          assert.match(driver.th, /[\u0E00-\u0E7F]/, company.ticker + " driver must contain Thai copy");
          assert.notEqual(driver.th.trim(), driver.en.trim(), company.ticker + " Thai driver must not fall back to English");
        }
        for (const sourceId of company.performanceDrivers.sourceIds) assert.ok(sourceIds.has(sourceId), segment.code + " unresolved company source " + sourceId);
      }
    }
  }

  const allCompanies = Object.values(data.sectors).flatMap((sector) => sector.segments.flatMap((segment) => segment.companies));
  assert.equal(allCompanies.length, 118);
  assert.equal(allCompanies.filter((company) => company.performanceDrivers.primaryMdaAvailable).length, 116);
  assert.deepEqual(allCompanies.filter((company) => !company.performanceDrivers.primaryMdaAvailable).map((company) => company.ticker).sort(), ["AKS","AP"]);
  const food = data.sectors.FOOD;
  close(food.metrics.rfoFy2024Mb, 1271330.27125);
  close(food.metrics.rfoFy2025Mb, 1259913.52285);
  close(food.metrics.npatOwnersFy2024Mb, 61543.52041);
  close(food.metrics.npatOwnersFy2025Mb, 70708.8896);

  const f1 = food.segments.find((row) => row.code === "F1");
  close(f1.metrics.rfoFy2024Mb, 778569.02447);
  close(f1.metrics.rfoFy2025Mb, 784535.4531);
  close(f1.metrics.rfoYoYPct, 0.7663326491);
  close(f1.metrics.npatOwnersFy2024Mb, 26124.63559);
  close(f1.metrics.npatOwnersFy2025Mb, 40273.60675);
  close(f1.metrics.npatYoYPct, 54.1594967373);
  assert.equal(f1.metrics.rfoDirectionDriver, "BTG");
  assert.equal(f1.metrics.npatDirectionDriver, "CPF");
  assert.equal(f1.coverage.rfo.count, 6);
  assert.equal(f1.coverage.positivePe.count, 6);

  const f5 = data.sectors.FOOD.segments.find((row) => row.code === "F5");
  assert.equal(f5.coverage.rfo.count, 5);
  assert.equal(f5.coverage.npat.count, 6);
  close(f5.metrics.npatYoYPct, -76.600474, 0.001);

  const f7 = data.sectors.FOOD.segments.find((row) => row.code === "F7");
  close(f7.metrics.rfoYoYPct, -7.0126480424);
  close(f7.metrics.npatYoYPct, 311.944197, 0.001);

  const p2 = data.sectors.PROP.segments.find((row) => row.code === "P2");
  close(p2.metrics.rfoYoYPct, -12.4162708264);
  close(p2.metrics.npatYoYPct, -29.8299639821);
  assert.ok(p2.metrics.ytdAdjustedReturnPct > 40);

  const p5 = data.sectors.PROP.segments.find((row) => row.code === "P5");
  assert.equal(p5.metrics.npatState, "loss_narrowed");
  assert.equal(p5.coverage.positivePe.count, 1);
  close(p5.coverage.positivePe.marketCapPct, 23.620219, 0.001);
  assert.ok(!p5.roles.some((role) => role.ticker === "PSH"));

  const f8 = data.sectors.FOOD.segments.find((row) => row.code === "F8");
  assert.equal(f8.alternativeFiscalView.companyCount, 9);
  close(f8.alternativeFiscalView.rfoYoYPct, -5.198046, 0.001);
  close(f8.alternativeFiscalView.npatYoYPct, -59.951491, 0.001);

  const f9 = data.sectors.FOOD.segments.find((row) => row.code === "F9");
  assert.equal(f9.coverage.positivePe.count, 2);
  assert.equal(f9.coverage.positivePe.total, 8);
  close(f9.coverage.positivePe.marketCapPct, 35.804468, 0.001);

  const uv = p5.companies.find((company) => company.ticker === "UV");
  assert.equal(uv.npatPanel, false);
  assert.equal(uv.marginPanel, false);
  assert.ok(Number.isFinite(uv.npatYoYPct)); // raw value retained; UI must respect npatPanel=false
  assert.equal(uv.netMarginPct, null);

  const aqua = f5.companies.find((company) => company.ticker === "AQUA");
  assert.match(aqua.panelExclusionReason, /Comparable RFO unavailable/);
  assert.deepEqual(aqua.npatOverrideSourceIds, ["AQUA_FY2025_MDA"]);
});


test("Sector Intelligence is bilingual, deep-linkable, coverage-aware and secret-safe", async () => {
  const [html, css, js, index, nav, data] = await Promise.all([
    read("sector-intelligence.html"), read("sector-intelligence.css"), read("sector-intelligence.js"),
    read("index.html"), read("nav.js"), read("data/sector-intelligence.json"),
  ]);
  assert.match(html, /data-i18n="page\.sectorIntelligence"/);
  assert.match(html, /id="evidenceDialog"/);
  assert.match(html, /id="claimList"/);
  assert.match(html, /id="alternativeFiscalView"/);
  assert.match(html, /id="marketCapDonut"/);
  assert.match(html, /id="earningsBars"/);
  assert.match(html, /id="earningsRfoTotal"/);
  assert.match(html, /id="earningsNpatTotal"/);
  assert.match(html, /id="marketMap"/);
  assert.match(html, /id="peStrip"/);
  assert.match(html, /id="companyCardList"/);
  assert.match(html, /id="companyStory"/);
  assert.equal((html.match(/class="si-flow/g) || []).length, 2);
  assert.match(index, /href="sector-intelligence\.html"/);
  assert.match(nav, /sector-intelligence\.html/);
  assert.match(js, /URLSearchParams\(location\.search\)/);
  assert.match(js, /query\.get\("flow"\)/);
  assert.match(js, /params\.set\("flow",state\.flow\)/);
  assert.match(js, /evidenceClaims\.map/);
  assert.match(js, /source\.sha256/);
  assert.match(js, /source\.path/);
  assert.match(js, /source\.role/);
  assert.match(js, /alternativeFiscalView/);
  assert.match(js, /renderVisuals/);
  assert.match(js, /renderMarketCapMix/);
  assert.match(js, /renderEarningsBars/);
  assert.match(js, /renderDriverChain/);
  assert.match(js, /renderRoleCards/);
  assert.match(js, /ticker-summary\.json/);
  assert.match(js, /renderMarketMap/);
  assert.match(js, /renderPeStrip/);
  assert.match(js, /directCompanyClaim/);
  assert.match(js, /rfoNarrative/);
  assert.match(js, /npatNarrative/);
  assert.match(js, /company\.panelExclusionReason/);
  assert.match(js, /claim\.sourceIds/);
  assert.match(js, /params\.set\("company",state\.company\)/);
  assert.match(js, /querySelectorAll\("\.si-flow"\)/);
  assert.match(js, /fetch\("\.\/data\/sector-intelligence\.json"/);
  assert.match(js, /loss_narrowed/);
  assert.match(js, /segment\.coverage\.positivePe/);
  assert.match(css, /\.si-metric-coverage/);
  assert.match(css, /\.si-claim-item/);
  assert.match(css, /\.si-source-meta/);
  assert.match(css, /\.si-flow-mobile/);
  assert.match(css, /\.si-visual-story/);
  assert.match(css, /\.si-market-map/);
  assert.match(css, /\.si-earnings-totals/);
  assert.match(css, /\.si-driver-node/);
  assert.match(css, /\.si-role-logo/);
  assert.match(css, /\.si-company-why-grid/);
  assert.match(css, /\.si-page\[data-mode="meeting"\] \.si-matrix-table-wrap/);
  assert.doesNotMatch(js, /lossNarrowed"\)\s*\+\s*"\s+—/);
  assert.doesNotMatch([html, css, js, data].join("\n"), /api[_-]?key\s*[:=]/i);
  assert.doesNotMatch(js, /setsmart|api\.set/i);
});