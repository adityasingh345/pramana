'use client'

import { useState } from 'react'
import Link from 'next/link'

const mockPosts = [
  {
    id: 1,
    title: 'False Rumors About Celebrity Death Circulating Online',
    content:
      'Cyber authorities have identified viral messages claiming the death of a public figure due to illness. After verification with official sources and family statements, this claim has been found to be false. Citizens are advised not to forward such messages.',
    verdict: 'Fake',
    issued_by: 'Cyber Crime Cell, India',
    timestamp: '30 Jan 2026',
  },
  {
    id: 2,
    title: 'Fake Government Cash Transfer Messages on WhatsApp',
    content:
      'Messages claiming that the government is offering ₹5000 to all citizens via a registration link are false. No such scheme has been announced by any official department. These messages are part of an online scam.',
    verdict: 'Fake',
    issued_by: 'Ministry of Electronics & IT',
    timestamp: '28 Jan 2026',
  },
  {
    id: 3,
    title: 'Earthquake Alert Messages – Clarification Issued',
    content:
      'Social media posts warning of an imminent earthquake are misleading. Earthquakes cannot be predicted with precise timing. Citizens are advised to rely only on official alerts from authorized agencies.',
    verdict: 'Verified',
    issued_by: 'National Disaster Management Authority',
    timestamp: '26 Jan 2026',
  },
  {
    id: 4,
    title: 'Deepfake Video Circulating of Political Leader',
    content:
      'A manipulated video of a political leader is circulating online. Preliminary analysis indicates signs of synthetic media. The matter is currently under investigation.',
    verdict: 'Under Investigation',
    issued_by: 'Election Cyber Monitoring Cell',
    timestamp: '25 Jan 2026',
  },
]

interface Comment {
  id: number
  text: string
}

export default function AuthorityPage() {
  const [selectedPost, setSelectedPost] = useState(mockPosts[0])
  const [comments, setComments] = useState<Comment[]>([])
  const [input, setInput] = useState('')

  const addComment = () => {
    if (!input.trim()) return
    setComments([...comments, { id: Date.now(), text: input }])
    setInput('')
  }

  return (
    <div style={{ maxWidth: 1100, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <Link href="/" style={{ textDecoration: 'none' }}>← Back to Home</Link>

      {/* Authority Feed + Selected Advisory */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 2fr',
          gap: 30,
          marginTop: 20,
        }}
      >
        {/* LEFT: Authority Feed */}
        <div style={{ borderRight: '1px solid #eee', paddingRight: 20 }}>
          <h3>Authority Advisories</h3>

          {mockPosts.map((post) => (
            <div
              key={post.id}
              onClick={() => setSelectedPost(post)}
              style={{
                padding: 12,
                marginBottom: 10,
                cursor: 'pointer',
                borderRadius: 6,
                background:
                  selectedPost.id === post.id ? '#f3f4f6' : 'transparent',
              }}
            >
              <strong>{post.title}</strong>
              <p style={{ fontSize: 12, opacity: 0.6 }}>{post.timestamp}</p>
            </div>
          ))}
        </div>

        {/* RIGHT: Selected Advisory */}
        <div
          style={{
            border: '1px solid #ddd',
            padding: 20,
            borderRadius: 8,
          }}
        >
          <h1>{selectedPost.title}</h1>

          <p style={{ opacity: 0.7 }}>
            Issued by <b>{selectedPost.issued_by}</b> • {selectedPost.timestamp}
          </p>

          <span
            style={{
              padding: '4px 10px',
              borderRadius: 20,
              fontWeight: 600,
              background:
                selectedPost.verdict === 'Fake'
                  ? '#fee2e2'
                  : selectedPost.verdict === 'Verified'
                  ? '#dcfce7'
                  : '#fef3c7',
              color:
                selectedPost.verdict === 'Fake'
                  ? '#b91c1c'
                  : selectedPost.verdict === 'Verified'
                  ? '#166534'
                  : '#92400e',
            }}
          >
            {selectedPost.verdict}
          </span>

          <p style={{ marginTop: 20, lineHeight: 1.6 }}>
            {selectedPost.content}
          </p>
        </div>
      </div>

      {/* Public Discussion */}
      <div style={{ marginTop: 40 }}>
        <h3>Public Discussion</h3>

        <textarea
          rows={3}
          placeholder="Ask a question or share concerns..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: '100%', padding: 10 }}
        />

        <button
          onClick={addComment}
          style={{ marginTop: 10, padding: '8px 16px' }}
        >
          Post Comment
        </button>

        <div style={{ marginTop: 20 }}>
          {comments.length === 0 && (
            <p style={{ opacity: 0.6 }}>No comments yet.</p>
          )}

          {comments.map((c) => (
            <div
              key={c.id}
              style={{
                padding: 10,
                borderBottom: '1px solid #eee',
              }}
            >
              {c.text}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
