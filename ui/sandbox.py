"""
Tab 1 — Manual Sandbox UI component.
"""

import streamlit as st

from smartypants_reviews.gates.nlp_gate import run_nlp_gate
from smartypants_reviews.gates.duplication_gate import run_duplication_gate
from smartypants_reviews.pipeline import process_review


def render_sandbox_tab():
    """Render the manual review evaluator tab."""
    st.markdown('<div class="section-header">Single Review Evaluator</div>', unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("""
        <div class="gate-card">
            <div style="font-family: 'JetBrains Mono', monospace; color: var(--neon-blue); font-size: 0.85rem; margin-bottom: 1rem;">
                ▸ INPUT REVIEW FOR ANALYSIS
            </div>
        </div>
        """, unsafe_allow_html=True)

        movie_title = st.text_input(
            "Movie Title",
            placeholder="e.g. The Dark Knight, Oppenheimer, Barbie...",
            key="sandbox_movie",
        )
        review_text = st.text_area(
            "Review Text",
            placeholder="Enter the review to evaluate...",
            height=150,
            key="sandbox_review",
        )

        submit_btn = st.button("⚡ SUBMIT FOR ANALYSIS", type="primary", use_container_width=True)

    with col_result:
        st.markdown("""
        <div class="gate-card">
            <div style="font-family: 'JetBrains Mono', monospace; color: var(--neon-purple); font-size: 0.85rem; margin-bottom: 1rem;">
                ▸ GATE 1 — NLP ANALYSIS RESULT
            </div>
        </div>
        """, unsafe_allow_html=True)

        if submit_btn:
            if not movie_title or not review_text:
                st.warning("⚠️ Please enter both a movie title and review text.")
            else:
                with st.spinner("🔄 Querying Llama 3 via Ollama..."):
                    result = run_nlp_gate(movie_title, review_text)

                if result["status"] == "Error":
                    st.error(f"**Connection Error:** {result['reason']}")
                else:
                    # ── Gate 1 result ──
                    if result["status"] == "Verified":
                        st.markdown(f"""
                        <div class="result-verified">
                            <div class="result-header">✅ GATE 1 — AUTHENTIC CONTENT</div>
                            <div class="result-score" style="color: var(--neon-green);">{result['confidence_score']}%</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 1px;">CONFIDENCE SCORE</div>
                            <div class="result-reason">{result['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-quarantined">
                            <div class="result-header">🚫 GATE 1 — SUSPICIOUS CONTENT</div>
                            <div class="result-score" style="color: var(--neon-red);">{result['confidence_score']}%</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 1px;">CONFIDENCE SCORE</div>
                            <div class="result-reason">{result['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # ── Gate 3: Duplication check ──
                    dup_result = run_duplication_gate(movie_title, review_text)
                    if not dup_result["passed"]:
                        st.markdown(f"""
                        <div class="result-quarantined">
                            <div class="result-header">🔁 GATE 3 — DUPLICATE CONTENT DETECTED</div>
                            <div class="result-score" style="color: var(--neon-red);">{dup_result['count']}×</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 1px;">TIMES SEEN</div>
                            <div class="result-reason">{dup_result['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-verified">
                            <div class="result-header">✅ GATE 3 — UNIQUE CONTENT</div>
                            <div class="result-score" style="color: var(--neon-green);">{dup_result['count']}</div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 1px;">PRIOR OCCURRENCES</div>
                            <div class="result-reason">{dup_result['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # ── Final verdict ──
                    rating = 7 if result["status"] == "Verified" else 1
                    verdict = process_review(
                        movie_title, review_text, rating, result, 1,
                        duplication_result=dup_result, source="sandbox",
                    )
                    if verdict == "Verified":
                        st.markdown(f"""
                        <div class="result-verified" style="margin-top: 0.5rem;">
                            <div class="result-header">🛡️ FINAL VERDICT — VERIFIED</div>
                            <div class="result-reason">Passed all gates. Routed to Verified_DB.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-quarantined" style="margin-top: 0.5rem;">
                            <div class="result-header">🚫 FINAL VERDICT — QUARANTINED</div>
                            <div class="result-reason">Failed one or more gates. Routed to Quarantine_DB.</div>
                        </div>
                        """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 3rem 1rem;
                color: var(--text-muted);
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.85rem;
            ">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🛡️</div>
                <div>Awaiting review submission...</div>
                <div style="font-size: 0.7rem; margin-top: 0.5rem; color: var(--text-muted);">
                    Enter a movie title and review to activate Gate 1 analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
