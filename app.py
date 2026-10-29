
import streamlit as st
import pandas as pd
from io import BytesIO
from html import escape
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Virtual Career Counsellor",
    page_icon="🎓",
    layout="wide"
)

# ---------------- NAVY, SLATE & TEAL THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
    color: #172033;
}

section[data-testid="stSidebar"] {
    background-color: #E5EDF6;
}

.stApp h1, .stApp h2, .stApp h3,
.stApp h4, .stApp p, .stApp label,
.stApp li, .stApp [data-testid="stMarkdownContainer"] {
    color: #172033;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #172033;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background-color: #244A73;
    color: #FFFFFF !important;
    border: 1px solid #244A73;
    border-radius: 10px;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #35658F;
    color: #FFFFFF !important;
    border-color: #35658F;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF;
    color: #172033 !important;
    border-color: #B9C9DC;
}

/* Dropdowns */
[data-baseweb="select"] > div {
    background-color: #FFFFFF;
    color: #172033;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #E7EEF7;
    border: 1px solid #D2DEEB;
    border-radius: 12px;
}

[data-testid="stChatMessage"] p {
    color: #172033 !important;
}

/* Information panels */
[data-testid="stAlert"] {
    background-color: #E7EEF7;
    color: #172033;
    border-radius: 10px;
}

[data-testid="stAlert"] p {
    color: #172033 !important;
}

/* Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #F4F7FB;
    color: #172033;
}

/* Radio buttons, checkboxes and captions */
.stRadio label,
.stCheckbox label,
.stCaption,
small {
    color: #172033 !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-color: #B9C9DC;
}

/* Links */
.stApp a {
    color: #244A73;
}

/* Accent color */
.stProgress > div > div {
    background-color: #287D86;
}
</style>
""", unsafe_allow_html=True)


# ---------------- CAREER DATABASE ----------------
CAREERS = {
    "Software Developer": {
        "interests": ["Coding", "Problem Solving", "Technology"],
        "skills": ["Python", "Programming", "Git", "Data Structures"],
        "education": "Computer Science, IT, or related studies",
        "roadmap": [
            "Learn Python basics",
            "Practise programming problems",
            "Learn data structures",
            "Learn Git and GitHub",
            "Build a software project"
        ]
    },

    "Data Analyst": {
        "interests": ["Data Analysis", "Mathematics", "Business"],
        "skills": ["Excel", "SQL", "Python", "Data Visualization"],
        "education": "Data, business, mathematics, or computing",
        "roadmap": [
            "Learn Excel",
            "Learn SQL",
            "Learn Python and Pandas",
            "Create charts and dashboards",
            "Complete a data analysis project"
        ]
    },

    "Data Scientist": {
        "interests": ["Data Analysis", "Mathematics", "Research"],
        "skills": ["Python", "Statistics", "Pandas", "Machine Learning"],
        "education": "Computing, mathematics, or a related field",
        "roadmap": [
            "Learn Python",
            "Study statistics",
            "Practise Pandas",
            "Learn machine learning",
            "Build a prediction project"
        ]
    },

    "UI/UX Designer": {
        "interests": ["Design", "Creativity", "Arts"],
        "skills": ["Creativity", "Wireframing", "Prototyping", "Design"],
        "education": "Design, computing, or portfolio-based learning",
        "roadmap": [
            "Learn design principles",
            "Study user experience",
            "Create wireframes",
            "Practise prototyping",
            "Build a design portfolio"
        ]
    },

    "Cybersecurity Analyst": {
        "interests": ["Security", "Technology", "Problem Solving"],
        "skills": ["Networking", "Linux", "Security Basics"],
        "education": "Computing, networking, or cybersecurity",
        "roadmap": [
            "Learn computer networks",
            "Practise Linux basics",
            "Study security fundamentals",
            "Use authorised practice labs",
            "Document security projects"
        ]
    },

    "Business Analyst": {
        "interests": ["Business", "Communication", "Data Analysis"],
        "skills": ["Excel", "SQL", "Communication", "Analysis"],
        "education": "Business, computing, or related studies",
        "roadmap": [
            "Learn business fundamentals",
            "Practise Excel",
            "Learn basic SQL",
            "Study requirements analysis",
            "Complete a business case study"
        ]
    },

    "Digital Marketer": {
        "interests": ["Business", "Communication", "Creativity"],
        "skills": ["Writing", "Marketing", "Analytics"],
        "education": "Marketing, business, or communications",
        "roadmap": [
            "Learn marketing fundamentals",
            "Practise content writing",
            "Study digital marketing",
            "Learn campaign analytics",
            "Create a sample campaign"
        ]
    }
}


# ---------------- SESSION STATE ----------------
defaults = {
    "student_name": "",
    "subject": "Computer Science",
    "interests": [],
    "skills": [],
    "recommendations": ["Software Developer", "Data Analyst"],
    "aptitude_score": None,
    "chosen_career": "Software Developer",
    "chat_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- CAREER MATCHING ----------------
def recommend_careers(subject, interests, skills):
    scores = {}

    for career, info in CAREERS.items():
        score = 0

        for interest in interests:
            if interest in info["interests"]:
                score += 2

        for skill in skills:
            if skill in info["skills"]:
                score += 1

        if subject == "Computer Science" and career in [
            "Software Developer", "Cybersecurity Analyst"
        ]:
            score += 1

        if subject == "Mathematics" and career in [
            "Data Analyst", "Data Scientist"
        ]:
            score += 1

        if subject == "Commerce" and career in [
            "Business Analyst", "Digital Marketer"
        ]:
            score += 1

        if subject == "Arts and Design" and career == "UI/UX Designer":
            score += 2

        scores[career] = score

    ranked = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    if scores[ranked[0]] == 0:
        return [
            "Software Developer",
            "Data Analyst",
            "UI/UX Designer"
        ]

    return ranked[:3]


# ---------------- PDF REPORT ----------------
def create_pdf():
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    styles["Title"].alignment = TA_CENTER

    story = [
        Paragraph("AI Virtual Career Counsellor", styles["Title"]),
        Spacer(1, 20),

        Paragraph(
            "Student: " + escape(
                st.session_state.student_name or "Student"
            ),
            styles["Normal"]
        ),

        Paragraph(
            "Favourite subject: " + escape(
                st.session_state.subject
            ),
            styles["Normal"]
        ),

        Paragraph(
            "Interests: " + escape(
                ", ".join(st.session_state.interests) or "Not entered"
            ),
            styles["Normal"]
        ),

        Paragraph(
            "Skills: " + escape(
                ", ".join(st.session_state.skills) or "Not entered"
            ),
            styles["Normal"]
        ),

        Spacer(1, 15),
        Paragraph("Recommended Careers", styles["Heading2"])
    ]

    for career in st.session_state.recommendations:
        story.append(
            Paragraph(escape(career), styles["Normal"])
        )

    story.extend([
        Spacer(1, 15),
        Paragraph("Aptitude Test", styles["Heading2"]),
        Paragraph(
            "Score: " + (
                str(st.session_state.aptitude_score) + "/5"
                if st.session_state.aptitude_score is not None
                else "Not completed"
            ),
            styles["Normal"]
        ),
        Spacer(1, 15),
        Paragraph("Selected Learning Roadmap", styles["Heading2"]),
        Paragraph(
            escape(st.session_state.chosen_career),
            styles["Normal"]
        )
    ])

    for step in CAREERS[
        st.session_state.chosen_career
    ]["roadmap"]:
        story.append(
            Paragraph("• " + escape(step), styles["Normal"])
        )

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 Career Counsellor")
st.sidebar.caption("Explore your future")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Career Recommendations",
        "Career Aptitude Test",
        "Learning Roadmap",
        "Career Chatbot",
        "Compare Careers",
        "PDF Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Navy • Slate • Teal")


# ==================================================
# 1. HOME PAGE
# ==================================================
if page == "Home":
    st.title("Welcome to Your Career Journey 🎓")

    st.write(
        "Discover careers, explore your interests, "
        "and build your personal learning roadmap."
    )

    st.info(
        "Explore the options using the sidebar. "
        "Recommendations are suggestions, not guarantees."
    )

    features = [
        (
            "🎯 Career Recommendations",
            "Discover careers matching your interests."
        ),
        (
            "📝 Aptitude Test",
            "Answer five questions about your preferences."
        ),
        (
            "🗺️ Learning Roadmap",
            "Follow career-specific learning steps."
        ),
        (
            "💬 Career Chatbot",
            "Ask common career guidance questions."
        ),
        (
            "⚖️ Compare Careers",
            "Compare skills and education paths."
        ),
        (
            "📄 PDF Report",
            "Create a downloadable career report."
        )
    ]

    cols = st.columns(3)

    for i, (title, description) in enumerate(features):
        with cols[i % 3]:
            st.subheader(title)
            st.write(description)


# ==================================================
# 2. CAREER RECOMMENDATIONS
# ==================================================
elif page == "Career Recommendations":
    st.title("🎯 Career Recommendations")

    st.write(
        "Enter your interests, favourite subject, and skills."
    )

    with st.form("career_form"):
        name = st.text_input(
            "Your name",
            value=st.session_state.student_name
        )

        subject = st.selectbox(
            "Favourite subject",
            [
                "Computer Science",
                "Mathematics",
                "Commerce",
                "Arts and Design",
                "Biology",
                "Other"
            ]
        )

        interests = st.multiselect(
            "Your interests",
            [
                "Coding",
                "Problem Solving",
                "Technology",
                "Data Analysis",
                "Mathematics",
                "Business",
                "Design",
                "Creativity",
                "Communication",
                "Research",
                "Security",
                "Arts"
            ]
        )

        skills = st.multiselect(
            "Your skills or skills you want to learn",
            [
                "Python",
                "Programming",
                "Git",
                "Data Structures",
                "Excel",
                "SQL",
                "Statistics",
                "Machine Learning",
                "Data Visualization",
                "Creativity",
                "Wireframing",
                "Prototyping",
                "Networking",
                "Linux",
                "Communication",
                "Writing",
                "Marketing",
                "Analysis"
            ]
        )

        submit = st.form_submit_button("Recommend Careers")

    if submit:
        st.session_state.student_name = name
        st.session_state.subject = subject
        st.session_state.interests = interests
        st.session_state.skills = skills

        st.session_state.recommendations = recommend_careers(
            subject, interests, skills
        )

    st.subheader("Your Suggested Careers")

    for career in st.session_state.recommendations:
        st.markdown(f"### 🎯 {career}")

        st.write(
            "Important skills: "
            + ", ".join(CAREERS[career]["skills"])
        )

        st.write(
            "Education: " + CAREERS[career]["education"]
        )

        st.markdown("---")


# ==================================================
# 3. CAREER APTITUDE TEST
# ==================================================
elif page == "Career Aptitude Test":
    st.title("📝 Career Aptitude Test")

    st.write(
        "Choose the option you prefer. This is a simple "
        "career-interest quiz, not a formal aptitude assessment."
    )

    questions = [
        (
            "1. Which activity do you enjoy?",
            ["Coding", "Analysing data", "Designing", "Business"]
        ),
        (
            "2. Which task sounds interesting?",
            [
                "Building software",
                "Finding patterns",
                "Drawing designs",
                "Presenting ideas"
            ]
        ),
        (
            "3. Which subject do you prefer?",
            ["Computers", "Mathematics", "Arts", "Commerce"]
        ),
        (
            "4. Which project would you choose?",
            [
                "Create an app",
                "Study a dataset",
                "Design a website",
                "Plan a campaign"
            ]
        ),
        (
            "5. Which strength do you prefer using?",
            [
                "Logical thinking",
                "Analytical thinking",
                "Creativity",
                "Communication"
            ]
        )
    ]

    answer_map = {
        "Coding": "Software Developer",
        "Building software": "Software Developer",
        "Computers": "Software Developer",
        "Create an app": "Software Developer",
        "Logical thinking": "Cybersecurity Analyst",
        "Analysing data": "Data Analyst",
        "Finding patterns": "Data Scientist",
        "Mathematics": "Data Scientist",
        "Study a dataset": "Data Analyst",
        "Analytical thinking": "Data Analyst",
        "Designing": "UI/UX Designer",
        "Drawing designs": "UI/UX Designer",
        "Arts": "UI/UX Designer",
        "Design a website": "UI/UX Designer",
        "Creativity": "UI/UX Designer",
        "Business": "Business Analyst",
        "Presenting ideas": "Digital Marketer",
        "Commerce": "Business Analyst",
        "Plan a campaign": "Digital Marketer",
        "Communication": "Digital Marketer"
    }

    with st.form("aptitude_form"):
        answers = []

        for question, options in questions:
            answer = st.radio(question, options)
            answers.append(answer)

        submitted = st.form_submit_button("Show My Results")

    if submitted:
        counts = {}

        for answer in answers:
            career = answer_map.get(
                answer,
                "Software Developer"
            )
            counts[career] = counts.get(career, 0) + 1

        ranked = sorted(
            counts,
            key=counts.get,
            reverse=True
        )

        st.session_state.aptitude_score = len(answers)
        st.session_state.recommendations = ranked[:3]

        st.success("You completed all five questions!")

        st.subheader("Career Areas to Explore")

        for career in ranked[:3]:
            st.write("🎯 " + career)

        st.caption(
            "Your result reflects your selected preferences. "
            "Explore several options before making a decision."
        )


# ==================================================
# 4. PERSONALIZED LEARNING ROADMAP
# ==================================================
elif page == "Learning Roadmap":
    st.title("🗺️ Personalized Learning Roadmap")

    career_options = list(CAREERS.keys())

    if st.session_state.chosen_career not in career_options:
        st.session_state.chosen_career = "Software Developer"

    career = st.selectbox(
        "Choose your career",
        career_options,
        index=career_options.index(
            st.session_state.chosen_career
        )
    )

    st.session_state.chosen_career = career

    st.subheader(f"Roadmap for {career}")
    st.write("Complete these steps at your own pace.")

    for i, step in enumerate(
        CAREERS[career]["roadmap"],
        start=1
    ):
        st.checkbox(
            f"Step {i}: {step}",
            key=f"roadmap_{career}_{i}"
        )

    st.subheader("Skills to Develop")
    st.write(", ".join(CAREERS[career]["skills"]))

    st.info(
        "Tip: Practise each skill and build a small project "
        "to demonstrate what you have learned."
    )


# ==================================================
# 5. CAREER CHATBOT
# ==================================================
elif page == "Career Chatbot":
    st.title("💬 Career Guidance Chatbot")

    st.write(
        "Ask about careers, skills, education, or learning paths."
    )

    if st.button("Clear Chat"):
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Example: What skills does a Data Analyst need?"
    )

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        text = prompt.lower()
        response = None

        for career, info in CAREERS.items():
            if career.lower() in text:
                response = (
                    f"{career} requires skills such as "
                    f"{', '.join(info['skills'])}. "
                    f"Education: {info['education']}. "
                    f"First step: {info['roadmap'][0]}."
                )
                break

        if response is None:
            if any(
                word in text
                for word in ["salary", "pay", "income"]
            ):
                response = (
                    "Salary depends on location, experience, "
                    "skills, and employer. Check current local "
                    "job listings and reliable salary surveys."
                )

            elif any(
                word in text
                for word in ["skill", "learn", "start"]
            ):
                response = (
                    "Choose a career first, learn its basics, "
                    "practise regularly, and build a project. "
                    "Open Learning Roadmap for step-by-step guidance."
                )

            elif any(
                word in text
                for word in ["confused", "choose", "interest"]
            ):
                response = (
                    "Think about your favourite subjects, "
                    "activities, and skills you want to develop. "
                    "Try the aptitude test and compare career options."
                )

            else:
                response = (
                    "I can provide basic guidance about career "
                    "options, skills, education, and learning paths. "
                    "Try asking about a career listed in the app."
                )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()


# ==================================================
# 6. CAREER COMPARISON DASHBOARD
# ==================================================
elif page == "Compare Careers":
    st.title("⚖️ Career Comparison Dashboard")

    selected = st.multiselect(
        "Choose careers to compare",
        list(CAREERS.keys()),
        default=["Software Developer", "Data Analyst"]
    )

    if selected:
        rows = []

        for career in selected:
            info = CAREERS[career]

            rows.append({
                "Career": career,
                "Skills": ", ".join(info["skills"]),
                "Education": info["education"],
                "First learning step": info["roadmap"][0]
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Listed Skills Comparison")

        chart = pd.DataFrame({
            "Career": selected,
            "Number of Skills": [
                len(CAREERS[career]["skills"])
                for career in selected
            ]
        }).set_index("Career")

        st.bar_chart(chart)

        st.caption(
            "This chart counts skills listed in the demo. "
            "It does not measure salary or job demand."
        )

    else:
        st.info("Select careers to compare.")


# ==================================================
# 7. DOWNLOADABLE PDF REPORT
# ==================================================
elif page == "PDF Report":
    st.title("📄 Download Your Career Report")

    st.write(
        "Generate a PDF containing your profile, "
        "career recommendations, and learning roadmap."
    )

    st.write(
        "Student: "
        + (st.session_state.student_name or "Not entered")
    )

    st.write(
        "Favourite subject: " + st.session_state.subject
    )

    st.write(
        "Interests: "
        + (", ".join(st.session_state.interests) or "Not entered")
    )

    st.write(
        "Skills: "
        + (", ".join(st.session_state.skills) or "Not entered")
    )

    if st.button("Prepare PDF Report"):
        pdf_data = create_pdf()

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name="career_guidance_report.pdf",
            mime="application/pdf"
        )

    st.caption(
        "For a more personalised report, complete the "
        "Career Recommendations and Aptitude Test pages first."
    )
