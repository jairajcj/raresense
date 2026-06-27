import { useState } from 'react'
import { api } from '../utils/api'
import { BrainCircuit, Play, Sparkles, Dna, FileText, Pill, FlaskConical, AlertTriangle } from 'lucide-react'

const SAMPLE_NOTES = [
  {
    title: "Lupus Case Study (Review 1)",
    text: `28F presents with erythematous malar rash across both cheeks. Reports photosensitivity for the past 3 months. Platelet count 89,000/uL. Urinalysis shows proteinuria (2+). eGFR mildly reduced at 72. Patient reports persistent fatigue and arthralgia in bilateral hands and knees. Oral ulcers noted on examination.`
  },
  {
    title: "Suspected Scleroderma",
    text: `45F presents with progressive skin tightening of fingers and face over 6 months. Raynaud phenomenon with digital color changes. Reports dyspnea on exertion. Pulmonary function tests show reduced DLCO. CXR shows early pulmonary fibrosis. Dysphagia for solid foods. Telangiectasia noted on face and chest.`
  },
  {
    title: "Metabolic Storage Disease",
    text: `12M presents with hepatomegaly and splenomegaly detected on routine examination. Blood work shows anemia with hemoglobin 9.2 g/dL. Thrombocytopenia with platelet count 95,000/uL. Reports chronic fatigue and bone pain. Arthralgia in bilateral hips. Growth retardation noted - below 5th percentile for age.`
  },
  {
    title: "Neurological Presentation",
    text: `55M with progressive cognitive decline over 18 months. Family reports personality changes and irritability. Tremor of bilateral hands noted. Muscle weakness in proximal limbs. Difficulty with dysphagia for liquids. Unintentional weight loss of 8kg. Gait ataxia on examination.`
  },
]

export default function AIAssistant() {
  const [text, setText] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)

  async function handleAnalyze() {
    if (!text.trim()) return
    setAnalyzing(true)
    setResult(null)
    try {
      const data = await api.analyzeNote(text)
      setResult(data)
    } catch (err) {
      alert(err.message)
    } finally {
      setAnalyzing(false)
    }
  }

  function loadSample(sample) {
    setText(sample.text)
    setResult(null)
  }

  const entityIcons = {
    symptom: <Sparkles size={12} />,
    medication: <Pill size={12} />,
    diagnosis: <AlertTriangle size={12} />,
    lab_value: <FlaskConical size={12} />,
  }

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h1>AI Diagnostic Assistant</h1>
          <p>Paste a clinical note to extract symptoms and match against rare diseases</p>
        </div>
      </div>

      {/* Sample Notes */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', padding: '0.4rem 0', fontWeight: 600 }}>Try a sample:</span>
        {SAMPLE_NOTES.map((s, i) => (
          <button key={i} className="btn btn-secondary btn-sm" onClick={() => loadSample(s)}>
            {s.title}
          </button>
        ))}
      </div>

      {/* Input Area */}
      <div className="ai-input-area">
        <textarea
          placeholder="Paste or type a clinical note here...&#10;&#10;Example: 28F presents with erythematous malar rash across both cheeks. Reports photosensitivity. Platelet count 89,000/uL..."
          value={text}
          onChange={e => setText(e.target.value)}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.75rem' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {text.length} characters · The NLP engine extracts symptoms, medications, diagnoses, and lab values
          </span>
          <button className="btn btn-primary" onClick={handleAnalyze} disabled={analyzing || !text.trim()}>
            {analyzing ? (
              <><span className="loading-dots"><span></span><span></span><span></span></span> Analyzing...</>
            ) : (
              <><BrainCircuit size={16} /> Analyze & Match</>
            )}
          </button>
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="ai-results slide-up">
          {/* Left: Extracted Entities */}
          <div>
            <div className="card" style={{ marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Sparkles size={18} color="var(--accent-light)" /> NLP Extraction Results
              </h3>

              {/* Summary */}
              <div className="stat-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: '1rem', gap: '0.5rem' }}>
                <div style={{ padding: '0.6rem', background: 'var(--symptom-bg)', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--symptom)' }}>{result.entities?.filter(e => e.entity_type === 'symptom').length || 0}</div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)' }}>Symptoms</div>
                </div>
                <div style={{ padding: '0.6rem', background: 'var(--medication-bg)', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--medication)' }}>{result.entities?.filter(e => e.entity_type === 'medication').length || 0}</div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)' }}>Medications</div>
                </div>
                <div style={{ padding: '0.6rem', background: 'var(--diagnosis-bg)', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--diagnosis)' }}>{result.entities?.filter(e => e.entity_type === 'diagnosis').length || 0}</div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)' }}>Diagnoses</div>
                </div>
                <div style={{ padding: '0.6rem', background: 'var(--lab-bg)', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--lab)' }}>{result.entities?.filter(e => e.entity_type === 'lab_value').length || 0}</div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)' }}>Lab Values</div>
                </div>
              </div>

              {/* Entity List */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                {result.entities?.map((e, i) => (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '0.5rem 0.75rem', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span className={`entity-tag ${e.entity_type}`} style={{ margin: 0 }}>
                        {entityIcons[e.entity_type]} {e.normalized_name}
                      </span>
                      {e.hpo_code && <code style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{e.hpo_code}</code>}
                    </div>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                      {Math.round(e.confidence * 100)}%
                    </span>
                  </div>
                ))}
              </div>

              {result.hpo_codes?.length > 0 && (
                <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
                    Patient Phenotype ({result.hpo_codes.length} HPO codes)
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
                    {result.hpo_codes.map((code, i) => (
                      <code key={i} style={{ fontSize: '0.65rem', color: 'var(--accent-light)', background: 'var(--accent-glow)', padding: '0.15rem 0.4rem', borderRadius: '3px' }}>
                        {code}
                      </code>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right: Disease Matches */}
          <div>
            <div className="card">
              <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Dna size={18} color="var(--accent-light)" /> Disease Matches
              </h3>

              {result.matches?.length > 0 ? result.matches.map((match, i) => {
                const confPct = Math.round(match.confidence * 100)
                const level = confPct >= 60 ? 'high' : confPct >= 30 ? 'medium' : 'low'
                return (
                  <div key={i} className={`match-card ${level}`} style={{ marginBottom: '0.75rem' }}>
                    <div className="match-header">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flex: 1 }}>
                        <div className="match-rank">{match.rank}</div>
                        <div>
                          <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-primary)' }}>{match.disease_name}</h4>
                          <code style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{match.disease_orpha_id}</code>
                        </div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '1.35rem', fontWeight: 800, color: level === 'high' ? 'var(--success)' : level === 'medium' ? 'var(--warning)' : 'var(--text-tertiary)' }}>
                          {confPct}%
                        </div>
                      </div>
                    </div>
                    <div className="confidence-bar">
                      <div className={`confidence-fill ${level}`} style={{ width: `${confPct}%` }} />
                    </div>
                    <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                      {match.matched_count}/{match.total_disease_symptoms} symptoms matched
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.2rem', marginTop: '0.35rem' }}>
                      {match.matched_symptoms?.map((s, j) => (
                        <span key={j} className="entity-tag symptom" style={{ fontSize: '0.65rem', padding: '0.15rem 0.45rem' }}>
                          {s.symptom_name}
                        </span>
                      ))}
                    </div>
                  </div>
                )
              }) : (
                <div className="empty-state" style={{ padding: '2rem' }}>
                  <Dna size={32} />
                  <p>No matches found. The note may not contain recognizable symptoms.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* How it works */}
      {!result && (
        <div className="card" style={{ marginTop: '1rem' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '1rem' }}>How It Works</h3>
          <div className="grid-3" style={{ gap: '1rem' }}>
            <div style={{ padding: '1.25rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
              <FileText size={32} color="var(--accent-light)" style={{ marginBottom: '0.75rem' }} />
              <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.35rem' }}>1. Input Clinical Notes</h4>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Paste raw clinical notes from any specialty — discharge summaries, progress notes, consultations</p>
            </div>
            <div style={{ padding: '1.25rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
              <BrainCircuit size={32} color="var(--symptom)" style={{ marginBottom: '0.75rem' }} />
              <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.35rem' }}>2. NLP Extraction</h4>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Clinical NLP engine extracts symptoms, medications, diagnoses, and lab values with HPO code mapping</p>
            </div>
            <div style={{ padding: '1.25rem', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
              <Dna size={32} color="var(--success)" style={{ marginBottom: '0.75rem' }} />
              <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.35rem' }}>3. Disease Matching</h4>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Cosine similarity matching against 25+ rare disease profiles from Orphanet/HPO database</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
