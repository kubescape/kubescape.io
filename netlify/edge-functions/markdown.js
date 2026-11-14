function parseAccept(header) {
  if (!header) return [];
  const entries = [];
  const parts = header.split(",");
  for (let i = 0; i < parts.length; i++) {
    const raw = parts[i].trim();
    if (!raw) continue;
    const tokens = raw.split(";").map((t) => t.trim());
    const mediaType = tokens[0].toLowerCase();
    let q = 1.0;
    for (let j = 1; j < tokens.length; j++) {
      const param = tokens[j];
      const eq = param.indexOf("=");
      if (eq !== -1) {
        const key = param.slice(0, eq).trim().toLowerCase();
        const val = param.slice(eq + 1).trim();
        if (key === "q") {
          const parsed = Number(val);
          q = Number.isFinite(parsed) ? Math.max(0, Math.min(1, parsed)) : 0;
        }
      }
    }
    entries.push({ mediaType, q, index: i });
  }
  return entries;
}

function matchEntry(entries, targetType) {
  const [targetMain, targetSub] = targetType.split("/");
  let best = null;
  let bestSpecificity = 0;

  for (const entry of entries) {
    const [main, sub] = entry.mediaType.split("/");
    let specificity = 0;
    if (main === targetMain && sub === targetSub) {
      specificity = 3;
    } else if (main === targetMain && sub === "*") {
      specificity = 2;
    } else if (main === "*" && sub === "*") {
      specificity = 1;
    }

    if (specificity > bestSpecificity) {
      bestSpecificity = specificity;
      best = { ...entry, specificity };
    }
  }
  return best;
}

function prefersMarkdown(acceptHeader) {
  if (!acceptHeader) return false;
  const entries = parseAccept(acceptHeader);
  const mdMatch = matchEntry(entries, "text/markdown");
  if (!mdMatch || mdMatch.q <= 0) return false;

  const htmlMatch = matchEntry(entries, "text/html");
  if (!htmlMatch || htmlMatch.q <= 0) return true;

  if (mdMatch.q > htmlMatch.q) return true;
  if (mdMatch.q < htmlMatch.q) return false;

  if (mdMatch.specificity > htmlMatch.specificity) return true;
  if (mdMatch.specificity < htmlMatch.specificity) return false;

  if (mdMatch.specificity === 1 && htmlMatch.specificity === 1) return false;

  return mdMatch.index < htmlMatch.index;
}

function withVaryAccept(response) {
  if (!response) return response;
  const headers = new Headers(response.headers);
  const current = headers.get("Vary");
  if (!current) {
    headers.set("Vary", "Accept");
  } else {
    const list = current.split(",").map((s) => s.trim().toLowerCase());
    if (!list.includes("accept")) {
      headers.set("Vary", `${current}, Accept`);
    }
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export default async (request, context) => {
  const url = new URL(request.url);
  if (!url.pathname.endsWith("/")) {
    return context && typeof context.next === "function" ? context.next() : undefined;
  }

  if (!prefersMarkdown(request.headers.get("accept"))) {
    if (context && typeof context.next === "function") {
      const response = await context.next();
      return withVaryAccept(response);
    }
    return;
  }

  const markdown = await fetch(new URL(url.pathname + "index.md", url));
  if (!markdown.ok) {
    if (context && typeof context.next === "function") {
      const response = await context.next();
      return withVaryAccept(response);
    }
    return;
  }

  const headers = new Headers({
    "Content-Type": "text/markdown; charset=utf-8",
    "Vary": "Accept",
  });
  for (const name of ["Cache-Control", "ETag"]) {
    if (markdown.headers.has(name)) headers.set(name, markdown.headers.get(name));
  }
  return new Response(markdown.body, { headers });
};

export const config = {
  path: "/*",
  onError: "bypass",
};

export { prefersMarkdown, withVaryAccept };
