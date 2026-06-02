"use client";

import React, { useState } from "react";
import { BookOpen, WifiOff, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function OfflineToolkit() {
  const [activePack, setActivePack] = useState<string | null>(null);

  // Pre-packaged static offline packs (Zero-data learning packs)
  const offlinePacks = [
    {
      id: "interview-basics",
      title: "Core Interview Blueprint (इंटरव्यू बेसिक्स)",
      description: "Learn how to introduce yourself and structure answer blueprints.",
      content: [
        "1. Tell Me About Yourself: Focus on the STAR format (Situation, Task, Action, Result). State your target technical domain in 3 sentences.",
        "2. Answering Technical Gaps: Never say 'I don't know'. Instead say 'I have worked extensively with similar paradigms like X, and I am highly confident in mapping my skills to Y within days.'",
        "3. Local Skilling Resources: Utilize free offline portals, college placement study kits, and open documentation."
      ]
    },
    {
      id: "react-cheat-sheet",
      title: "React.js Quick Primer (रिएक्ट चीट शीट)",
      description: "Quick lookup definitions for common Frontend React interview terms.",
      content: [
        "1. Props vs State: Props are immutable values passed down by parent modules. State is a mutable internal memory tracker owned by the component.",
        "2. Hooks: useState manages local component state variables; useEffect runs side-effects during component rendering phases.",
        "3. Key prop: Unique string indices given to dynamic lists allowing the virtual DOM to target updates efficiently."
      ]
    }
  ];

  return (
    <div className="flex flex-col gap-6">
      <header className="flex items-center gap-3 pb-3 border-b border-border">
        <Link href="/" className="p-1 hover:bg-slate-100 rounded transition">
          <ArrowLeft className="w-4 h-4 text-slate-600" />
        </Link>
        <div>
          <h1 className="text-lg font-bold text-slate-800">Offline Learning Kit</h1>
          <p className="text-[10px] text-slate-500">Access pre-downloaded study packages without internet.</p>
        </div>
      </header>

      {/* Offline Status alert */}
      <div className="flex items-center gap-2.5 p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/20 text-yellow-600 text-xs">
        <WifiOff className="w-4 h-4" />
        <span>You are currently offline. Server APIs are inaccessible, but study kits remain fully active.</span>
      </div>

      {!activePack ? (
        <div className="flex flex-col gap-3">
          {offlinePacks.map((pack) => (
            <div 
              key={pack.id} 
              onClick={() => setActivePack(pack.id)}
              className="p-4 rounded-xl border border-border bg-card hover:border-primary cursor-pointer transition shadow-sm"
            >
              <div className="flex items-center gap-2 mb-1.5 text-slate-700">
                <BookOpen className="w-4 h-4 text-primary" />
                <h3 className="text-xs font-bold">{pack.title}</h3>
              </div>
              <p className="text-[10px] text-slate-500">{pack.description}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-col gap-4 animate-fadeIn">
          {offlinePacks.filter(p => p.id === activePack).map((pack) => (
            <div key={pack.id} className="p-4 rounded-xl border border-border bg-card shadow-sm flex flex-col gap-3">
              <h3 className="text-xs font-bold text-primary pb-2 border-b border-border">
                {pack.title}
              </h3>
              <div className="flex flex-col gap-3">
                {pack.content.map((point, idx) => (
                  <p key={idx} className="text-[10px] text-slate-600 leading-relaxed bg-slate-50 p-2.5 rounded border border-border">
                    {point}
                  </p>
                ))}
              </div>
              <button 
                onClick={() => setActivePack(null)}
                className="mt-2 py-1.5 text-[10px] font-semibold text-slate-500 border border-border rounded hover:bg-slate-50 transition"
              >
                Back to All Kits
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
