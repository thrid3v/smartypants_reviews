"""
Tab 2 — Live Attack Simulator UI component.
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from smartypants_reviews.gates.nlp_gate import run_nlp_gate
from smartypants_reviews.gates.velocity_gate import run_velocity_gate
from smartypants_reviews.gates.duplication_gate import run_duplication_gate
from smartypants_reviews.mock_data import (
    generate_authentic_stream,
    generate_astroturf_bot_stream,
    generate_hater_mob_stream,
)
from smartypants_reviews.pipeline import process_review


def render_simulator_tab():
    """Render the live attack simulator tab."""
    st.markdown('<div class="section-header">Three-Stream Attack Simulation</div>', unsafe_allow_html=True)

    # ── Stream selection cards ──
    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown("""
        <div class="gate-card">
            <div class="stream-label authentic">● Authentic Stream</div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">
                15 varied reviews · Ratings 4-8 · Staggered timestamps (3-15s apart)
            </div>
        </div>
        """, unsafe_allow_html=True)
        use_authentic = st.checkbox("Include Authentic", value=True, key="chk_authentic")
    with info_cols[1]:
        st.markdown("""
        <div class="gate-card">
            <div class="stream-label hater">● Hater Mob Stream</div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">
                500 reviews · 1-star · Toxic copy-paste · Identical timestamps
            </div>
        </div>
        """, unsafe_allow_html=True)
        use_haters = st.checkbox("Include Hater Mob", value=True, key="chk_haters")
    with info_cols[2]:
        st.markdown("""
        <div class="gate-card">
            <div class="stream-label astroturf">● Astroturf Bot Stream</div>
            <div style="font-family: 'Inter', sans-serif; font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5;">
                500 reviews · 10-star · Generic promo · Identical timestamps
            </div>
        </div>
        """, unsafe_allow_html=True)
        use_bots = st.checkbox("Include Astroturf Bots", value=True, key="chk_bots")

    st.markdown("")

    # ── Target movie input ──
    target_movie = st.text_input(
        "Target Movie for Attack Streams",
        value="The Latest Blockbuster",
        placeholder="Enter the movie to simulate attacks against...",
        key="sim_target_movie",
    )

    # ── Control buttons ──
    btn_cols = st.columns([1, 1, 1, 2])
    with btn_cols[0]:
        simulate_btn = st.button("⚡ SIMULATE LIVE ATTACK", type="primary", use_container_width=True)
    with btn_cols[1]:
        reset_btn = st.button("🗑️ RESET DATABASES", use_container_width=True)
    with btn_cols[2]:
        def _stop_sim():
            st.session_state.sim_running = False
        stop_btn = st.button(  # noqa: F841
            "⏹ STOP SIMULATION", on_click=_stop_sim, use_container_width=True,
        )

    if reset_btn:
        st.session_state.verified_db = pd.DataFrame(
            columns=["timestamp", "movie", "review", "rating", "confidence", "reason", "source"]
        )
        st.session_state.quarantine_db = pd.DataFrame(
            columns=["timestamp", "movie", "review", "rating", "confidence", "reason", "gate_failed", "source"]
        )
        st.rerun()

    # ── Metric Placeholders ──
    st.markdown("")
    metric_cols = st.columns(2)
    with metric_cols[0]:
        verified_metric = st.empty()
    with metric_cols[1]:
        quarantine_metric = st.empty()

    # ── Progress & Log ──
    progress_bar = st.empty()
    log_container = st.empty()

    # ── Database display placeholders ──
    st.markdown('<div class="section-header">Database State</div>', unsafe_allow_html=True)
    db_cols = st.columns(2)
    with db_cols[0]:
        st.markdown("""
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--neon-green); margin-bottom: 0.5rem;">
            ✅ VERIFIED_DB
        </div>
        """, unsafe_allow_html=True)
        verified_table = st.empty()
    with db_cols[1]:
        st.markdown("""
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--neon-red); margin-bottom: 0.5rem;">
            🚫 QUARANTINE_DB
        </div>
        """, unsafe_allow_html=True)
        quarantine_table = st.empty()

    def render_metrics(v_count, q_count, v_delta=0, q_delta=0):
        """Render the live metric cards."""
        v_delta_html = f'<div class="metric-delta" style="color: var(--neon-green);">▲ +{v_delta}</div>' if v_delta else ""
        q_delta_html = f'<div class="metric-delta" style="color: var(--neon-red);">▲ +{q_delta}</div>' if q_delta else ""

        verified_metric.markdown(f"""
        <div class="metric-card verified">
            <div class="metric-label" style="color: var(--neon-green);">Verified Reviews</div>
            <div class="metric-value" style="color: var(--neon-green);">{v_count:,}</div>
            {v_delta_html}
        </div>
        """, unsafe_allow_html=True)

        quarantine_metric.markdown(f"""
        <div class="metric-card quarantined">
            <div class="metric-label" style="color: var(--neon-red);">Quarantined Threats</div>
            <div class="metric-value" style="color: var(--neon-red);">{q_count:,}</div>
            {q_delta_html}
        </div>
        """, unsafe_allow_html=True)

    def render_tables():
        """Render the database tables."""
        if len(st.session_state.verified_db) > 0:
            verified_table.dataframe(
                st.session_state.verified_db,
                use_container_width=True,
                height=300,
            )
        else:
            verified_table.info("No verified reviews yet.")

        if len(st.session_state.quarantine_db) > 0:
            quarantine_table.dataframe(
                st.session_state.quarantine_db,
                use_container_width=True,
                height=300,
            )
        else:
            quarantine_table.info("No quarantined reviews yet.")

    # ── Initial render ──
    render_metrics(len(st.session_state.verified_db), len(st.session_state.quarantine_db))
    render_tables()

    # ── Simulation Logic ──
    if simulate_btn:
        if not use_authentic and not use_haters and not use_bots:
            st.warning("⚠️ Select at least one stream to simulate.")
            return

        st.session_state.sim_running = True

        # Generate only selected streams
        all_reviews = []
        if use_authentic:
            all_reviews += generate_authentic_stream(15)
        if use_haters:
            all_reviews += generate_hater_mob_stream(500, target_movie=target_movie)
        if use_bots:
            all_reviews += generate_astroturf_bot_stream(500, target_movie=target_movie)

        all_timestamps = [r["timestamp"] for r in all_reviews]

        total = len(all_reviews)

        # ── Gate 2: Velocity Check on entire batch ──
        log_container.markdown(f"""
        <div class="log-line"><span class="ts">[GATE 2]</span> <span class="warn">Running Isolation Forest on {total:,} timestamps...</span></div>
        """, unsafe_allow_html=True)

        velocity_labels = run_velocity_gate(all_timestamps)

        verified_count = len(st.session_state.verified_db)
        quarantine_count = len(st.session_state.quarantine_db)
        log_lines = []

        for idx, (review_data, vel_flag) in enumerate(zip(all_reviews, velocity_labels)):
            progress = (idx + 1) / total
            progress_bar.progress(progress, text=f"Processing review {idx + 1:,}/{total:,}")

            source = review_data["source"]
            movie = review_data["movie"]
            text = review_data["review"]
            rating = review_data["rating"]
            ts_str = datetime.fromtimestamp(review_data["timestamp"]).strftime("%H:%M:%S.%f")[:-3]

            # If velocity already flagged it, skip the expensive NLP call
            if vel_flag == -1:
                nlp_result = {
                    "status": "Quarantined",
                    "confidence_score": 0,
                    "reason": "Skipped — velocity anomaly detected (Gate 2 override)",
                }
                dup_result = run_duplication_gate(movie, text)
                result = process_review(movie, text, rating, nlp_result, vel_flag, duplication_result=dup_result, source=source, ts=ts_str)
                quarantine_count = len(st.session_state.quarantine_db)

                if len(log_lines) < 30 or idx % 100 == 0:
                    gate_info = "Gate 2 velocity override"
                    if not dup_result["passed"]:
                        gate_info += f" + Gate 3 dup ({dup_result['count']}×)"
                    log_lines.append(
                        f'<div class="log-line"><span class="ts">[{ts_str}]</span> '
                        f'<span class="fail">▪ QUARANTINED</span> '
                        f'<span style="color:var(--text-muted)">({source}) {gate_info}</span></div>'
                    )
            else:
                # Run NLP gate for reviews that passed velocity
                nlp_result = run_nlp_gate(movie, text)
                dup_result = run_duplication_gate(movie, text)
                result = process_review(movie, text, rating, nlp_result, vel_flag, duplication_result=dup_result, source=source, ts=ts_str)

                dup_note = ""
                if not dup_result["passed"]:
                    dup_note = f" [DUP:{dup_result['count']}×]"

                if result == "Verified":
                    verified_count = len(st.session_state.verified_db)
                    log_lines.append(
                        f'<div class="log-line"><span class="ts">[{ts_str}]</span> '
                        f'<span class="ok">▪ VERIFIED</span> '
                        f'<span style="color:var(--text-muted)">({source}) {nlp_result.get("reason", "")[:60]}</span></div>'
                    )
                else:
                    quarantine_count = len(st.session_state.quarantine_db)
                    log_lines.append(
                        f'<div class="log-line"><span class="ts">[{ts_str}]</span> '
                        f'<span class="fail">▪ QUARANTINED</span> '
                        f'<span style="color:var(--text-muted)">({source}) {nlp_result.get("reason", "")[:50]}{dup_note}</span></div>'
                    )

            # Live update metrics & tables every 50 reviews or on authentic reviews
            if source == "authentic" or idx % 50 == 0 or idx == total - 1:
                v_delta = len(st.session_state.verified_db) - (verified_count - len(st.session_state.verified_db))
                render_metrics(
                    len(st.session_state.verified_db),
                    len(st.session_state.quarantine_db),
                    v_delta=1 if source == "authentic" and result == "Verified" else 0,
                    q_delta=50 if source != "authentic" else 0,
                )
                log_container.markdown("".join(log_lines[-20:]), unsafe_allow_html=True)

            # Refresh tables every 10 reviews for real-time data visibility
            if idx % 10 == 0 or idx == total - 1:
                render_tables()

            # Check for stop request
            if not st.session_state.sim_running:
                progress_bar.progress((idx + 1) / total, text=f"⏹ Simulation stopped at review {idx + 1:,}/{total:,}")
                break

        # ── Final render ──
        progress_bar.progress(1.0, text="✅ Simulation complete!")
        render_metrics(
            len(st.session_state.verified_db),
            len(st.session_state.quarantine_db),
        )
        render_tables()

        st.session_state.sim_running = False

        st.markdown(f"""
        <div class="gate-card" style="border-color: rgba(0, 212, 255, 0.3); margin-top: 1rem;">
            <div style="font-family: 'JetBrains Mono', monospace; color: var(--neon-blue); font-size: 0.85rem; margin-bottom: 0.8rem;">
                ▸ SIMULATION SUMMARY
            </div>
            <div style="font-family: 'Inter', sans-serif; color: var(--text-secondary); font-size: 0.9rem; line-height: 1.8;">
                <strong style="color: var(--neon-green);">{len(st.session_state.verified_db):,}</strong> reviews verified &nbsp;│&nbsp;
                <strong style="color: var(--neon-red);">{len(st.session_state.quarantine_db):,}</strong> threats quarantined &nbsp;│&nbsp;
                <strong style="color: var(--neon-blue);">{total:,}</strong> total processed
            </div>
        </div>
        """, unsafe_allow_html=True)
