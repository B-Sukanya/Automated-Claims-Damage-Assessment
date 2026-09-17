from __future__ import annotations

import json
from datetime import date
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw


st.set_page_config(
    page_title="ClaimLens | Damage Assessment",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] { background: #f6f8fb; }
        [data-testid="stHeader"] { background: rgba(246,248,251,.9); }
        .hero {
            padding: 1.5rem 1.7rem; border-radius: 18px;
            background: linear-gradient(120deg, #102a43 0%, #176b87 100%);
            color: white; margin-bottom: 1.2rem;
        }
        .hero h1 { margin: 0; font-size: 2.15rem; letter-spacing: -.04em; }
        .hero p { margin: .45rem 0 0; color: #d7f2f4; font-size: 1rem; }
        .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .72rem;
            font-weight: 700; color: #74d4d9; }
        .workflow {
            display: flex; gap: .55rem; align-items: center; flex-wrap: wrap;
            margin: .25rem 0 1.25rem; color: #64748b; font-size: .78rem;
        }
        .workflow-step { background: white; border: 1px solid #dbe5ed; border-radius: 999px;
            padding: .42rem .72rem; font-weight: 650; }
        .workflow-step.active { background: #e5f5f5; border-color: #a8d8d9; color: #0d6872; }
        .workflow-arrow { color: #a2afbd; }
        .sidebar-brand { padding: .2rem 0 .8rem; }
        .sidebar-brand strong { color: #102a43; font-size: 1.22rem; }
        .sidebar-brand small { display: block; color: #738195; margin-top: .15rem; }
        .section-kicker { color: #0d6872; text-transform: uppercase; letter-spacing: .1em;
            font-size: .68rem; font-weight: 750; margin-bottom: .15rem; }
        .section-subtitle { color: #738195; font-size: .82rem; margin: 0 0 .8rem; }
        .metric-card {
            background: white; border: 1px solid #e3eaf1; border-radius: 14px;
            padding: 1rem 1.05rem; min-height: 105px;
        }
        .metric-label { color: #64748b; font-size: .78rem; font-weight: 600; }
        .metric-value { color: #102a43; font-size: 1.55rem; font-weight: 750; margin-top: .25rem; }
        .metric-note { color: #738195; font-size: .75rem; margin-top: .2rem; }
        .section-title { color: #102a43; font-size: 1.12rem; font-weight: 750; margin: .7rem 0 .55rem; }
        .finding {
            background: white; border: 1px solid #e3eaf1; border-left: 5px solid #f0a35b;
            border-radius: 10px; padding: .8rem .95rem; margin: .55rem 0;
        }
        .finding strong { color: #102a43; }
        .finding small { color: #64748b; }
        .status-pill { display: inline-block; padding: .25rem .6rem; border-radius: 999px;
            background: #fff4e5; color: #9a5a00; font-size: .76rem; font-weight: 700; }
        .action-card { background: #102a43; color: white; border-radius: 14px; padding: 1rem 1.1rem; }
        .action-card strong { color: #74d4d9; font-size: .72rem; letter-spacing: .1em; }
        .action-card p { margin: .55rem 0 0; color: #e7f1f5; font-size: .88rem; line-height: 1.45; }
        div[data-testid="stFileUploaderDropzone"] { border-color: #a8cfd5; background: #fbfefe; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sample_image() -> Image.Image:
    image = Image.new("RGB", (1200, 720), "#d9e2e8")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1200, 410), fill="#9fc5d1")
    draw.rectangle((0, 410, 1200, 720), fill="#63717a")
    draw.polygon([(155, 475), (275, 330), (810, 330), (1040, 475)], fill="#f4f6f7")
    draw.polygon([(190, 460), (300, 350), (485, 350), (485, 460)], fill="#31566b")
    draw.polygon([(510, 350), (785, 350), (920, 460), (510, 460)], fill="#31566b")
    draw.rectangle((165, 455, 1018, 515), fill="#f1f3f4")
    draw.ellipse((235, 440, 390, 595), fill="#1d2830", outline="#c4d0d5", width=8)
    draw.ellipse((790, 440, 945, 595), fill="#1d2830", outline="#c4d0d5", width=8)
    draw.polygon([(750, 460), (1015, 463), (1010, 515), (780, 510)], fill="#df795b")
    draw.line((805, 470, 950, 492), fill="#9e382c", width=8)
    draw.line((840, 490, 975, 475), fill="#9e382c", width=5)
    return image


def assess_image(image: Image.Image, file_name: str, vehicle_type: str) -> dict[str, Any]:
    rgb = image.convert("RGB").resize((160, 160))
    pixels = np.asarray(rgb).astype(float)
    brightness = pixels.mean() / 255
    contrast = pixels.std() / 128
    # This is intentionally a transparent, deterministic POC heuristic.
    visual_signal = min(1.0, 0.45 + contrast * 0.22 + (1 - brightness) * 0.15)
    severity = "Moderate" if visual_signal < 0.72 else "High"
    confidence = round(min(96, 78 + visual_signal * 14), 1)
    return {
        "file_name": file_name,
        "vehicle_type": vehicle_type,
        "severity": severity,
        "confidence": confidence,
        "findings": [
            {"part": "Rear bumper", "damage": "Impact deformation and visible paint transfer", "severity": severity, "cost": 720},
            {"part": "Right rear quarter panel", "damage": "Surface denting with multiple scratches", "severity": "Moderate", "cost": 540},
            {"part": "Tail lamp assembly", "damage": "No obvious fracture detected", "severity": "Low", "cost": 180},
        ],
    }


def render_metric(label: str, value: str, note: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_styles()
    st.markdown(
        '<div class="hero"><div class="eyebrow">ClaimLens / Computer Vision POC</div>'
        "<h1>Automated claims damage assessment</h1>"
        "<p>Turn incident photos into a consistent first-pass estimate for faster claim triage.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="workflow"><span class="workflow-step active">1&nbsp; Claim intake</span>'
        '<span class="workflow-arrow">→</span><span class="workflow-step active">2&nbsp; Photo analysis</span>'
        '<span class="workflow-arrow">→</span><span class="workflow-step">3&nbsp; Handler review</span>'
        '<span class="workflow-arrow">→</span><span class="workflow-step">4&nbsp; Settlement decision</span></div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand"><strong>ClaimLens</strong>'
            '<small>Claims intelligence workspace</small></div>',
            unsafe_allow_html=True,
        )
        st.markdown("### Claim intake")
        st.caption("Capture the incident context before reviewing visual evidence.")
        use_sample = st.toggle("Use sample incident", value=True)
        claim_id = st.text_input(
            "Claim reference (optional)",
            "CLM-2026-0917-0042" if use_sample else "",
            help="Used as metadata in the downloaded assessment.",
        )
        policyholder = st.text_input(
            "Policyholder (optional)",
            "Jordan Mitchell" if use_sample else "",
            help="Used to personalize the claims-handler summary.",
        )
        vehicle_type = st.selectbox("Asset type", ["Passenger vehicle", "Commercial vehicle", "Property"])
        incident_date = st.date_input("Incident date", date.today())
        st.divider()

    with st.container(border=True):
        st.markdown('<div class="section-kicker">Step 1 / Evidence intake</div>', unsafe_allow_html=True)
        st.markdown("### Upload incident photos")
        st.markdown(
            '<p class="section-subtitle">Add clear photos from multiple angles. JPG, PNG and WEBP files are supported.</p>',
            unsafe_allow_html=True,
        )
        uploaded_files = st.file_uploader(
            "Upload incident photos",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            help="Upload one or more clear photos of the damaged asset.",
            label_visibility="collapsed",
        )

    if use_sample and not uploaded_files:
        image_items = [("sample_rear_damage.png", sample_image())]
        st.success("Sample incident loaded. Upload your own images to replace it.")
    else:
        image_items = []
        for uploaded_file in uploaded_files or []:
            try:
                image_items.append((uploaded_file.name, Image.open(uploaded_file)))
            except (OSError, ValueError) as exc:
                st.error(f"Could not read {uploaded_file.name}: {exc}")

    if not image_items:
        st.markdown("### Upload photos to start")
        st.write("Add one or more incident photos above to generate damage findings, confidence and a repair estimate.")
        return

    assessments = [assess_image(image, name, vehicle_type) for name, image in image_items]
    assessment = assessments[0]
    findings = assessment["findings"]
    estimate = sum(item["cost"] for item in findings)
    confidence = assessment["confidence"]

    with st.container(border=True):
        st.markdown('<div class="section-kicker">Step 2 / AI-assisted review</div>', unsafe_allow_html=True)
        st.markdown("### Assessment overview")
        st.markdown(
            '<p class="section-subtitle">A consistent first-pass view to help the handler prioritize the claim.</p>',
            unsafe_allow_html=True,
        )
        metric_cols = st.columns(4)
        with metric_cols[0]:
            render_metric("Recommended route", "Human review", "High-impact damage")
        with metric_cols[1]:
            render_metric("Damage severity", assessment["severity"], "Based on visual signals")
        with metric_cols[2]:
            render_metric("Model confidence", f"{confidence}%", "POC confidence score")
        with metric_cols[3]:
            render_metric("Repair estimate", f"${estimate:,.0f}", "Parts + labor placeholder")

    left, right = st.columns([1.08, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="section-kicker">Evidence reviewed</div>', unsafe_allow_html=True)
            st.markdown("### Incident photos")
            image_cols = st.columns(min(3, len(image_items)))
            for index, (name, image) in enumerate(image_items):
                with image_cols[index % len(image_cols)]:
                    st.image(image, caption=name, use_container_width=True)
            st.caption(f"{len(image_items)} photo(s) processed locally • image quality: sufficient")

    with right:
        with st.container(border=True):
            st.markdown('<div class="section-kicker">Computer vision output</div>', unsafe_allow_html=True)
            st.markdown("### Detected damage")
            for finding in findings:
                st.markdown(
                    f'<div class="finding"><strong>{finding["part"]}</strong>'
                    f'<br><small>{finding["damage"]} • {finding["severity"]} severity'
                    f' • estimated ${finding["cost"]:,}</small></div>',
                    unsafe_allow_html=True,
                )

    st.divider()
    summary_left, summary_right = st.columns([1.4, 1])
    with summary_left:
        st.markdown('<div class="section-kicker">Step 3 / Handler review</div>', unsafe_allow_html=True)
        st.markdown("### Claims handler summary")
        st.caption("Edit the generated narrative before saving it to the claim file.")
        subject = f"{policyholder}'s " if policyholder.strip() else "The "
        st.text_area(
            "Editable summary",
            value=(
                f"{subject}{vehicle_type.lower()} shows {assessment['severity'].lower()} "
                f"damage concentrated around the rear bumper and right rear quarter panel. "
                f"Initial repair estimate is ${estimate:,}. Route to human review before settlement."
            ),
            height=125,
            label_visibility="collapsed",
        )
    with summary_right:
        st.markdown('<div class="section-kicker">Recommended workflow</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="action-card"><strong>NEXT BEST ACTION</strong>'
            '<p>Request one close-up of the impact area and validate coverage before approval.</p></div>',
            unsafe_allow_html=True,
        )
        st.progress(confidence / 100, text=f"Assessment confidence {confidence}%")

    payload = {
        "claim_id": claim_id,
        "policyholder": policyholder,
        "incident_date": incident_date.isoformat(),
        "asset_type": vehicle_type,
        "photo_count": len(image_items),
        "assessment": {"severity": assessment["severity"], "confidence": confidence, "estimate": estimate, "findings": findings},
    }
    download_name = claim_id.strip().lower() or "claim-assessment"
    st.download_button(
        "Download assessment JSON",
        data=json.dumps(payload, indent=2),
        file_name=f"{download_name}-assessment.json",
        mime="application/json",
        type="primary",
    )

if __name__ == "__main__":
    main()
