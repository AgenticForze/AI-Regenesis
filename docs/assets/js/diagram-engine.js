/*
 * diagram-engine.js — a faithful JS port of skills/quick-reference-engine/scripts/svg_engine.py's Diagram
 * class, trimmed to the subset that skill actually uses (no row-labels/spine branch — the quick-reference
 * pattern builders never call add_row with a label, only the deep8 engine does, and this page only needs
 * the 8 quick-reference patterns). Verified line-for-line against the Python engine's output before shipping
 * — see the isolation test this was built alongside for the exact diff-based comparison.
 *
 * Ported constants, wrap logic, node layout, edge-path routing (including the same-row vs. cross-row
 * branch and the elbow-connector math), and card rendering are all deliberately kept 1:1 with the Python
 * source rather than "improved" — any visual quirk in the Python engine (see quick-reference-engine's own
 * lessons-learned.md) will reproduce identically here, which is the point: this is the same engine, just
 * running in the browser instead of on a server.
 */

const BOX_W = 250;
const BOX_H_MIN = 92; // unused directly (box_h computed dynamically, same as Python) — kept for reference
const ROW_GAP = 78;
const COL_GAP = 26;
const MARGIN = 46;
const TITLE_SIZE = 15.5;
const SUB_SIZE = 12.5;
const TITLE_LINE_H = 20;
const SUB_LINE_H = 17;
const CORNER_R = 16;
const ARROW_COLOR = "#9AA3AE";

const COLORS = {
  data:   { fill: "#F2EEE3", stroke: "#C7BC9E", title: "#4A4432", sub: "#8C8365" },
  orch:   { fill: "#DCEBFB", stroke: "#5B93C9", title: "#1C4A73", sub: "#3E6D93" },
  agent:  { fill: "#DBF2E7", stroke: "#4FAE83", title: "#1B5E3D", sub: "#3D8261" },
  action: { fill: "#FBE8CE", stroke: "#D89A3F", title: "#7A4E12", sub: "#9C6B22" },
  obs:    { fill: "#EAE1F8", stroke: "#9575CD", title: "#4A2E7A", sub: "#6B4A9E" },
};

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Same word-wrap behavior as Python's textwrap.wrap(width=..., break_long_words=False) for the common case
// (no single word longer than the wrap width). Two things had to be ported deliberately, not just the
// obvious greedy line-fill:
//   1. textwrap's default break_on_hyphens=True splits at internal hyphens as wrap points (a naive
//      whitespace-only split treats "High-Blast-Radius" as one atomic 18-char chunk and wraps it onto its
//      own line even when "High-" alone would have fit the previous line — verified against real Python
//      output before this fix: it produced a 3-line label where Python produces 2, which silently changed
//      the whole diagram's canvas height for any use case with a hyphenated node label).
//   2. the hyphen stays attached to the end of the piece before the break, and there's no space between
//      hyphen-split pieces of the same original word (unlike the space between separate words).
function splitHyphenated(word) {
  const parts = word.split("-");
  if (parts.length === 1) return [{ text: word, spaceBefore: true }];
  return parts.map((p, i) => ({
    text: i < parts.length - 1 ? p + "-" : p,
    spaceBefore: i === 0, // only the first sub-piece carries the word-boundary space; the rest glue on
  }));
}

function wrapText(text, width, maxLines) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const pieces = [];
  words.forEach((w, i) => {
    const sub = splitHyphenated(w);
    sub.forEach((p, j) => pieces.push({ text: p.text, spaceBefore: j === 0 ? i > 0 : false }));
  });

  const lines = [];
  let cur = "";
  for (const piece of pieces) {
    const sep = piece.spaceBefore && cur ? " " : "";
    const candidate = cur + sep + piece.text;
    if (candidate.length <= width) {
      cur = candidate;
    } else {
      if (cur) lines.push(cur);
      cur = piece.text;
    }
  }
  if (cur) lines.push(cur);
  if (lines.length > maxLines) {
    const truncated = lines.slice(0, maxLines);
    let last = truncated[truncated.length - 1];
    if (last.length > width - 1) last = last.slice(0, width - 1);
    truncated[truncated.length - 1] = last.replace(/\s+$/, "") + "…";
    return truncated;
  }
  return lines;
}

class Node {
  constructor(id, title, subtitle, colorKey) {
    this.id = id;
    this.titleLines = wrapText(title, 24, 3);
    this.subLines = wrapText(subtitle, 30, 2);
    this.colorKey = colorKey;
    this.cx = 0;
    this.cy = 0;
  }
}

class Diagram {
  constructor() {
    this.rows = [];
    this._nodes = {};
  }

  addRow(nodes) {
    for (const n of nodes) this._nodes[n.id] = n;
    this.rows.push(nodes);
    return nodes;
  }

  edge(a, b, opts = {}) {
    if (!this.edges) this.edges = [];
    this.edges.push({ a, b, dashed: !!opts.dashed, bidir: !!opts.bidir });
  }

  node(id, title, subtitle, colorKey) {
    const n = new Node(id, title, subtitle, colorKey);
    this._nodes[id] = n;
    return n;
  }

  render() {
    this.edges = this.edges || [];
    let maxBlockH = 0;
    for (const row of this.rows) {
      for (const n of row) {
        const blockH = n.titleLines.length * TITLE_LINE_H + n.subLines.length * SUB_LINE_H;
        maxBlockH = Math.max(maxBlockH, blockH);
      }
    }
    const boxH = maxBlockH + 48;

    const rowWidths = this.rows.map(row => row.length * BOX_W + Math.max(0, row.length - 1) * COL_GAP);
    const contentW = Math.max(...rowWidths, BOX_W) + 2 * MARGIN;
    const canvasW = contentW;
    const canvasH = MARGIN + this.rows.length * boxH + Math.max(0, this.rows.length - 1) * ROW_GAP + MARGIN;

    this.rows.forEach((row, ri) => {
      const rowW = rowWidths[ri];
      const startX = (contentW - rowW) / 2;
      const cy = MARGIN + ri * (boxH + ROW_GAP) + boxH / 2;
      row.forEach((n, ci) => {
        n.cx = startX + ci * (BOX_W + COL_GAP) + BOX_W / 2;
        n.cy = cy;
      });
    });

    const svg = [
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${canvasW.toFixed(0)} ${canvasH.toFixed(0)}" font-family="'Inter','IBM Plex Sans',-apple-system,sans-serif">`,
      "<defs>",
      '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
      `<path d="M0,0 L10,5 L0,10 z" fill="${ARROW_COLOR}"/>`,
      "</marker>",
      '<filter id="cardshadow" x="-20%" y="-20%" width="140%" height="140%">',
      '<feDropShadow dx="0" dy="1.5" stdDeviation="2.5" flood-color="#1a1a1a" flood-opacity="0.08"/>',
      "</filter>",
      "</defs>",
      `<rect x="0" y="0" width="${canvasW.toFixed(0)}" height="${canvasH.toFixed(0)}" fill="#FFFFFF"/>`,
    ];

    for (const e of this.edges) {
      const na = this._nodes[e.a], nb = this._nodes[e.b];
      svg.push(this._edgePath(na, nb, boxH, e.dashed, e.bidir));
    }

    for (const row of this.rows) {
      for (const n of row) svg.push(this._card(n, boxH));
    }

    svg.push("</svg>");
    return svg.join("\n");
  }

  _edgePath(na, nb, boxH, dashed, bidir) {
    const dash = dashed ? ' stroke-dasharray="5 4"' : "";
    const markerStart = bidir ? ' marker-start="url(#arrow)"' : "";
    let d;
    if (Math.abs(na.cy - nb.cy) < 1) {
      let x1, y1, x2, y2;
      if (na.cx < nb.cx) {
        x1 = na.cx + BOX_W / 2; y1 = na.cy;
        x2 = nb.cx - BOX_W / 2; y2 = nb.cy;
      } else {
        x1 = na.cx - BOX_W / 2; y1 = na.cy;
        x2 = nb.cx + BOX_W / 2; y2 = nb.cy;
      }
      d = `M ${x1.toFixed(1)} ${y1.toFixed(1)} L ${x2.toFixed(1)} ${y2.toFixed(1)}`;
    } else {
      const x1 = na.cx, y1 = na.cy + boxH / 2;
      const x2 = nb.cx, y2 = nb.cy - boxH / 2;
      if (Math.abs(x1 - x2) < 1) {
        d = `M ${x1.toFixed(1)} ${y1.toFixed(1)} L ${x2.toFixed(1)} ${y2.toFixed(1)}`;
      } else {
        const r = 12;
        const midY = (y1 + y2) / 2;
        const sign = x2 > x1 ? 1 : -1;
        d = `M ${x1.toFixed(1)} ${y1.toFixed(1)} ` +
            `L ${x1.toFixed(1)} ${(midY - r).toFixed(1)} ` +
            `Q ${x1.toFixed(1)} ${midY.toFixed(1)} ${(x1 + r * sign).toFixed(1)} ${midY.toFixed(1)} ` +
            `L ${(x2 - r * sign).toFixed(1)} ${midY.toFixed(1)} ` +
            `Q ${x2.toFixed(1)} ${midY.toFixed(1)} ${x2.toFixed(1)} ${(midY + r).toFixed(1)} ` +
            `L ${x2.toFixed(1)} ${y2.toFixed(1)}`;
      }
    }
    return `<path d="${d}" fill="none" stroke="${ARROW_COLOR}" stroke-width="1.75"${dash} marker-end="url(#arrow)"${markerStart}/>`;
  }

  _card(n, boxH) {
    const c = COLORS[n.colorKey];
    const x = n.cx - BOX_W / 2;
    const y = n.cy - boxH / 2;
    const parts = [
      '<g filter="url(#cardshadow)">',
      `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${BOX_W}" height="${boxH.toFixed(0)}" rx="${CORNER_R}" fill="${c.fill}" stroke="${c.stroke}" stroke-width="1.5"/>`,
      "</g>",
    ];
    const nTitleLines = n.titleLines.length;
    const nSubLines = n.subLines.length;
    const blockH = nTitleLines * TITLE_LINE_H + nSubLines * SUB_LINE_H;
    const top = n.cy - blockH / 2;
    let ty = top + TITLE_LINE_H * 0.78;
    for (const line of n.titleLines) {
      parts.push(`<text x="${n.cx.toFixed(1)}" y="${ty.toFixed(1)}" text-anchor="middle" font-size="${TITLE_SIZE}" font-weight="600" fill="${c.title}">${esc(line)}</text>`);
      ty += TITLE_LINE_H;
    }
    let sy = top + nTitleLines * TITLE_LINE_H + SUB_LINE_H * 0.72;
    for (const line of n.subLines) {
      parts.push(`<text x="${n.cx.toFixed(1)}" y="${sy.toFixed(1)}" text-anchor="middle" font-size="${SUB_SIZE}" fill="${c.sub}">${esc(line)}</text>`);
      sy += SUB_LINE_H;
    }
    return parts.join("\n");
  }
}

// ---------------------------------------------------------------------------------------------------------
// The 8 pattern builders — 1:1 port of skills/quick-reference-engine/scripts/svg_patterns.py.
// Each takes the same argument shape as the Python version (arrays instead of lists).
// ---------------------------------------------------------------------------------------------------------

const L_DATA = "Data & Integration";
const L_ORCH = "Orchestration";
const L_AGENT = "Specialist Agent";
const L_ACTION = "Action & Execution";

function orchestratorWorker(title, orchestrator, workers, dataSources, actions, humanGate) {
  const d = new Diagram();
  const dataNodes = dataSources.map((s, i) => d.node(`d${i}`, s, L_DATA, "data"));
  d.addRow(dataNodes);
  const orch = d.node("orch", orchestrator, L_ORCH, "orch");
  d.addRow([orch]);
  const workerNodes = workers.map((w, i) => d.node(`w${i}`, w, L_AGENT, "agent"));
  d.addRow(workerNodes);
  const agg = d.node("agg", "Aggregator / Synthesis Agent", "Combines findings", "agent");
  d.addRow([agg]);
  let gate;
  if (humanGate) {
    gate = d.node("gate", humanGate, "Human review", "obs");
    d.addRow([gate]);
  }
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  for (const n of dataNodes) d.edge(n.id, "orch");
  for (const n of workerNodes) { d.edge("orch", n.id); d.edge(n.id, "agg"); }
  if (humanGate) {
    d.edge("agg", "gate");
    for (const n of actNodes) d.edge("gate", n.id);
  } else {
    for (const n of actNodes) d.edge("agg", n.id);
  }
  return d.render();
}

function hierarchical(title, top, midLayer, leavesByMid, actions) {
  const d = new Diagram();
  const topN = d.node("top", top, L_ORCH, "orch");
  d.addRow([topN]);
  const midNodes = midLayer.map((m, i) => d.node(`m${i}`, m, "Domain Manager", "agent"));
  d.addRow(midNodes);
  const leafNodes = [];
  leavesByMid.forEach((leaves, i) => {
    leaves.forEach((leaf, j) => leafNodes.push([i, d.node(`l${i}_${j}`, leaf, L_AGENT, "agent")]));
  });
  d.addRow(leafNodes.map(([, n]) => n));
  const res = d.node("res", "Resolution / Reporting Agent", "Consolidates output", "agent");
  d.addRow([res]);
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  for (const n of midNodes) d.edge("top", n.id);
  for (const [i, n] of leafNodes) d.edge(`m${i}`, n.id);
  d.edge("top", "res");
  for (const n of actNodes) d.edge("res", n.id);
  return d.render();
}

function pipeline(title, stages, actions) {
  const d = new Diagram();
  stages.forEach((s, i) => {
    const n = d.node(`s${i}`, s, `Stage ${i + 1} of ${stages.length}`, "agent");
    d.addRow([n]);
  });
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  for (let i = 0; i < stages.length - 1; i++) d.edge(`s${i}`, `s${i + 1}`);
  for (const n of actNodes) d.edge(`s${stages.length - 1}`, n.id);
  return d.render();
}

function blackboard(title, controller, agents, storeName, actions) {
  const d = new Diagram();
  const store = d.node("store", storeName, "Shared Data Layer", "data");
  d.addRow([store]);
  const ctrl = d.node("ctrl", controller, L_ORCH, "orch");
  d.addRow([ctrl]);
  const agentNodes = agents.map((a, i) => d.node(`ag${i}`, a, "Reads / writes blackboard", "agent"));
  d.addRow(agentNodes);
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  d.edge("store", "ctrl", { bidir: true });
  for (const n of agentNodes) d.edge("ctrl", n.id, { dashed: true });
  for (const n of actNodes) d.edge("ctrl", n.id);
  return d.render();
}

function debateCritique(title, proposer, critic, arbiter, refs, actions) {
  const d = new Diagram();
  const refNodes = refs.map((r, i) => d.node(`r${i}`, r, L_DATA, "data"));
  d.addRow(refNodes);
  const p = d.node("p", proposer, "Proposes", "agent");
  const c = d.node("c", critic, "Challenges", "agent");
  d.addRow([p, c]);
  const arb = d.node("arb", arbiter, "Final decision", "orch");
  d.addRow([arb]);
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  for (const n of refNodes) d.edge(n.id, "p");
  d.edge("p", "c");
  d.edge("c", "p", { dashed: true });
  d.edge("c", "arb");
  for (const n of actNodes) d.edge("arb", n.id);
  return d.render();
}

function marketBased(title, auctioneer, bidders, actions) {
  const d = new Diagram();
  const ctx = d.node("ctx", "Live Market / Resource State", L_DATA, "data");
  d.addRow([ctx]);
  const auc = d.node("auc", auctioneer, L_ORCH, "orch");
  d.addRow([auc]);
  const bidderNodes = bidders.map((b, i) => d.node(`b${i}`, b, "Submits bids", "agent"));
  d.addRow(bidderNodes);
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  d.edge("ctx", "auc");
  for (const n of bidderNodes) d.edge(n.id, "auc");
  for (const n of actNodes) d.edge("auc", n.id);
  return d.render();
}

function eventSwarm(title, busName, agents, actions) {
  const d = new Diagram();
  const bus = d.node("bus", busName, "Event Bus", "data");
  d.addRow([bus]);
  const agentNodes = agents.map((a, i) => d.node(`ag${i}`, a, "Reactive agent", "agent"));
  d.addRow(agentNodes);
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  for (const n of agentNodes) { d.edge("bus", n.id); d.edge(n.id, "bus", { dashed: true }); }
  for (const n of actNodes) d.edge("bus", n.id);
  return d.render();
}

function humanEscalation(title, autoAgents, escalationGate, humanRole, actions) {
  const d = new Diagram();
  autoAgents.forEach((a, i) => {
    const n = d.node(`aa${i}`, a, `Automation step ${i + 1}`, "agent");
    d.addRow([n]);
  });
  const gate = d.node("gate", escalationGate, "Confidence / risk check", "orch");
  d.addRow([gate]);
  const auto = d.node("auto", "Auto-resolve", "Low risk / high confidence", "agent");
  const human = d.node("human", humanRole, "High risk / low confidence", "obs");
  d.addRow([auto, human]);
  const actNodes = actions.map((a, i) => d.node(`a${i}`, a, L_ACTION, "action"));
  d.addRow(actNodes);

  for (let i = 0; i < autoAgents.length - 1; i++) d.edge(`aa${i}`, `aa${i + 1}`);
  d.edge(`aa${autoAgents.length - 1}`, "gate");
  d.edge("gate", "auto");
  d.edge("gate", "human");
  d.edge("human", "auto", { dashed: true });
  for (const n of actNodes) d.edge("auto", n.id);
  return d.render();
}

const BUILDERS = {
  "orchestrator-worker": orchestratorWorker,
  "hierarchical": hierarchical,
  "pipeline": pipeline,
  "blackboard": blackboard,
  "debate-critique": debateCritique,
  "market-based": marketBased,
  "event-swarm": eventSwarm,
  "human-escalation": humanEscalation,
};

// ---------------------------------------------------------------------------------------------------------
// Build order — 1:1 port of skills/quick-reference-engine/scripts/build_order.py.
// ---------------------------------------------------------------------------------------------------------

function pl(n, singular, plural) { return n === 1 ? singular : (plural || singular + "s"); }

const BUILD_ORDER_BUILDERS = {
  "orchestrator-worker": (uc) => {
    const { orchestrator: orch, workers, human_gate: gate } = uc;
    return [
      `**Phase 1 — one worker, no fan-out.** Wire a single path end to end: ${workers[0]} reading real data and producing a result, with ${orch} just passing data through untouched. Prove the data pipeline and one agent's reasoning before adding parallelism.`,
      `**Phase 2 — add the fan-out.** Bring the remaining ${workers.length - 1} worker agent${workers.length > 2 ? "s" : ""} online in parallel and build ${orch}'s aggregation/synthesis logic. This is where the orchestrator-worker pattern is actually learned — watch for race conditions and partial-failure handling here, not before.`,
      gate
        ? `**Phase 3 — add the governance gate.** Wire in the human checkpoint: ${gate}.`
        : `**Phase 3 — add the governance gate.** Add policy/guardrail checks the aggregator's output must clear before it reaches the action layer.`,
      `**Phase 4 — observability and feedback.** Trace every worker call, monitor the aggregator's decision quality against real outcomes, and add a feedback loop that catches drift before it becomes a production incident.`,
    ];
  },
  "hierarchical": (uc) => {
    const { top, mid_layer: mid } = uc;
    return [
      `**Phase 1 — one branch only.** Build ${top} talking to just ${mid[0]} and that manager's own leaf agents, ignoring the other ${mid.length - 1} branch${mid.length > 2 ? "es" : ""} entirely. Prove one full manager-to-leaf chain before replicating it.`,
      `**Phase 2 — add the remaining branches.** Bring ${mid.slice(1).join(", ")} online, each with their own leaf agents. Build ${top}'s cross-branch consolidation logic — this is the actual hard part of the hierarchical pattern, not any single branch.`,
      `**Phase 3 — resolve cross-branch conflicts.** Real inputs will disagree across managers (different branches recommending incompatible actions); add explicit conflict-resolution logic at ${top} rather than letting the last branch to report silently win.`,
      `**Phase 4 — observability and feedback.** Trace decisions at every level of the hierarchy separately (top orchestrator, each manager, each leaf) so a bad outcome can be traced to the specific branch and level that caused it.`,
    ];
  },
  "pipeline": (uc) => {
    const { stages } = uc;
    return [
      `**Phase 1 — the first two stages only.** Get ${stages[0]} feeding ${stages[1]} correctly, with the rest of the pipeline stubbed out. Durability matters more than completeness here — make sure a crash mid-pipeline doesn't lose or duplicate work.`,
      `**Phase 2 — the full chain.** Add the remaining ${stages.length - 2} stage${stages.length - 2 !== 1 ? "s" : ""} in order, testing each newly-added stage against real output from the stage before it, not synthetic test data.`,
      `**Phase 3 — add retry and partial-failure handling.** Decide, stage by stage, what happens when that specific stage fails: retry, skip, or halt the whole pipeline. This decision is different per stage and shouldn't be a single global policy.`,
      `**Phase 4 — observability and feedback.** Add per-stage tracing so a slow or wrong pipeline run can be attributed to one specific stage, and track output quality over time to catch silent degradation in an early stage before it compounds downstream.`,
    ];
  },
  "blackboard": (uc) => {
    const { controller: ctrl, agents } = uc;
    return [
      `**Phase 1 — one agent writing to the blackboard.** Get ${agents[0]} reading and writing the shared store with ${ctrl} just reading it back out, no synthesis logic yet. Prove the shared-state read/write mechanics before adding more writers.`,
      `**Phase 2 — add the remaining agents.** Bring ${agents.slice(1).join(", ")} online, each writing independently to the blackboard. Build ${ctrl}'s synthesis logic — deciding which agent to trigger next and how to combine partial, sometimes-conflicting findings.`,
      `**Phase 3 — add a minimum-evidence threshold.** An early blackboard system will over-synthesize from sparse data; require a minimum number of corroborating agent findings before the controller surfaces a conclusion.`,
      `**Phase 4 — observability and feedback.** Snapshot the blackboard's state history so any synthesized conclusion can be traced back to exactly which agent findings produced it.`,
    ];
  },
  "debate-critique": (uc) => {
    const { proposer, critic, arbiter } = uc;
    return [
      `**Phase 1 — the proposer alone.** Get ${proposer} producing a hypothesis from real data, with no critic yet — this is just a single-pass classifier/recommender at this stage, and that's fine.`,
      `**Phase 2 — add the critic, fully independent.** Build ${critic} with no visibility into the proposer's reasoning — separate context, separate prompt. This independence is the entire point of the pattern; skipping it turns the critic into a rubber stamp.`,
      `**Phase 3 — add ${arbiter} and calibrate.** Build the arbitration logic, then run it against a set of cases with known-correct outcomes to calibrate how much weight the critic's pushback should carry before trusting it on live decisions.`,
      `**Phase 4 — observability and feedback.** Track how often the arbiter overrides the proposer and whether those overrides were actually correct — this tells you whether the critic is earning its place in the pipeline or just adding latency.`,
    ];
  },
  "market-based": (uc) => {
    const { auctioneer: auc, bidders } = uc;
    return [
      `**Phase 1 — two bidders, manual clearing.** Get ${bidders[0]} and ${bidders.length > 1 ? bidders[1] : bidders[0]} submitting bids with ${auc} clearing them on a fixed schedule — no real-time re-clearing yet.`,
      `**Phase 2 — add the remaining bidders and automate clearing.** Bring the rest of the bidder population online and move ${auc} to event-triggered (not just scheduled) clearing.`,
      `**Phase 3 — add hard guardrails independent of the market mechanism.** A pure auction can clear at a technically-valid but operationally-bad price; add a guardrail service that can veto a clearing result regardless of what the market mechanism decided.`,
      `**Phase 4 — observability and feedback.** Track clearing-price trends and bidder participation over time — a market that's stopped clearing efficiently is a slow-motion failure that won't show up in any single transaction.`,
    ];
  },
  "event-swarm": (uc) => {
    const { bus_name: bus, agents } = uc;
    return [
      `**Phase 1 — one reactive agent.** Get ${agents[0]} subscribed to ${bus} and reacting to real events, with no other agents listening yet. Prove the event-driven mechanics work under real event volume before adding more subscribers.`,
      `**Phase 2 — add the remaining agents.** Bring ${agents.slice(1).join(", ")} online as independent subscribers. Test what happens when multiple agents react to the *same* event — this is where swarm-specific bugs (duplicate actions, conflicting responses) show up.`,
      `**Phase 3 — add rate limits and blast-radius guardrails.** A reactive swarm with no shared coordination can act on the same trigger repeatedly; add per-agent and global rate limits before connecting real downstream actions.`,
      `**Phase 4 — observability and feedback.** Add distributed tracing across the event bus so a cascading reaction across multiple agents can be reconstructed after the fact, not just guessed at.`,
    ];
  },
  "human-escalation": (uc) => {
    const { auto_agents: autoAgents, escalation_gate: gate, human_role: human } = uc;
    return [
      `**Phase 1 — the automation chain, no gate yet.** Get ${autoAgents.join(" → ")} working end to end against real data, routing every single case to ${human} for now — automation logic before automation trust.`,
      `**Phase 2 — add ${gate} in shadow mode.** Let the gate score every case and log what it *would* route, but keep sending everything to ${human} regardless. Compare the gate's decisions against what the human actually did.`,
      `**Phase 3 — turn on auto-resolve for the highest-confidence tier only.** Once shadow-mode data shows the gate agrees with ${human} at very high confidence, let only that top tier bypass the human — keep everything else routed to review.`,
      `**Phase 4 — observability and feedback.** Track the auto-resolve tier's real-world accuracy continuously, not just at launch, and be willing to narrow the auto-resolve criteria back down if accuracy drifts.`,
    ];
  },
};

function buildOrderFor(uc) {
  return BUILD_ORDER_BUILDERS[uc.pattern](uc);
}

// Export for both browser (window) and Node (module.exports, used only by the isolation test).
const DiagramEngine = { BUILDERS, buildOrderFor, Diagram, esc, wrapText };
if (typeof module !== "undefined" && module.exports) {
  module.exports = DiagramEngine;
} else {
  window.DiagramEngine = DiagramEngine;
}
