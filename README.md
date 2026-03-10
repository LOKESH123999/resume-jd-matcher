# Resume-Job Description Matcher

AI-powered tool to analyze how well your resume matches job descriptions using advanced NLP and Groq LLM.

## 🚀 Features

- **Smart Matching**: TF-IDF + cosine similarity for accurate skill matching
- **AI Insights**: Groq LLM provides personalized career recommendations
- **Skill Analysis**: Identifies matched and missing skills with visual feedback
- **Learning Resources**: Free courses and resources for skill gaps
- **History Tracking**: Save and review previous analyses
- **Modern UI**: Responsive Bootstrap 5 design with smooth animations

## 📋 Prerequisites

- Python 3.8+
- Groq API key (free at [groq.com](https://groq.com))
- Git

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd resume-job-matcher
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Frontend Setup

```bash
# Navigate to frontend (from root)
cd frontend

# Frontend is static - no setup needed!
# All files are ready to use
```

### 4. Run the Application

#### Option A: Backend Only (Recommended for Development)

```bash
# In backend folder (with venv activated)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open: http://localhost:8000

#### Option B: Separate Backend + Frontend

```bash
# Terminal 1: Backend (in backend folder)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (in frontend folder)
# Using Python's built-in server
python -m http.server 3000

# Or using Node.js live-server (if installed)
npx live-server --port=3000
```

Then open: http://localhost:3000

## 🧪 Testing Guide

### Sample Resume Text

```
John Doe
Software Engineer | Python Developer
Email: john.doe@email.com | Phone: +91 9876543210

SUMMARY
Experienced Python developer with 3 years of expertise in web development, 
machine learning, and cloud technologies. Proficient in Django, React, and AWS.

EXPERIENCE
Software Engineer | Tech Corp | 2021-Present
- Developed REST APIs using Django and FastAPI
- Built responsive web applications with React and JavaScript
- Implemented machine learning models using scikit-learn and TensorFlow
- Deployed applications on AWS EC2 and Docker containers

Junior Developer | StartupXYZ | 2020-2021
- Assisted in full-stack development using Python and JavaScript
- Worked on database design and optimization with PostgreSQL
- Participated in agile development and code reviews

EDUCATION
B.Tech Computer Science | XYZ University | 2016-2020
- CGPA: 8.5/10
- Relevant coursework: Data Structures, Algorithms, Machine Learning

SKILLS
Programming: Python, JavaScript, SQL, HTML/CSS
Frameworks: Django, Flask, React, Node.js
Databases: PostgreSQL, MongoDB, Redis
Cloud: AWS, Docker, Git
ML/AI: scikit-learn, TensorFlow, Pandas, NumPy
```

### Sample Job Description

```
Senior Python Developer | FinTech Solutions
Location: Bangalore | Remote: Hybrid

We are seeking a talented Senior Python Developer to join our growing team.

RESPONSIBILITIES
- Design and develop scalable backend systems using Python and Django
- Build RESTful APIs and microservices architecture
- Implement machine learning solutions for financial data analysis
- Lead code reviews and mentor junior developers
- Collaborate with frontend team for seamless integration

REQUIREMENTS
- 4+ years of Python development experience
- Strong experience with Django, Flask, or FastAPI
- Proficiency in React or Angular for frontend integration
- Experience with AWS cloud services and deployment
- Knowledge of machine learning frameworks (scikit-learn, TensorFlow)
- Strong database skills (PostgreSQL, MongoDB)
- Experience with Docker and containerization
- Understanding of DevOps practices and CI/CD pipelines

PREFERRED QUALIFICATIONS
- Experience with financial systems or FinTech
- Knowledge of blockchain technologies
- Familiarity with Kubernetes
- Strong problem-solving and communication skills

BENEFITS
- Competitive salary and stock options
- Flexible work arrangements
- Professional development budget
- Health insurance and wellness programs
```

### Testing Steps

1. **Start the Backend**
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the Application**
   - Open http://localhost:8000 in your browser
   - You should see the Resume Matcher interface

3. **Test API Health**
   - Visit http://localhost:8000/docs for Swagger documentation
   - Check http://localhost:8000/health for status

4. **Run Analysis**
   - Copy the sample resume text into the "Resume Text" textarea
   - Copy the sample job description into the "Job Description" textarea
   - Click "Analyze Match"
   - Wait for the analysis to complete (30-60 seconds)

5. **Verify Results**
   - Check the overall fit score (should be Medium-High)
   - Review matched skills (Python, Django, React, AWS, etc.)
   - Review missing skills (Angular, Kubernetes, etc.)
   - Read AI feedback and learning resources

6. **Test History**
   - Scroll down to the History section
   - Verify your analysis appears in the list
   - Test "View Details" and "Delete" functionality

### Expected Results

With the sample data above, you should see:
- **Overall Score**: 65-75% (Medium-High)
- **Matched Skills**: Python, Django, React, AWS, scikit-learn, etc.
- **Missing Skills**: Angular, Kubernetes, blockchain, etc.
- **AI Feedback**: Personalized recommendations for missing skills

## 🔧 Troubleshooting

### Common Issues

1. **Groq API Key Error**
   ```
   Error: Invalid Groq API key
   ```
   **Solution**: Ensure your `.env` file contains a valid GROQ_API_KEY

2. **Port Already in Use**
   ```
   Error: Port 8000 is already in use
   ```
   **Solution**: Change port or kill existing process:
   ```bash
   # Find process using port 8000
   netstat -ano | findstr :8000
   # Kill process (replace PID)
   taskkill /PID <PID> /F
   ```

3. **NLTK Download Issues**
   ```
   Error: Resource punkt not found
   ```
   **Solution**: Run Python and download manually:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

4. **CORS Errors**
   ```
   Error: CORS policy blocked request
   ```
   **Solution**: Backend CORS is configured for all origins in development

### Debug Mode

For debugging, run with verbose logging:
```bash
uvicorn app.main:app --reload --log-level debug --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
resume-job-matcher/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # Database connection
│   │   ├── services/            # Business logic
│   │   │   ├── nlp_service.py   # NLP processing
│   │   │   ├── llm_service.py   # Groq AI integration
│   │   │   └── matcher_service.py # Core matching logic
│   │   ├── api/
│   │   │   └── endpoints.py     # API routes
│   │   └── utils.py             # Helper functions
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── Railway.toml            # Deployment config
├── frontend/
│   ├── index.html              # Main web page
│   ├── css/
│   │   └── style.css           # Custom styling
│   ├── js/
│   │   └── main.js             # Frontend JavaScript
│   └── assets/
│       └── favicon.ico         # Site icon
└── README.md                   # This file
```

## 🚀 Next Steps

After successful local testing:

1. **Environment Setup** - Configure production variables
2. **Deployment** - Deploy to Railway (backend) + Netlify (frontend)
3. **Resume Enhancement** - Add this project to your resume

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API docs at http://localhost:8000/docs
3. Verify your Groq API key is valid and has credits

---

**Built with ❤️ using FastAPI, Bootstrap 5, scikit-learn, and Groq AI**
