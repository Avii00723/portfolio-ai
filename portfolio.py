from pathlib import Path
from dotenv import load_dotenv
import os
import json
import re
from time import sleep

from groq import Groq


# ============================================================
# ENVIRONMENT
# ============================================================

# Find .env in week1/
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

my_api_key = os.getenv("Grok_key")

if not my_api_key:
    raise ValueError("API key not found")


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(api_key=my_api_key)

MODEL = "qwen/qwen3.8-27b"

# ============================================================
# 2. PORTFOLIO DATA
# ============================================================

PORTFOLIO = {
    "personal": {
        "name": "Avinash Wagh",
        "location": "Pune, India",
        "email": "wavinash.2003@gmail.com",
    },

    "education": {
        "degree": "B.Tech in Computer Science and Engineering",
        "college": "Indian Institute of Information Technology, Nagpur",
        "duration": "Dec 2021 - Jun 2025",
        "coursework": [
            "Data Structures and Algorithms",
            "Design and Analysis of Algorithms",
            "Object Oriented Programming",
            "Operating Systems",
            "Database Management Systems"
        ]
    },

    "experience": [
        {
            "company": "Softhub Technologies",
            "role": "Flutter Developer Intern",
            "duration": "Feb 2025 - May 2025",
            "skills": [
                "Flutter",
                "Provider",
                "Bloc",
                "REST APIs"
            ],
            "details": [
                "Worked on 4 production Flutter applications.",
                "Implemented RESTful API integrations handling 50K+ daily API calls.",
                "Built responsive UI components across 15+ screen sizes.",
                "Reduced cross-platform compatibility issues by 85%."
            ]
        },

        {
            "company": "Vaali Infotech LLP",
            "role": "Flutter Developer Intern",
            "duration": "Jun 2025 - Nov 2025",
            "skills": [
                "Flutter",
                "REST APIs",
                "Deep Linking",
                "Push Notifications"
            ],
            "details": [
                "Engineered and deployed 3 cross-platform mobile applications.",
                "Published applications to Google Play Store and App Store.",
                "Achieved 1,200+ downloads with 4.3+ star ratings within the first month.",
                "Reduced data loading times by 60%.",
                "Implemented deep linking across 5 app modules.",
                "Configured push notifications.",
                "Improved user retention by 28%."
            ]
        },

        {
            "company": "Centralogic",
            "role": "Software Engineer",
            "duration": "Dec 2025 - Present",
            "skills": [
                "Next.js",
                "React",
                "TypeScript",
                "REST APIs",
                "Jira"
            ],
            "details": [
                "Developed a production-grade Agent DB platform.",
                "Built agent profiles, licensing, pay plans and lifecycle management features.",
                "Implemented Pay Plan CRUD and item/concession management.",
                "Implemented filtering, sorting and validation.",
                "Worked on conditional banners, icons and edit-locks.",
                "Owned features from Jira requirements through implementation, debugging, testing and PR delivery.",
                "Resolved 40+ production bugs.",
                "Delivered 15+ development stories."
            ]
        }
    ],

    "skills": {
        "languages": [
            "C++",
            "Java",
            "Kotlin",
            "Dart",
            "Python",
            "HTML",
            "SQL",
            "C",
            "Golang"
        ],

        "frameworks": [
            "Flutter",
            "React",
            "Django",
            "TensorFlow",
            "Next.js",
            "NestJS",
            "TypeScript"
        ],

        "tools": [
            "Firebase",
            "Git",
            "GitHub",
            "Figma",
            "Canva",
            "Power BI",
            "Tableau",
            "Android Studio",
            "VS Code"
        ]
    },

    "projects": [
        {
            "name": "Financial News-Driven Stock Prediction System",
            "technologies": [
                "Python",
                "FinBERT",
                "TensorFlow"
            ],
            "details": [
                "Combined FinBERT sentiment analysis with technical indicators.",
                "Processed 10K+ financial news articles.",
                "Analyzed 2 years of historical stock data across 50 S&P 500 companies.",
                "Achieved 78.5% accuracy in predicting next-day trading signals."
            ]
        },

        {
            "name": "Real-time Object Detection Mobile App",
            "technologies": [
                "Flutter",
                "TensorFlow Lite",
                "Dart"
            ],
            "details": [
                "Implemented a TensorFlow Lite YOLO model.",
                "Supported 80+ object classes.",
                "Achieved 30+ FPS performance.",
                "Reduced memory usage by 65%.",
                "Reduced battery consumption by 40%."
            ]
        },

        {
            "name": "Food Recipe Web Application",
            "technologies": [
                "React",
                "CSS/SCSS",
                "Material UI",
                "Tailwind CSS"
            ],
            "details": [
                "Built a responsive recipe web application.",
                "Implemented React Router.",
                "Created recipe categories, details and search functionality."
            ]
        },

        {
            "name": "Jobify",
            "technologies": [
                "Next.js",
                "TypeScript",
                "Supabase",
                "Clerk",
                "Prisma",
                "Tailwind CSS"
            ],
            "url": "https://jobify-j9xe0z09w-avii00723s-projects.vercel.app/",
            "details": [
                "Built a full-stack job board and management application.",
                "Implemented authenticated CRUD for job postings.",
                "Built responsive UI and forms.",
                "Implemented Prisma-backed database with seeded data.",
                "Built job listing and detail pages.",
                "Implemented analytics dashboards with charts."
            ]
        },

        {
            "name": "NXT Store",
            "technologies": [
                "Next.js",
                "TypeScript",
                "Clerk",
                "Tailwind CSS",
                "shadcn/ui"
            ],
            "url": "https://nxtstore-three.vercel.app/",
            "details": [
                "Implemented product management.",
                "Built shopping cart and order management.",
                "Built admin dashboard.",
                "Implemented authentication and reviews.",
                "Built responsive UI."
            ]
        },

        {
            "name": "Lucid - Full-Stack Blogging Platform",
            "technologies": [
                "Node.js",
                "Express.js",
                "EJS",
                "MongoDB"
            ],
            "url": "https://blogapp-n-seven.vercel.app/",
            "details": [
                "Built a minimalist blogging platform.",
                "Implemented blog creation and publishing.",
                "Built server-rendered interfaces using EJS.",
                "Used MongoDB for content management."
            ]
        },

        {
            "name": "Classroom Dashboard",
            "technologies": [
                "React",
                "TypeScript",
                "Refine",
                "Express",
                "Drizzle ORM",
                "Neon Postgres",
                "Better-Auth",
                "Arcjet",
                "TanStack Table",
                "Recharts"
            ],
            "url": "https://github.com/Avii00723/classroom-dashboard-frontend",
            "details": [
                "Built a full-stack classroom management dashboard.",
                "Implemented admin, class and subject management.",
                "Used Refine for admin and dashboard functionality.",
                "Used TanStack Table for data tables.",
                "Used Recharts for data visualization.",
                "Built an Express/TypeScript backend.",
                "Used Drizzle ORM with Neon Postgres.",
                "Implemented authentication with Better-Auth.",
                "Used Arcjet for security and rate limiting."
            ]
        }
    ],

    "achievements": [
        "LeetCode rating: 1,395",
        "40+ production bugs resolved",
        "15+ development stories delivered"
    ],

    "leadership": {
        "organization": "Abhivyakti 2023 - IIIT Nagpur Cultural Festival",
        "role": "Content Team Member",
        "details": [
            "Coordinated content strategy and creative direction.",
            "Managed promotional campaigns reaching 5,000+ students across 20+ colleges.",
            "Designed 50+ marketing assets.",
            "Contributed to a 35% increase in event attendance."
        ]
    }
}


# ============================================================
# 3. CONTACT LINKS
# ============================================================

CONTACT_INFO = {
    "email": "wavinash.2003@gmail.com",
    "email_link": "mailto:wavinash.2003@gmail.com",
    "github": "https://github.com/Avii00723",
    "linkedin": "https://www.linkedin.com/in/avinash-wagh-628968239/"
}

# ============================================================
# 4. STEP 1 - UNDERSTAND USER QUESTION
# ============================================================

def analyze_question(question):
    prompt = f"""
You are analyzing a question about Avinash Wagh's portfolio.

Classify the question into ONE of these categories:

- skills
- experience
- projects
- education
- achievements
- contact
- leadership
- general

Question:
{question}

Return ONLY valid JSON:

{{
    "category": "skills",
    "keywords": ["flutter", "react"]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You classify portfolio questions into categories."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_completion_tokens=200
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "category": "general",
            "keywords": []
        }


# ============================================================
# 5. STEP 2 - RETRIEVE RELEVANT INFORMATION
# ============================================================
def retrieve_context(category, question):
    """
    Select only the relevant part of the portfolio.
    """

    if category == "skills":
        return {
            "skills": PORTFOLIO["skills"]
        }

    if category == "experience":
        return {
            "experience": PORTFOLIO["experience"]
        }

    if category == "projects":
        return {
            "projects": PORTFOLIO["projects"]
        }

    if category == "education":
        return {
            "education": PORTFOLIO["education"]
        }

    if category == "achievements":
        return {
            "achievements": PORTFOLIO["achievements"]
        }

    if category == "leadership":
        return {
            "leadership": PORTFOLIO["leadership"]
        }

    if category == "contact":
        return {
            "contact": CONTACT_INFO
        }

    # General question
    return PORTFOLIO


# ============================================================
# 6. STEP 3 - GENERATE STREAMING ANSWER
# ============================================================

def generate_answer(question, context):

    system_prompt = """
You are Avinash Wagh's portfolio assistant.

Answer questions about Avinash using ONLY the provided portfolio
information.

Rules:
- Never invent information.
- Never claim Avinash knows a technology unless it appears in the data.
- Never invent projects or experience.
- Be concise but useful.
- If the information is unavailable, clearly say that it is not
  available in the portfolio.
- If discussing a project, mention the technologies and important
  implementation details when relevant.
- For contact questions, provide the available contact links.
"""

    user_prompt = f"""
Portfolio information:

{json.dumps(context, indent=2)}

User question:
{question}

Answer the user's question naturally.
"""

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=500,
        stream=True
    )

    full_response = ""

    for chunk in stream:

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            full_response += content

    print()

    return full_response


# ============================================================
# 7. COMPLETE CHATBOT PIPELINE
# ============================================================

def chatbot(question):

    print("\nAnalyzing question...\n")

    # Step 1
    analysis = analyze_question(question)

    category = analysis.get("category", "general")

    print(f"Category: {category}")

    # Step 2
    context = retrieve_context(
        category,
        question
    )

    # Step 3
    print("\nAvinash's Portfolio Assistant:\n")

    answer = generate_answer(
        question,
        context
    )

    return answer


# ============================================================
# 8. CHAT LOOP
# ============================================================

def main():

    print("=" * 60)
    print("Avinash Wagh - Portfolio Assistant")
    print("=" * 60)

    print("\nAsk me anything about Avinash's:")
    print("- Skills")
    print("- Experience")
    print("- Projects")
    print("- Education")
    print("- Achievements")
    print("- Contact information")

    print("\nType 'exit' to quit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        if not question:
            continue

        try:
            chatbot(question)

        except Exception as e:
            print(f"\nError: {e}")


# ============================================================
# 9. RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    main()