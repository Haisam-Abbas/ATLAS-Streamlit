import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import numpy as np
import os

# ── Colors ────────────────────────────────────────────────────────────────────
BG = "#ffffff"
SURFACE = "#f7f5f0"
GOLD = "#9a6f2e"
GOLD2 = "#b8862e"
CREAM = "#1a1a1a"
DIM = "#666666"
DIM2 = "#cccccc"
TEAL = "#1a7a5e"

plt.rcParams.update(
    {
        "font.family": "serif",
        "text.color": "#1a1a1a",
        "axes.facecolor": BG,
        "figure.facecolor": BG,
        "axes.edgecolor": "#dddddd",
        "xtick.color": DIM,
        "ytick.color": "#333333",
        "grid.color": "#eeeeee",
        "grid.linewidth": 0.6,
    }
)

st.set_page_config(
    page_title="ATLAS — The Olfactory Map of the World",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=Montserrat:wght@200;300;400;500&display=swap');

html, body, [class*="css"] { background-color: #ffffff; color: #1a1a1a; }
.main { background-color: #ffffff; }
.block-container { 
    padding-top: 3rem;   /* was 1.5rem */
    padding-bottom: 2rem; 
    max-width: 1400px; 
}

h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #1a1a1a !important; }
p, div, span, label { font-family: 'Montserrat', sans-serif; color: #1a1a1a; }

[data-testid="stSidebar"] { background-color: #f7f5f0; border-right: 1px solid #e8e4dc; }
[data-testid="stSidebar"] * { color: #888 !important; font-family: 'Montserrat', sans-serif; }

.stat-card {
    background: #f7f5f0;
    border: 1px solid #e8e4dc;
    border-top: 2px solid #9a6f2e;
    border-radius: 2px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.stat-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem;
    font-weight: 600;
    color: #9a6f2e;
    line-height: 1;
}
.stat-label {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.62rem;
    color: #999;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.gold-rule {
    border: none;
    border-top: 1px solid #9a6f2e;
    margin: 0.5rem 0 1.2rem 0;
    opacity: 0.3;
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: #1a1a1a;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
}
.section-sub {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.68rem;
    color: #aaa;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.insight-box {
    background: #f7f5f0;
    border-left: 2px solid #9a6f2e;
    padding: 0.9rem 1.3rem;
    border-radius: 0 4px 4px 0;
    font-size: 0.78rem;
    color: #666;
    line-height: 1.8;
    margin: 0.8rem 0;
}
.zero-tag {
    display: inline-block;
    background: #f7f5f0;
    border: 1px solid #e8e4dc;
    color: #bbb;
    padding: 3px 10px;
    border-radius: 2px;
    font-size: 0.7rem;
    margin: 2px;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.05em;
}
.city-card {
    border-left: 1px solid #e8e4dc;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    background: #f7f5f0;
    border-radius: 0 3px 3px 0;
}
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""",
    unsafe_allow_html=True,
)


# ── Load CSV ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_csv():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, "kepler_scattered_v5.csv")
    return pd.read_csv(path)

df = load_csv()

TOTAL_PERFUMES = 1571
TOTAL_NOTES_OCCURRENCES = 12846

NOTES_TOP = {
    "Bergamot": 547,
    "Patchouli": 540,
    "Musk": 447,
    "Jasmine": 438,
    "Vanilla": 379,
    "Amber": 353,
    "Rose": 325,
    "Cedar": 289,
    "Sandalwood": 277,
    "Mandarin Orange": 265,
    "Orange Blossom": 259,
    "Vetiver": 215,
    "Tonka Bean": 182,
    "Lavender": 174,
    "Pink Pepper": 173,
    "Iris": 147,
    "Pear": 128,
    "White Musk": 125,
    "Lily-of-the-Valley": 123,
    "Ginger": 122,
    "Lemon": 121,
    "Leather": 121,
    "Cardamom": 119,
    "Benzoin": 118,
    "Black Currant": 111,
}
TERRA_NOTES = {
    "Neem": 0,
    "Marigold": 8,
    "Turmeric": 1,
    "Pandan": 0,
    "Copal": 0,
    "Bukhoor": 0,
    "Petrichor": 0,
    "Champaca": 0,
    "Bissap": 0,
    "Rooibos": 0,
}
ZERO_PLACES = [
    "Lahore",
    "Karachi",
    "Accra",
    "Lagos",
    "Nairobi",
    "Dakar",
    "Cartagena",
    "Zanzibar",
    "Dhaka",
    "Colombo",
    "Hanoi",
    "Addis Ababa",
    "Kampala",
    "Yangon",
]
WESTERN = [
    "Italian (North)",
    "Italian (South)",
    "Mediterranean (West)",
    "Mediterranean (East)",
    "Paris",
    "France",
    "Provence",
    "Rome",
    "Sicilian",
    "Cassis",
    "Calabria",
    "Grasse",
    "Cologne",
    "Florentine",
    "Venice",
    "Milan",
    "Pantelleria",
    "Capri",
    "Florence",
    "Amalfi",
    "Aegean",
    "Barcelona",
    "Spain",
    "Cordoba",
    "London",
    "Brussels",
    "Amsterdam",
    "Hollywood",
    "Virginia",
    "Georgia",
    "Texas",
    "Los Angeles",
    "Brooklyn",
    "Manhattan",
    "New York City",
    "Southern France",
    "Venetian",
    "Tuscany",
    "Piedmont",
    "Cyclades",
    "Bulgaria",
    "Slovenia",
    "Bristol",
    "The Netherlands",
    "Istanbul",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"""
    <div style="padding:1.5rem 0 2rem 0;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                    color:{GOLD};font-weight:600;letter-spacing:0.1em;">ATLAS</div>
        <div style="font-size:0.58rem;color:{DIM2};letter-spacing:0.2em;
                    text-transform:uppercase;margin-top:0.2rem;">
            The Olfactory Map of the World
        </div>
    </div>
    <hr style="border-color:#e8e4dc;margin-bottom:1.5rem;">
    """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "",
        ["The Gap", "World Heatmap", "Note Dominance", "The Opportunity"],
        label_visibility="collapsed",
    )

    st.markdown(
        f"""
    <hr style="border-color:#e8e4dc;margin-top:2rem;">
    <div style="font-size:0.58rem;color:{DIM2};letter-spacing:0.1em;
                text-transform:uppercase;padding-top:1rem;line-height:2.2;">
        L'Oréal Brandstorm 2026<br>1,571 fragrances analyzed<br>13 L'Oréal Luxe brands<br>Team ATLAS
    </div>
    """,
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — THE GAP
# ══════════════════════════════════════════════════════════════════════════════
if page == "The Gap":
    st.markdown(
        f"""
    <div style="padding:1rem 0 0.5rem 0;">
        <div style="font-family:'Cormorant Garamond',serif;font-size:3.2rem;
                    font-weight:700;color:{CREAM};line-height:1.1;">
            The world smells<br>
            <span style="color:{GOLD};">like one place.</span>
        </div>
        <div style="font-family:'Montserrat',sans-serif;font-size:0.72rem;color:{GOLD};
                    letter-spacing:0.15em;text-transform:uppercase;margin-top:1rem;font-weight:600;">
            A data analysis of 1,571 L'Oréal Luxe fragrances · 13 brands · 685,000 language vectors
        </div>
    </div>
    <hr class="gold-rule">
    """,
        unsafe_allow_html=True,
    )

    total_mentions = int(df["count"].sum())
    west_count = int(df[df["place"].isin(WESTERN)]["count"].sum())
    west_pct = round(west_count / total_mentions * 100)

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in [
        (c1, f"{TOTAL_PERFUMES:,}", "Fragrances Analyzed"),
        (c2, "13", "L'Oréal Luxe Brands"),
        (c3, f"{west_pct}%", "Western & European"),
        (c4, str(len(ZERO_PLACES)), "Cities With Zero Mentions"),
    ]:
        col.markdown(
            f'<div class="stat-card"><div class="stat-number">{num}</div>'
            f'<div class="stat-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            '<div class="section-title">The Finding</div>'
            '<div class="section-sub">Geographic mentions in perfume descriptions — top 20 places</div>',
            unsafe_allow_html=True,
        )

        place_totals = (
            df.groupby("place")["count"].sum().sort_values(ascending=False).head(20)
        )
        bar_colors = [GOLD if p in WESTERN else TEAL for p in place_totals.index]

        fig, ax = plt.subplots(figsize=(8, 6.5))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        ax.barh(
            range(len(place_totals) - 1, -1, -1),
            place_totals.values,
            color=bar_colors,
            edgecolor="none",
            height=0.7,
            zorder=2,
        )
        ax.set_yticks(range(len(place_totals)))
        ax.set_yticklabels(place_totals.index[::-1], fontsize=9, color=CREAM)
        ax.tick_params(axis="x", colors=DIM, labelsize=7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color(DIM2)
        ax.grid(axis="x", color="#eeeeee", linewidth=0.6, linestyle="--")
        gold_p = plt.Rectangle((0, 0), 1, 1, fc=GOLD)
        teal_p = plt.Rectangle((0, 0), 1, 1, fc=TEAL)
        ax.legend(
            [gold_p, teal_p],
            ["Western / European", "Global South"],
            loc="lower right",
            fontsize=8,
            facecolor=SURFACE,
            edgecolor=DIM2,
            labelcolor=CREAM,
        )
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with right:
        st.markdown(
            '<div class="section-title">The Silence</div>'
            '<div class="section-sub">Cities with zero mentions across all 1,571 perfumes</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="insight-box">These cities — home to billions of people and centuries '
            f"of fragrance tradition — do not appear a single time across L'Oréal's entire "
            f"fragrance portfolio.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            " ".join([f'<span class="zero-tag">{p}</span>' for p in ZERO_PLACES]),
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.35rem;
                    color:{CREAM};line-height:1.7;margin-top:1.5rem;">
            "Fragrance is 4,000 years old.<br>
            The industry tells <span style="color:{GOLD};">one story.</span>"
        </div>
        <div style="font-family:'Montserrat',sans-serif;font-size:0.68rem;color:{GOLD};
                    margin-top:1.2rem;line-height:1.8;">
            Powered by a custom Python scraper + spaCy NLP (685,000 vectors) applied
            to perfume marketing descriptions across 13 L'Oréal Luxe brand portfolios.
        </div>
        """,
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — WORLD HEATMAP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "World Heatmap":
    st.markdown(
        "<div class=\"section-title\">Where Does L'Oréal's Fragrance World Exist?</div>"
        '<div class="section-sub">Geographic density of mentions · brighter = more mentions · dark = zero</div>'
        '<hr class="gold-rule">',
        unsafe_allow_html=True,
    )

    heat_data = []
    for _, row in df.iterrows():
        for _ in range(int(row["count"])):
            heat_data.append([float(row["lat"]), float(row["lng"]), 1])

    m = folium.Map(location=[25.0, 15.0], zoom_start=2, tiles=None, prefer_canvas=True)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB",
        name="Dark",
        max_zoom=19,
    ).add_to(m)

    HeatMap(
        heat_data,
        min_opacity=0.35,
        max_zoom=6,
        radius=38,
        blur=28,
        gradient={
            "0.2": "#001233",
            "0.4": "#023e8a",
            "0.6": "#e85d04",
            "0.8": "#f48c06",
            "1.0": "#ffff3f",
        },
    ).add_to(m)

    place_totals = (
        df.groupby("place")
        .agg({"count": "sum", "lat": "mean", "lng": "mean"})
        .reset_index()
    )
    for _, row in place_totals.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lng"]],
            radius=max(3, min(float(row["count"]) * 0.8, 16)),
            color=GOLD,
            fill=True,
            fill_color=GOLD,
            fill_opacity=0.15,
            popup=folium.Popup(
                f"<b>{row['place']}</b><br>{int(row['count'])} mentions", max_width=180
            ),
            tooltip=f"{row['place']}: {int(row['count'])}",
        ).add_to(m)

    st_folium(m, width=None, height=580, returned_objects=[])
    st.markdown(
        f'<div class="insight-box"><strong style="color:{GOLD};">Reading the map.</strong> '
        f"Yellow = highest mentions. Blue = low. Black = zero. The darkness across Africa, "
        f"South Asia and Southeast Asia is not a gap in data — it is the finding.</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — NOTE DOMINANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Note Dominance":
    st.markdown(
        '<div class="section-title">The Same Notes. Over and Over Again.</div>'
        '<div class="section-sub">Frequency analysis across 1,571 perfumes · 564 unique notes identified</div>'
        '<hr class="gold-rule">',
        unsafe_allow_html=True,
    )

    notes_sorted = sorted(NOTES_TOP.items(), key=lambda x: x[1], reverse=True)
    all_counts_n = [v for _, v in notes_sorted]
    top10_pct = sum(all_counts_n[:10]) / TOTAL_NOTES_OCCURRENCES * 100

    c1, c2, c3 = st.columns(3)
    for col, num, label in [
        (c1, f"{top10_pct:.0f}%", "Of all note slots filled by top 10 notes"),
        (c2, "564", "Unique notes identified"),
        (c3, f"{TOTAL_NOTES_OCCURRENCES:,}", "Total note occurrences"),
    ]:
        col.markdown(
            f'<div class="stat-card"><div class="stat-number">{num}</div>'
            f'<div class="stat-label">{label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        st.markdown(
            f"<div style=\"font-family:'Cormorant Garamond',serif;font-size:1rem;"
            f'color:{DIM};margin-bottom:0.5rem;letter-spacing:0.05em;">'
            f"TOP 25 NOTES BY PERFUME COUNT</div>",
            unsafe_allow_html=True,
        )

        top25 = notes_sorted[:25]
        names_top = [n[0] for n in top25]
        counts_top = [n[1] for n in top25]

        fig, ax = plt.subplots(figsize=(7, 7))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        bar_colors = [plt.cm.YlOrBr(0.85 - 0.5 * (i / 25)) for i in range(25)]
        y_pos = list(range(24, -1, -1))
        for y in y_pos:
            ax.barh(y, TOTAL_PERFUMES, color="#f0ede8", height=0.72, zorder=1)
        ax.barh(
            y_pos, counts_top, color=bar_colors, height=0.72, edgecolor="none", zorder=2
        )
        for count, y in zip(counts_top, y_pos):
            ax.text(
                count + 15,
                y,
                f"{count/TOTAL_PERFUMES*100:.0f}%",
                va="center",
                fontsize=7,
                color=DIM,
            )
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names_top, fontsize=8.5, color=CREAM)
        ax.set_xlim(0, TOTAL_PERFUMES * 1.22)
        ax.tick_params(axis="x", colors=DIM, labelsize=6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color(DIM2)
        ax.grid(axis="x", color="#eeeeee", linewidth=0.6, linestyle="--")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with right:
        st.markdown(
            f"<div style=\"font-family:'Cormorant Garamond',serif;font-size:1rem;"
            f'color:{DIM};margin-bottom:0.5rem;letter-spacing:0.05em;">'
            f"NOTE CONCENTRATION — PARETO CURVE</div>",
            unsafe_allow_html=True,
        )

        # Build full sorted counts for pareto (use NOTES_TOP as proxy)
        all_vals = sorted(NOTES_TOP.values(), reverse=True)
        total_occ = TOTAL_NOTES_OCCURRENCES
        cum_pct = np.cumsum(all_vals) / total_occ * 100
        x_range = np.arange(1, len(all_vals) + 1)

        # Find thresholds
        def n_to_cover(pct):
            for i, c in enumerate(cum_pct):
                if c >= pct:
                    return i + 1
            return len(all_vals)

        n50 = n_to_cover(50)
        n75 = n_to_cover(75)
        n90 = n_to_cover(90)

        fig2, ax2 = plt.subplots(figsize=(7, 7))
        fig2.patch.set_facecolor(BG)
        ax2.set_facecolor(BG)

        # Fill + line
        ax2.fill_between(x_range, cum_pct, alpha=0.08, color=GOLD)
        ax2.plot(x_range, cum_pct, color=GOLD, linewidth=2.5, zorder=3)

        # Reference lines at 50 / 75 / 90
        for threshold, color, label in [
            (50, TEAL, f"{n50} notes → 50%"),
            (75, GOLD2, f"{n75} notes → 75%"),
            (90, "#aaaaaa", f"{n90} notes → 90%"),
        ]:
            n = n_to_cover(threshold)
            ax2.axhline(
                y=threshold,
                color=color,
                linewidth=0.8,
                linestyle="--",
                alpha=0.7,
                zorder=2,
            )
            ax2.axvline(
                x=n, color=color, linewidth=0.8, linestyle="--", alpha=0.7, zorder=2
            )
            ax2.scatter([n], [threshold], color=color, s=55, zorder=5)
            ax2.text(n + 0.4, threshold - 4, label, fontsize=8, color=color)

        # Top 10 shaded zone
        ax2.axvspan(0, 10, alpha=0.05, color=GOLD, zorder=0)
        ax2.text(
            5.5,
            8,
            "TOP\n10",
            fontsize=8,
            color=GOLD,
            ha="center",
            fontweight="bold",
            alpha=0.7,
        )

        ax2.set_xlabel(
            "Number of unique notes (ranked by frequency)",
            fontsize=8.5,
            color=DIM,
            labelpad=8,
        )
        ax2.set_ylabel(
            "Cumulative % of total note occurrences",
            fontsize=8.5,
            color=DIM,
            labelpad=8,
        )
        ax2.set_xlim(0, len(all_vals))
        ax2.set_ylim(0, 103)
        ax2.tick_params(colors=DIM, labelsize=7)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["bottom"].set_color(DIM2)
        ax2.spines["left"].set_color(DIM2)
        ax2.grid(True, color="#eeeeee", linewidth=0.6)

        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()

        st.markdown(
            f'<div class="insight-box">'
            f'Just <strong style="color:{GOLD};">{n50} notes</strong> account for '
            f"50% of every note slot across all 1,571 perfumes. "
            f"Out of 564 unique notes identified, the industry keeps reaching "
            f"for the same narrow palette — leaving the vast majority of the "
            f"world's ingredients untouched."
            f"</div>",
            unsafe_allow_html=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — THE OPPORTUNITY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "The Opportunity":
    st.markdown(
        f'<div class="section-title">ATLAS</div>'
        f'<div class="section-sub">The Olfactory Map of the World · L\'Oréal Brandstorm 2026</div>'
        f'<hr class="gold-rule">',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1])

    with left:
        st.markdown(
            f"""
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.45rem;
                    color:{CREAM};line-height:1.8;margin-bottom:1.5rem;">
            Modern luxury perfumery is geographically concentrated
            and narratively repetitive.<br><br>
            <span style="color:{GOLD};">ATLAS changes that.</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        for city, notes in [
            ("The Scent of Lahore", "Marigold · Neem · Attar · Petrichor on red earth"),
            (
                "The Scent of Marrakech",
                "Bukhoor · Rose de Taif · Atlas Cedar · Spice Market",
            ),
            (
                "The Scent of Cartagena",
                "Copal · Tropical Bloom · Caribbean Sea Salt · Cacao",
            ),
            (
                "The Scent of Singapore",
                "Pandan · Frangipani · Kampong Rain · Night Market",
            ),
            ("The Scent of Accra", "Shea · Bissap · Harmattan Dust · Kente Cotton"),
        ]:
            st.markdown(
                f"""
            <div class="city-card">
                <div style="font-family:'Cormorant Garamond',serif;font-size:1rem;
                            color:{GOLD};font-weight:600;">{city}</div>
                <div style="font-family:'Montserrat',sans-serif;font-size:0.7rem;
                            color:{DIM};margin-top:0.2rem;letter-spacing:0.05em;">{notes}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            f"<div style=\"font-family:'Montserrat',sans-serif;font-size:0.68rem;"
            f"color:{DIM2};text-transform:uppercase;letter-spacing:0.12em;"
            f'margin-bottom:1rem;">How it works</div>',
            unsafe_allow_html=True,
        )

        for step, title, body in [
            (
                "01",
                "Identify",
                "Partner with local ethnobotanists and cultural historians to map a city's olfactory DNA.",
            ),
            (
                "02",
                "Source",
                "Work with indigenous ingredient communities. Local supply chains. Traceable provenance.",
            ),
            (
                "03",
                "Create",
                "Co-develop with regional artisan perfumers. Made by the people who live the scent.",
            ),
            (
                "04",
                "Launch",
                "Each release is a cultural moment — a documentary, a local collaborator, a story.",
            ),
            (
                "05",
                "Scale",
                "Every city is a new chapter. ATLAS builds the world's olfactory library indefinitely.",
            ),
        ]:
            st.markdown(
                f"""
            <div style="display:flex;gap:1rem;margin-bottom:0.8rem;align-items:flex-start;">
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;
                            color:{DIM2};font-weight:600;min-width:2rem;">{step}</div>
                <div>
                    <div style="font-family:'Montserrat',sans-serif;font-size:0.7rem;
                                color:{GOLD};font-weight:500;letter-spacing:0.1em;
                                text-transform:uppercase;">{title}</div>
                    <div style="font-family:'Montserrat',sans-serif;font-size:0.75rem;
                                color:{DIM};margin-top:0.2rem;line-height:1.6;">{body}</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
        <div style="margin-top:1.5rem;padding:1.2rem 1.5rem;background:{SURFACE};
                    border:1px solid #e8e4dc;border-top:2px solid {GOLD};">
            <div style="font-family:'Cormorant Garamond',serif;font-size:0.8rem;
                        color:{GOLD};letter-spacing:0.1em;text-transform:uppercase;
                        margin-bottom:0.5rem;">Pilot — The Scent of Lahore</div>
            <div style="font-family:'Montserrat',sans-serif;font-size:0.75rem;
                        color:{DIM};line-height:1.8;">
                Estimated cost: <span style="color:{GOLD};">$35,000–55,000 USD</span><br>
                Estimated cost per bottle: $75 - $120 <br>
                Average luxury fragrance price: <span style="color:{GOLD};">$100+</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown(
    f'<div style="text-align:center;color:{GOLD};font-size:0.65rem;'
    f"font-family:'Montserrat',sans-serif;margin-top:3rem;"
    f'letter-spacing:0.1em;font-style:italic;">'
    f"ATLAS · L'Oréal Brandstorm 2026 · Haisam Abbas, Laima Imran, Danish Raza</div>",
    unsafe_allow_html=True,
)
