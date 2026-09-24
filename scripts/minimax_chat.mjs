// Minimal MiniMax M3 client for the Node eval/feedback scripts. Same wire shape
// as scripts/minimax_chat.py (Anthropic-compatible Messages endpoint), so only
// text blocks come back and thinking blocks are dropped.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const BASE_URL = (process.env.MINIMAX_BASE_URL || "https://api.minimax.io/anthropic").replace(/\/$/, "");
export const MINIMAX_MODEL = process.env.MINIMAX_MODEL || "MiniMax-M3";

// Env first, then the same .env files the scripts already read the chat token from.
export function loadMinimaxKey() {
  if (process.env.MINIMAX_API_KEY) return process.env.MINIMAX_API_KEY.trim();
  for (const p of [join(HERE, "..", "..", "AI Agent", ".env"), join(HERE, "..", ".env")]) {
    try { const m = readFileSync(p, "utf8").match(/^MINIMAX_API_KEY\s*=\s*(.+)$/m); if (m) return m[1].trim(); }
    catch { /* next */ }
  }
  return null;
}

export async function minimaxChat(key, system, user, { maxTokens = 2000, temperature = 0.2 } = {}) {
  const r = await fetch(`${BASE_URL}/v1/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({
      model: MINIMAX_MODEL, max_tokens: maxTokens, temperature, system,
      messages: [{ role: "user", content: user }],
    }),
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(`MiniMax ${r.status}: ${JSON.stringify(d).slice(0, 200)}`);
  const text = (d.content || []).filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  if (!text) throw new Error(`MiniMax returned no text (stop_reason=${d.stop_reason})`);
  return text;
}

// Model replies sometimes wrap JSON in markdown fences.
export function parseJsonReply(text) {
  let t = text.trim();
  if (t.startsWith("```")) t = t.split("```")[1].replace(/^json/, "").trim();
  return JSON.parse(t);
}
