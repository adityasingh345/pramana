'use client'

import { useState } from 'react'
import Link from 'next/link'

interface Complaint {
  id: number
  name: string
  category: string
  description: string
  status: 'Submitted' | 'Under Review' | 'Resolved'
  date: string
}

export default function ComplaintPage() {
  const [complaints, setComplaints] = useState<Complaint[]>([
    {
      id: 1,
      name: 'Anonymous User',
      category: 'Fake News',
      description: 'False news about celebrity death circulating on WhatsApp.',
      status: 'Under Review',
      date: '30 Jan 2026',
    },
    {
      id: 2,
      name: 'Rahul Sharma',
      category: 'Deepfake',
      description: 'AI-generated video of a political leader spreading misinformation.',
      status: 'Submitted',
      date: '29 Jan 2026',
    },
  ])

  const [form, setForm] = useState({
    name: '',
    category: '',
    description: '',
  })

  const handleSubmit = () => {
    if (!form.description || !form.category) return alert('Fill all required fields')

    const newComplaint: Complaint = {
      id: Date.now(),
      name: form.name || 'Anonymous',
      category: form.category,
      description: form.description,
      status: 'Submitted',
      date: new Date().toLocaleDateString(),
    }

    setComplaints([newComplaint, ...complaints])
    setForm({ name: '', category: '', description: '' })
  }

  return (
    <div style={{ maxWidth: 900, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <Link href="/" style={{ textDecoration: 'none' }}>← Back to Home</Link>

      <h1 style={{ marginTop: 20 }}>📝 File a Complaint</h1>
      <p style={{ opacity: 0.7 }}>
        Report misinformation, deepfakes, or harmful digital content.
      </p>

      {/* Complaint Form */}
      <div
        style={{
          border: '1px solid #ddd',
          padding: 20,
          borderRadius: 8,
          marginTop: 20,
        }}
      >
        <input
          placeholder="Your Name (optional)"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          style={{ width: '100%', padding: 10, marginBottom: 10 }}
        />

        <select
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
          style={{ width: '100%', padding: 10, marginBottom: 10 }}
        >
          <option value="">Select Complaint Type *</option>
          <option value="Fake News">Fake News</option>
          <option value="Deepfake">Deepfake</option>
          <option value="Scam">Scam / Fraud</option>
          <option value="Impersonation">Impersonation</option>
        </select>

        <textarea
          rows={4}
          placeholder="Describe the issue *"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          style={{ width: '100%', padding: 10 }}
        />

        <button
          onClick={handleSubmit}
          style={{
            marginTop: 10,
            padding: '10px 16px',
            background: '#111',
            color: '#fff',
            borderRadius: 6,
          }}
        >
          Submit Complaint
        </button>
      </div>

      {/* Complaints List */}
      <h2 style={{ marginTop: 40 }}>📂 Submitted Complaints</h2>

      {complaints.length === 0 && <p>No complaints yet.</p>}

      {complaints.map((c) => (
        <div
          key={c.id}
          style={{
            border: '1px solid #eee',
            padding: 15,
            borderRadius: 6,
            marginTop: 12,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong>{c.category}</strong>
            <span
              style={{
                padding: '4px 10px',
                borderRadius: 20,
                background:
                  c.status === 'Resolved'
                    ? '#dcfce7'
                    : c.status === 'Under Review'
                    ? '#fef3c7'
                    : '#e0e7ff',
              }}
            >
              {c.status}
            </span>
          </div>

          <p style={{ marginTop: 8 }}>{c.description}</p>

          <p style={{ fontSize: 12, opacity: 0.6 }}>
            Reported by {c.name} • {c.date}
          </p>
        </div>
      ))}
    </div>
  )
}
