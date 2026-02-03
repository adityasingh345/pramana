// app/authority/page.tsx

import Parser from "rss-parser";

/* ---------------- TYPES ---------------- */

type NewsItem = {
  title?: string;
  link?: string;
  pubDate?: string;
  contentSnippet?: string;
  analysis?: {
    verdict: "Real" | "Unverified" | "Likely Fake";
    confidence: string;
  };
};

/* ---------------- RSS PARSER ---------------- */

const parser = new Parser({
  headers: {
    "User-Agent": "Mozilla/5.0 (Next.js RSS Reader)",
    Accept: "application/rss+xml",
  },
});

/* ---------------- FETCH RSS ---------------- */

async function getTopNews(): Promise<NewsItem[]> {
  const RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml";
  const feed = await parser.parseURL(RSS_URL);
  return feed.items.slice(0, 10);
}

/* ---------------- PAGE ---------------- */

export default async function AuthorityPage() {
  // 1️⃣ Fetch RSS
  const news = await getTopNews();

  // 2️⃣ Add SAFE default analysis (NO backend)
  const enrichedNews: NewsItem[] = news.map((item) => ({
    ...item,
    analysis: {
      verdict: "Unverified",
      confidence: "0.50",
    },
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-5xl mx-auto px-6 py-10">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-800">
              Authority News
            </h1>
            <p className="text-slate-600 mt-1">
              Top 10 updates from trusted RSS sources
            </p>
          </div>

          <span className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
            ● Live RSS
          </span>
        </div>

        {/* News Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {enrichedNews.map((item, index) => (
            <article
              key={index}
              className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition"
            >
              <a
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="block"
              >
                <h2 className="text-lg font-semibold text-slate-800 hover:text-blue-600 transition line-clamp-2">
                  {item.title}
                </h2>

                <p className="text-xs text-slate-500 mt-2">
                  🕒 {item.pubDate}
                </p>

                <p className="text-slate-600 mt-3 text-sm line-clamp-3">
                  {item.contentSnippet}
                </p>

                <div className="mt-4 flex items-center justify-between">
                  <span className="text-xs px-2 py-1 rounded font-medium bg-yellow-100 text-yellow-700">
                    {item.analysis?.verdict} • {item.analysis?.confidence}
                  </span>

                  <span className="text-sm text-blue-600 font-medium">
                    Read →
                  </span>
                </div>
              </a>
            </article>
          ))}
        </div>

        <p className="text-center text-xs text-slate-500 mt-10">
          Data fetched live from BBC RSS • Server-rendered
        </p>
      </div>
    </div>
  );
}
