import { NextResponse } from "next/server";

export async function POST(req: Request) {
  const { title, description, source } = await req.json();

  // 🔍 Simple heuristic rules (hackathon-safe)
  let score = 0;

  const suspiciousWords = [
    "shocking", "breaking!!!", "you won't believe",
    "miracle", "exposed", "secret", "hoax"
  ];

  suspiciousWords.forEach(word => {
    if (
      title?.toLowerCase().includes(word) ||
      description?.toLowerCase().includes(word)
    ) {
      score += 1;
    }
  });

  // Trusted sources = boost credibility
  const trustedSources = ["bbc", "cnn", "guardian", "reuters"];
  const isTrusted = trustedSources.some(s =>
    source?.toLowerCase().includes(s)
  );

  let verdict = "Unverified";

  if (isTrusted && score === 0) verdict = "Real";
  if (score >= 2) verdict = "Likely Fake";

  return NextResponse.json({
    verdict,
    confidence:
      verdict === "Real" ? "0.85"
      : verdict === "Likely Fake" ? "0.30"
      : "0.55",
    signals: {
      suspiciousScore: score,
      trustedSource: isTrusted
    }
  });
}
