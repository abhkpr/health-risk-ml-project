'use client';
import { useState } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:5000';

type RiskResult = {
  risk_level: string;
  risk_code: number;
  confidence: number;
  color: string;
  recommendations: string[];
  probabilities: Record<string, number>;
};

const DEFAULTS = {
  age: 35, gender: 0, bmi: 24.5,
  bp_systolic: 120, bp_diastolic: 80,
  fasting_sugar: 95, hba1c: 5.4,
  total_cholesterol: 185, ldl: 110, hdl: 55,
  heart_rate: 72, smoking: 0, alcohol: 0,
  physical_activity: 4, family_history: 0,
};

const FIELDS = [
  { key: 'age',               label: 'Age',                     unit: 'years', min: 20,  max: 100, step: 1,   type: 'number' },
  { key: 'gender',            label: 'Gender',                  unit: '',      type: 'select', options: [{v:0,l:'Female'},{v:1,l:'Male'}] },
  { key: 'bmi',               label: 'BMI',                     unit: 'kg/m²', min: 15,  max: 50,  step: 0.1, type: 'number' },
  { key: 'bp_systolic',       label: 'Systolic BP',             unit: 'mmHg',  min: 90,  max: 200, step: 1,   type: 'number' },
  { key: 'bp_diastolic',      label: 'Diastolic BP',            unit: 'mmHg',  min: 60,  max: 120, step: 1,   type: 'number' },
  { key: 'fasting_sugar',     label: 'Fasting Blood Sugar',     unit: 'mg/dL', min: 70,  max: 300, step: 1,   type: 'number' },
  { key: 'hba1c',             label: 'HbA1c',                   unit: '%',     min: 4,   max: 14,  step: 0.1, type: 'number' },
  { key: 'total_cholesterol', label: 'Total Cholesterol',       unit: 'mg/dL', min: 130, max: 320, step: 1,   type: 'number' },
  { key: 'ldl',               label: 'LDL Cholesterol',         unit: 'mg/dL', min: 50,  max: 250, step: 1,   type: 'number' },
  { key: 'hdl',               label: 'HDL Cholesterol',         unit: 'mg/dL', min: 20,  max: 100, step: 1,   type: 'number' },
  { key: 'heart_rate',        label: 'Resting Heart Rate',      unit: 'bpm',   min: 40,  max: 120, step: 1,   type: 'number' },
  { key: 'smoking',           label: 'Smoking',                 unit: '',      type: 'select', options: [{v:0,l:'No'},{v:1,l:'Yes'}] },
  { key: 'alcohol',           label: 'Alcohol Consumption',     unit: '',      type: 'select', options: [{v:0,l:'No'},{v:1,l:'Yes'}] },
  { key: 'physical_activity', label: 'Physical Activity',       unit: 'hrs/wk',min: 0,  max: 7,   step: 1,   type: 'number' },
  { key: 'family_history',    label: 'Family History (CVD/DM)', unit: '',      type: 'select', options: [{v:0,l:'No'},{v:1,l:'Yes'}] },
] as const;

const BADGE: Record<number, string> = {
  0: 'bg-green-50 text-green-800 border-green-300',
  1: 'bg-yellow-50 text-yellow-800 border-yellow-300',
  2: 'bg-orange-50 text-orange-800 border-orange-300',
  3: 'bg-red-50 text-red-800 border-red-300',
};
const BAR: Record<string, string> = {
  'Healthy':       'bg-green-500',
  'Low Risk':      'bg-yellow-400',
  'Moderate Risk': 'bg-orange-500',
  'High Risk':     'bg-red-500',
};

export default function Home() {
  const [form, setForm]       = useState<Record<string, number>>(DEFAULTS);
  const [result, setResult]   = useState<RiskResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');

  const set = (k: string, v: string) => setForm(f => ({ ...f, [k]: parseFloat(v) }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError(''); setResult(null);
    try {
      const r = await fetch(`${API}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!r.ok) throw new Error(`Server error ${r.status}`);
      setResult(await r.json());
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Prediction failed. Check backend.');
    } finally { setLoading(false); }
  };

  const sample = (type: 'healthy' | 'high') => {
    setResult(null);
    if (type === 'healthy')
      setForm({ age:28, gender:0, bmi:22.1, bp_systolic:112, bp_diastolic:70, fasting_sugar:88,
        hba1c:5.0, total_cholesterol:162, ldl:88, hdl:68, heart_rate:66, smoking:0, alcohol:0, physical_activity:6, family_history:0 });
    else
      setForm({ age:67, gender:1, bmi:34.2, bp_systolic:165, bp_diastolic:98, fasting_sugar:220,
        hba1c:9.1, total_cholesterol:275, ldl:188, hdl:29, heart_rate:98, smoking:1, alcohol:1, physical_activity:0, family_history:1 });
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <header className="bg-gradient-to-r from-blue-700 to-indigo-700 text-white shadow-lg">
        <div className="max-w-5xl mx-auto px-6 py-5">
          <h1 className="text-2xl font-bold">Smart Health Risk Assessment System</h1>
          <p className="text-blue-200 text-sm mt-0.5">ML-powered chronic disease risk · 7 algorithms · 2000-patient dataset</p>
          <p className="text-blue-300 text-xs mt-0.5">Abhishek Kumar · CSJMA23001390288 · CSJMU Kanpur</p>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-8 grid lg:grid-cols-2 gap-8">
        {/* ── Form ── */}
        <section className="bg-white rounded-2xl shadow-md p-6">
          <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
            <h2 className="text-lg font-semibold text-gray-800">Patient Information</h2>
            <div className="flex gap-2 text-xs">
              <button type="button" onClick={() => sample('healthy')}
                className="px-3 py-1 bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition">
                Healthy Sample
              </button>
              <button type="button" onClick={() => sample('high')}
                className="px-3 py-1 bg-red-100 text-red-700 rounded-full hover:bg-red-200 transition">
                High-Risk Sample
              </button>
            </div>
          </div>

          <form onSubmit={submit} className="space-y-2.5">
            {FIELDS.map(f => (
              <div key={f.key} className="flex items-center gap-3">
                <label className="w-48 text-xs font-medium text-gray-600 flex-shrink-0">
                  {f.label}
                  {'unit' in f && f.unit && <span className="text-gray-400 ml-1">({f.unit})</span>}
                </label>
                {f.type === 'select' ? (
                  <select value={form[f.key]}
                    onChange={e => set(f.key, e.target.value)}
                    className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-300 focus:outline-none bg-gray-50">
                    {f.options.map(o => <option key={o.v} value={o.v}>{o.l}</option>)}
                  </select>
                ) : (
                  <input type="number"
                    min={f.min} max={f.max} step={f.step}
                    value={form[f.key]}
                    onChange={e => set(f.key, e.target.value)}
                    className="flex-1 border border-gray-200 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-300 focus:outline-none bg-gray-50"
                    required />
                )}
              </div>
            ))}

            <button type="submit" disabled={loading}
              className="w-full mt-3 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 transition disabled:opacity-60 shadow">
              {loading
                ? <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                    </svg>
                    Analysing…
                  </span>
                : 'Predict Health Risk'}
            </button>
          </form>
        </section>

        {/* ── Results ── */}
        <section className="space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 text-sm">{error}</div>
          )}

          {!result && !error && !loading && (
            <div className="bg-white rounded-2xl shadow-md p-8 flex flex-col items-center justify-center text-center text-gray-400 min-h-[300px]">
              <svg className="w-14 h-14 mb-3 opacity-25" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              <p className="font-medium">Fill in patient details</p>
              <p className="text-sm mt-1">or load a sample, then click Predict</p>
            </div>
          )}

          {loading && (
            <div className="bg-white rounded-2xl shadow-md p-8 flex items-center justify-center min-h-[300px]">
              <div className="text-center">
                <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3"/>
                <p className="text-gray-500 text-sm">Running 7 ML algorithms…</p>
              </div>
            </div>
          )}

          {result && (
            <>
              <div className={`rounded-2xl shadow-md p-6 border-2 ${BADGE[result.risk_code]}`}>
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wider opacity-70">Risk Level</p>
                    <p className="text-3xl font-bold mt-1">{result.risk_level}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-semibold uppercase tracking-wider opacity-70">Confidence</p>
                    <p className="text-3xl font-bold mt-1">{result.confidence}%</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-md p-5">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">Class Probabilities</h3>
                {Object.entries(result.probabilities).map(([cls, pct]) => (
                  <div key={cls} className="mb-2">
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>{cls}</span><span>{pct}%</span>
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full transition-all duration-500 ${BAR[cls] ?? 'bg-gray-400'}`}
                        style={{ width: `${pct}%` }}/>
                    </div>
                  </div>
                ))}
              </div>

              <div className="bg-white rounded-2xl shadow-md p-5">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">Personalised Recommendations</h3>
                <ul className="space-y-2">
                  {result.recommendations.map((r, i) => (
                    <li key={i} className="flex gap-2 text-sm text-gray-700">
                      <span className="mt-0.5 flex-shrink-0 text-blue-500">•</span>{r}
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </section>
      </div>

      <footer className="text-center text-xs text-gray-400 pb-6">
        Smart Health Risk Assessment · Random Forest (95.5% acc) · 7 algorithms · CSJMU Kanpur
      </footer>
    </main>
  );
}
