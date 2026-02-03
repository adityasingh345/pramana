'use client'

import Link from 'next/link'

const cases = [
  {
    id: 'MDRS-2026-001',
    type: 'Health Misinformation',
    verdict: 'Fake',
    risk: 'High',
    laws: ['IT Act 66D', 'IPC 505(1)'],
    status: 'Pending Review',
  },
  {
    id: 'MDRS-2026-002',
    type: 'Political Deepfake',
    verdict: 'Under Investigation',
    risk: 'Medium',
    laws: ['IPC 171G'],
    status: 'Escalated',
  },
  {
    id: 'MDRS-2026-003',
    type: 'Public Panic Rumor',
    verdict: 'Fake',
    risk: 'High',
    laws: ['Disaster Management Act'],
    status: 'Reviewed',
  },
]

export default function LegalDocketPage() {
  return (
    <div style={{ maxWidth: 1000, margin: '40px auto' }}>
      <Link href="/">← Back</Link>

      <h1 style={{ marginTop: 20 }}>🏛 Legal Review Desk</h1>
      <p style={{ opacity: 0.7 }}>
        Court-assisted intake view of misinformation cases flagged by MDRS
      </p>

      {cases.map((c) => (
        <div
          key={c.id}
          style={{
            border: '1px solid #ddd',
            borderRadius: 8,
            padding: 20,
            marginTop: 20,
          }}
        >
          <h3>{c.id}</h3>
          <p><b>Content Type:</b> {c.type}</p>
          <p><b>Verdict:</b> {c.verdict}</p>
          <p><b>Legal Risk:</b> {c.risk}</p>
          <p><b>Applicable Laws:</b> {c.laws.join(', ')}</p>
          <p><b>Status:</b> {c.status}</p>

          <button style={{ marginTop: 10 }}>
            📄 Download Evidence Pack
          </button>
        </div>
      ))}
    </div>
  )
}
