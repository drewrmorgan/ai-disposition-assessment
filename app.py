import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(
    page_title="AI Disposition Assessment",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

html, body, [class*="css"] {
    font-size: 20px;
}

p, div, label {
    font-size: 20px !important;
}

h1 {
    font-size: 40px !important;
}

h2 {
    font-size: 32px !important;
}

h3 {
    font-size: 28px !important;
}

</style>
""", unsafe_allow_html=True)
def generate_pdf(primary, secondary, dimension_scores):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("AI Disposition Assessment Report", styles['Title'])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"<b>Primary Persona:</b> {primary}", styles['BodyText'])
    )

    content.append(
        Paragraph(f"<b>Secondary Persona:</b> {secondary}", styles['BodyText'])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph("Disposition Scores", styles['Heading2'])
    )

    for dimension, score in dimension_scores.items():
        content.append(
            Paragraph(
                f"{dimension}: {score}%",
                styles['BodyText']
            )
        )

    doc.build(content)

    buffer.seek(0)

    return buffer
# ----------------------------------
# PERSONAS
# ----------------------------------

PERSONAS = {
    "Reflective Explorer": {
        "description": """
You use AI as a tool for learning, exploration, and growth. You are curious
about new possibilities while remaining aware of how AI influences your thinking.
""",
        "strengths": [
            "Curiosity",
            "Self-awareness",
            "Lifelong learning"
        ],
        "growth": "Explore opportunities to mentor others in thoughtful AI use."
    },

    "Critical Evaluator": {
        "description": """
You approach AI thoughtfully and verify information before acting on it. Accuracy
and evidence matter more than convenience.
""",
        "strengths": [
            "Discernment",
            "Judgment",
            "Analytical thinking"
        ],
        "growth": "Experiment with more creative and exploratory uses of AI."
    },

    "Efficient Collaborator": {
        "description": """
You see AI as a practical partner that helps you work more effectively and save time.
""",
        "strengths": [
            "Productivity",
            "Strategic use",
            "Organization"
        ],
        "growth": "Consider which tasks are valuable learning experiences even when AI could do them."
    },

    "AI Enthusiast": {
        "description": """
You embrace innovation and enjoy discovering new AI capabilities.
""",
        "strengths": [
            "Adaptability",
            "Early adoption",
            "Innovation"
        ],
        "growth": "Continue strengthening habits of verification and fact-checking."
    },

    "Cautious Observer": {
        "description": """
You are interested in AI but adopt it selectively and thoughtfully.
""",
        "strengths": [
            "Prudence",
            "Independent thinking",
            "Risk awareness"
        ],
        "growth": "Explore situations where AI can enhance creativity and learning."
    },

    "Independent Thinker": {
        "description": """
You place high value on personal reasoning and maintain strong intellectual independence.
""",
        "strengths": [
            "Autonomy",
            "Self-reliance",
            "Personal judgment"
        ],
        "growth": "Consider opportunities to use AI as a thought partner rather than a shortcut."
    }
}

# ----------------------------------
# QUESTIONS
# ----------------------------------

questions = {
    "Curiosity": [
        "I use AI to explore ideas I would not have considered on my own.",
        "AI helps me discover new perspectives.",
        "I enjoy experimenting with AI tools and prompts.",
        "I use AI to deepen my understanding of topics."
    ],

    "Critical Thinking": [
        "I verify important information provided by AI.",
        "I recognize that AI can be wrong or misleading.",
        "I compare AI responses with other sources.",
        "I evaluate AI output before acting on it."
    ],

    "Trust": [
        "I generally trust AI-generated responses.",
        "I feel comfortable using AI recommendations.",
        "AI provides useful guidance.",
        "I often rely on AI's first response."
    ],

    "Dependence": [
        "AI has become part of my daily routine.",
        "I turn to AI before attempting some tasks myself.",
        "It would be difficult to complete certain tasks without AI.",
        "I use AI whenever it is available."
    ],

    "Ethical Awareness": [
        "I think about bias when reviewing AI-generated content.",
        "I consider ethical implications of AI use.",
        "Transparency matters when AI assists with work.",
        "I think about AI's impact on society."
    ],

    "Reflection & Agency": [
        "I regularly reflect on how AI influences my thinking.",
        "I intentionally decide when not to use AI.",
        "I recognize situations where AI may reduce my learning.",
        "I think about how my AI habits are developing."
    ]
}

# ----------------------------------
# HEADER
# ----------------------------------

st.title("🤖 AI Disposition Assessment")

st.markdown("""
This assessment is designed to help you reflect on your attitudes,
habits, and beliefs regarding AI.

Rate each statement according to how strongly you agree.
""")

# ----------------------------------
# SURVEY
# ----------------------------------

responses = {}

for category, items in questions.items():

    st.header(category)

    for i, question in enumerate(items):

        key = f"{category}_{i}"

        responses[key] = st.radio(
            question,
            [1, 2, 3, 4, 5],
            horizontal=True,
            format_func=lambda x: {
                1: "Strongly Disagree",
                2: "Disagree",
                3: "Neutral",
                4: "Agree",
                5: "Strongly Agree"
            }[x],
            key=key
        )

# ----------------------------------
# SCORING
# ----------------------------------

if st.button("Generate My Profile"):

    dimension_scores = {}

    for category, items in questions.items():

        values = []

        for i in range(len(items)):
            values.append(responses[f"{category}_{i}"])

        score = sum(values) / len(values)

        dimension_scores[category] = round(score * 20, 1)

    # Persona logic

    persona_scores = {
        "Reflective Explorer":
            dimension_scores["Curiosity"] +
            dimension_scores["Reflection & Agency"],

        "Critical Evaluator":
            dimension_scores["Critical Thinking"] +
            dimension_scores["Ethical Awareness"],

        "Efficient Collaborator":
            dimension_scores["Dependence"] +
            dimension_scores["Critical Thinking"],

        "AI Enthusiast":
            dimension_scores["Trust"] +
            dimension_scores["Curiosity"],

        "Cautious Observer":
            dimension_scores["Critical Thinking"] +
            (100 - dimension_scores["Trust"]),

        "Independent Thinker":
            dimension_scores["Reflection & Agency"] +
            (100 - dimension_scores["Dependence"])
    }

    ranked = sorted(
        persona_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary = ranked[0][0]
    secondary = ranked[1][0]

    st.success(f"Primary Persona: {primary}")
    st.info(f"Secondary Persona: {secondary}")

    st.subheader("Your Persona")

    st.write(PERSONAS[primary]["description"])

    st.markdown("### Strengths")

    for item in PERSONAS[primary]["strengths"]:
        st.write(f"✅ {item}")

    st.markdown("### Growth Opportunity")
    st.write(PERSONAS[primary]["growth"])

    # ----------------------------------
    # RADAR CHART
    # ----------------------------------

    categories = list(dimension_scores.keys())
    values = list(dimension_scores.values())

    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Disposition Profile'
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------
    # SCORE TABLE
    # ----------------------------------

    st.subheader("Disposition Scores")

    df = pd.DataFrame({
        "Dimension": dimension_scores.keys(),
        "Score": dimension_scores.values()
    })

    st.dataframe(df, use_container_width=True)

    # ----------------------------------
    # REFLECTION
    # ----------------------------------

    st.subheader("Reflection Questions")

    if primary == "Reflective Explorer":
        st.write(
            "How might you help others become more intentional in their use of AI?"
        )

    elif primary == "Critical Evaluator":
        st.write(
            "Where might experimentation with AI help you discover new possibilities?"
        )

    elif primary == "Efficient Collaborator":
        st.write(
            "Which tasks are worth doing yourself because they contribute to learning?"
        )

    elif primary == "AI Enthusiast":
        st.write(
            "What habits help you distinguish between convenience and overreliance?"
        )

    elif primary == "Cautious Observer":
        st.write(
            "What low-risk opportunities could help you explore AI more confidently?"
        )

    elif primary == "Independent Thinker":
        st.write(
            "What might AI contribute as a thought partner without replacing your judgment?"
        )

st.markdown("---")

pdf_file = generate_pdf(
    primary,
    secondary,
    dimension_scores
)

 st.download_button(
    label="📄 Download My Report",
    data=pdf_file,
    file_name="AI_Disposition_Report.pdf",
    mime="application/pdf"
)

st.caption("AI Disposition Assessment v1.0")
