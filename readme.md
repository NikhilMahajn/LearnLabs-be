# LearnLabs Backend

AI-powered backend API for generating personalized courses, tutorials, and developer roadmaps using LangChain and Groq LLM.

🔗 **Frontend**: [https://learn-labs-fe.vercel.app/](https://learn-labs-fe.vercel.app/)

🔗 **Frontend Repository**: [https://github.com/NikhilMahajn/LearnLabs-fe](https://github.com/NikhilMahajn/LearnLabs-fe)

## Overview

The LearnLabs backend is built with FastAPI and leverages LangChain for AI orchestration and Groq API for high-performance language model inference. It provides RESTful endpoints that generate structured learning content, custom roadmaps, and step-by-step tutorials tailored to any technology or programming topic.

## Features

- **AI Content Generation**: Creates personalized courses and tutorials using advanced LLM models
- **LangChain Integration**: Orchestrates complex AI workflows for structured content generation
- **Groq API**: Utilizes fast LLM inference for real-time content creation
- **RESTful API**: Clean, well-documented endpoints for frontend integration
- **Flexible Learning Paths**: Generates custom roadmaps for various tech stacks and skill levels
- **Scalable Architecture**: Built with FastAPI for high performance and async support

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing LLM-powered applications
- **Groq API**: High-performance LLM inference
- **Python 3.10+**: Core programming language
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running FastAPI

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or poetry
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd learnlabs-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# or if using poetry
poetry install
```

4. Create a `.env` file in the root directory:
```env
DB_URI=your_database_uri_here
GROQ_API_KEY=your_groq_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

5. Run the development server:
```bash
uvicorn main:app --reload
# or
python main.py
```

6. Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive API documentation

## Alembic Commands

Run database migrations:
```bash
alembic revision --autogenerate -m "your migration message"
alembic upgrade head
```

## Project Structure
```
.
├── main.py                          # Application entry point
├── app/
│   ├── router/
│   │   └── apis.py                 # API endpoint modules
│   ├── core/
│   │   ├── config.py               # Settings and environment variables
│   │   └── security.py             # Security utilities
│   ├── models/                     # Pydantic models
│   ├── services/
│   │   ├── Course_generation.py   # Course generation service
│   │   └── roadmap_generation.py  # Roadmap generation service
│   └── utils/                      # Utility functions
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment variables template
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DB_URI` | Database connection string | Yes |
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes |
| `ALGORITHM` | JWT algorithm (default: HS256) | Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration time | Yes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration time | Yes |

## Development

### Running Tests
```bash
pytest
# or with coverage
pytest --cov=app tests/
```

### Code Formatting
```bash
black .
isort .
```

### Linting
```bash
flake8
pylint app/
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [LangChain](https://www.langchain.com/) - LLM orchestration
- [Groq](https://groq.com/) - High-performance LLM inference

---

Built with ❤️ by [Nikhil Mahajan](https://nikhilmahajan.vercel.app)