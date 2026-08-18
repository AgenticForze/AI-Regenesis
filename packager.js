// Store-only ZIP writer + package manifests. No dependencies.
(function () {
  var TBL = null;
  function crcTable() {
    if (TBL) return TBL;
    TBL = new Uint32Array(256);
    for (var n = 0; n < 256; n++) {
      var c = n;
      for (var k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      TBL[n] = c >>> 0;
    }
    return TBL;
  }
  function crc32(buf) {
    var t = crcTable(), c = 0xffffffff;
    for (var i = 0; i < buf.length; i++) c = t[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }
  function w16(a, o, v) { a[o] = v & 255; a[o + 1] = (v >>> 8) & 255; }
  function w32(a, o, v) { a[o] = v & 255; a[o + 1] = (v >>> 8) & 255; a[o + 2] = (v >>> 16) & 255; a[o + 3] = (v >>> 24) & 255; }

  function zip(entries) {
    var enc = new TextEncoder(), parts = [], central = [], offset = 0;
    entries.forEach(function (e) {
      var name = enc.encode(e.name), data = e.data, crc = crc32(data);
      var lh = new Uint8Array(30 + name.length);
      w32(lh, 0, 0x04034b50); w16(lh, 4, 20); w16(lh, 6, 0); w16(lh, 8, 0);
      w16(lh, 10, 0); w16(lh, 12, 0x2821);
      w32(lh, 14, crc); w32(lh, 18, data.length); w32(lh, 22, data.length);
      w16(lh, 26, name.length); w16(lh, 28, 0);
      lh.set(name, 30);
      parts.push(lh, data);
      var cd = new Uint8Array(46 + name.length);
      w32(cd, 0, 0x02014b50); w16(cd, 4, 20); w16(cd, 6, 20); w16(cd, 8, 0);
      w16(cd, 10, 0); w16(cd, 12, 0); w16(cd, 14, 0x2821);
      w32(cd, 16, crc); w32(cd, 20, data.length); w32(cd, 24, data.length);
      w16(cd, 28, name.length); w16(cd, 30, 0); w16(cd, 32, 0);
      w16(cd, 34, 0); w16(cd, 36, 0); w32(cd, 38, 0); w32(cd, 42, offset);
      cd.set(name, 46);
      central.push(cd);
      offset += lh.length + data.length;
    });
    var cSize = central.reduce(function (a, b) { return a + b.length; }, 0);
    var eocd = new Uint8Array(22);
    w32(eocd, 0, 0x06054b50); w16(eocd, 4, 0); w16(eocd, 6, 0);
    w16(eocd, 8, entries.length); w16(eocd, 10, entries.length);
    w32(eocd, 12, cSize); w32(eocd, 16, offset); w16(eocd, 20, 0);
    return new Blob(parts.concat(central, [eocd]), { type: "application/zip" });
  }

  function save(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }

  var enc = new TextEncoder();

  // path -> in-zip name; folders are expanded from the manifest below
  var PKG = {
    "quick-reference-engine": {
      file: "quick-reference-engine.zip",
      root: "quick-reference-engine",
      files: ["SKILL.md", "references/lessons-learned.md", "references/spec-format.md",
        "scripts/build_order.py", "scripts/example_spec.py", "scripts/svg_engine.py",
        "scripts/svg_patterns.py", "scripts/templates.py"]
    },
    "deep8-architecture-engine": {
      file: "deep8-architecture-engine.zip",
      root: "deep8-architecture-engine",
      files: ["SKILL.md", "references/bespoke-pattern.md", "references/lessons-learned.md",
        "references/spec-format.md", "scripts/blueprint_table.py", "scripts/deep8_engine.py",
        "scripts/example_spec.py", "scripts/svg_engine.py"]
    },
    "retrospective-generator": {
      file: "retrospective-generator.zip",
      root: "retrospective-generator",
      files: ["SKILL.md", "references/lessons-learned.md", "references/spec-format.md",
        "scripts/example_interview.py", "scripts/interview_protocol.py", "scripts/retrospective_engine.py"]
    },
    "proposal-generator": {
      file: "proposal-generator.zip",
      root: "proposal-generator",
      files: ["SKILL.md", "references/lessons-learned.md", "references/spec-format.md",
        "scripts/example_proposal.py", "scripts/proposal_engine.py"]
    },
    "telecom-pack-v1": {
      file: "telecom-pack-v1.zip",
      root: "telecom-pack-v1",
      files: ["README.md", "CONTENT-LICENSE.md", "telecom_data.py", "telecom_deep8_data.py"],
      diagrams: "telecom"
    },
    "bssoss-pack-v1": {
      file: "bssoss-pack-v1.zip",
      root: "bssoss-pack-v1",
      files: ["README.md", "CONTENT-LICENSE.md", "bssoss_data.py", "bssoss_deep8_data.py"],
      diagrams: "bssoss"
    },
    "finance-pack-v1": {
      file: "finance-pack-v1.zip",
      root: "finance-pack-v1",
      files: ["README.md", "CONTENT-LICENSE.md", "finance_data.py", "finance_deep8_data.py"],
      diagrams: "finance"
    }
  };

  var SLUGS = {
    telecom: ["01-network-fault-rca-remediation", "02-5g-network-slicing-orchestration",
      "03-capacity-planning-traffic-forecasting", "04-self-healing-network-closed-loop",
      "05-churn-prediction-winback", "06-contact-center-triage-resolution",
      "07-sim-swap-fraud-detection", "08-telecom-soc-threat-hunting",
      "09-field-workforce-dispatch-scheduling", "10-billing-dispute-resolution",
      "11-line-onboarding-kyc-automation", "12-rf-cell-site-planning-optimization",
      "13-roaming-settlement-reconciliation", "14-iot-fleet-anomaly-detection",
      "15-sentiment-social-listening-action", "16-spectrum-interference-detection",
      "17-enterprise-sla-compliance-monitoring", "18-wholesale-bandwidth-marketplace",
      "19-predictive-maintenance-network-hardware", "20-personalized-plan-upsell-agent"],
    bssoss: ["01-order-to-activation-orchestration", "02-product-catalog-offer-management",
      "03-revenue-assurance-leakage-detection", "04-order-fallout-detection-recovery",
      "05-network-inventory-discovery-reconciliation", "06-mediation-cdr-xdr-processing",
      "07-charging-rating-anomaly-detection", "08-customer-360-master-data-unification",
      "09-subscription-lifecycle-entitlement", "10-number-portability-orchestration",
      "11-wholesale-partner-interconnect-onboarding", "12-service-catalog-network-activation-mapping",
      "13-trouble-ticket-cross-domain-assurance", "14-digital-bss-oss-migration-reconciliation",
      "15-promotions-campaign-configuration-engine", "16-dunning-collections-automation",
      "17-api-gateway-tmf-governance", "18-credit-limit-fraud-threshold-management",
      "19-partner-revenue-share-settlement", "20-legacy-system-decommissioning-archival"],
    finance: ["01-aml-transaction-monitoring-sar", "02-credit-underwriting-loan-origination",
      "03-algo-trading-strategy-orchestration", "04-card-not-present-fraud-detection",
      "05-customer-onboarding-kyc-finance", "06-robo-advisory-portfolio-rebalancing",
      "07-regulatory-compliance-monitoring-reporting", "08-insurance-claims-processing-fraud",
      "09-contract-loan-document-review", "10-fpna-forecasting", "11-chargeback-dispute-resolution",
      "12-market-risk-var-monitoring", "13-collections-delinquency-management", "14-ma-due-diligence",
      "15-esg-investment-screening", "16-treasury-cash-liquidity-forecasting",
      "17-insider-trading-surveillance", "18-complaint-handling-regulatory-compliance",
      "19-trade-settlement-reconciliation", "20-personalized-financial-advisory-nba"]
  };

  async function grab(path) {
    var r = await fetch(path);
    if (!r.ok) throw new Error(path + " (" + r.status + ")");
    return new Uint8Array(await r.arrayBuffer());
  }

  window.AIR_PACKAGE = async function (key, onState) {
    var p = PKG[key];
    if (!p) throw new Error("unknown package " + key);
    if (onState) onState("working");
    try {
      var jobs = p.files.map(function (f) {
        return grab(p.root + "/" + f).then(function (d) { return { name: key + "/" + f, data: d }; });
      });
      if (p.diagrams) {
        SLUGS[p.diagrams].forEach(function (slug) {
          jobs.push(grab("docs/" + p.diagrams + "/" + slug + "/README.md")
            .then(function (d) { return { name: key + "/use-cases/" + slug + "/README.md", data: d }; }));
          jobs.push(grab("docs/" + p.diagrams + "/" + slug + "/architecture.svg")
            .then(function (d) { return { name: key + "/use-cases/" + slug + "/architecture.svg", data: d }; }));
          jobs.push(grab("docs/deep8/" + p.diagrams + "/" + slug + "/diagram.svg")
            .then(function (d) { return { name: key + "/deep8/" + slug + "/diagram.svg", data: d }; })
            .catch(function () { return null; }));
          jobs.push(grab("docs/deep8/" + p.diagrams + "/" + slug + "/blueprint.svg")
            .then(function (d) { return { name: key + "/deep8/" + slug + "/blueprint.svg", data: d }; })
            .catch(function () { return null; }));
        });
      }
      var entries = (await Promise.all(jobs)).filter(Boolean);
      entries.push({
        name: key + "/PACKAGE.txt",
        data: enc.encode("AI-Regenesis — " + key + "\n" +
          "Packaged from the AI-Regenesis product site.\n" +
          entries.length + " files.\n\n" +
          "Source: https://github.com/AgenticForze/AI-Regenesis\n" +
          "Code MIT · content CC BY-NC 4.0 · created by Naga Gande\n")
      });
      save(zip(entries), p.file);
      if (onState) onState("done");
    } catch (e) {
      if (onState) onState("error");
      throw e;
    }
  };

  window.AIR_SAVE_SVG = function (svgText, filename) {
    save(new Blob([svgText], { type: "image/svg+xml" }), filename);
  };
  window.AIR_SAVE_TEXT = function (text, filename, type) {
    save(new Blob([text], { type: type || "text/plain" }), filename);
  };
  window.AIR_ZIP_FILES = function (entries, filename) {
    save(zip(entries.map(function (e) {
      return { name: e.name, data: typeof e.data === "string" ? enc.encode(e.data) : e.data };
    })), filename);
  };
})();
