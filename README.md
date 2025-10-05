# 🔍 StartupScout

**AI-Powered Startup Validation Platform**
*Built for FutureStack Hackathon 2025*

Validate your startup ideas in under 5 minutes with ultra-fast AI agents powered by Cerebras inference, Meta's Llama 4 Maverick, and Docker MCP toolkit.

---

## 📋 Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Features](#features)
- [Docker MCP Integration](#docker-mcp-integration)
- [Project Structure](#project-structure)
- [Configuration](#configuration)

---

## 🎯 Overview

**The Problem:**
Indie hackers and entrepreneurs have countless ideas but lack the time and resources to validate each one properly. Traditional market research takes weeks and requires expensive consultants.

**Our Solution:**
StartupScout is an AI-powered validation platform that analyzes startup ideas in minutes, not weeks. Using 6 specialized AI agents working in parallel, we deliver comprehensive market research, competitor analysis, and customer insights—all powered by cutting-edge AI infrastructure.

**Key Value Proposition:**
- ⚡ **5-minute validation** vs 2-4 weeks traditional research
- 🧠 **6 AI specialists** analyzing different aspects simultaneously
- 💰 **Free/low-cost** vs $5,000-$20,000 consulting fees
- 📊 **Data-driven insights** from real web sources, Reddit, GitHub

---

## 🔄 How It Works

### 1. **Idea Submission**
User enters their startup concept through the web interface.

### 2. **AI Validation & Refinement**
The Research Manager agent refines the idea, identifying:
- Core problem statement
- Target users
- Unique value proposition
- Product concept

### 3. **Parallel Research (6 Agents)**

**Team 1 - Initial Research:**
- 🔍 **Market Analyst** - Market size, growth trends, TAM/SAM/SOM
- 🏢 **Competitor Scout** - Existing solutions, competitive landscape
- 👥 **Customer Researcher** - Pain points from Reddit/forums
- 💻 **Online Trends Analyst** - Current trends, timing validation

**Team 2 - Output Generation:**
- 📝 **Executive Summarizer** - Comprehensive validation report
- 🎙️ **Podcast Generator** - Audio summary of findings

### 4. **Real-Time Dashboard**
Users watch agents work through an interactive dashboard showing:
- Agent status (pending → running → completed)
- Current tasks and progress
- Live results streaming

### 5. **Comprehensive Report**
Final deliverables include:
- Market opportunity assessment
- Competitive landscape analysis
- Customer insights and pain points
- Technical feasibility evaluation
- Go/no-go recommendation

---

## 🛠️ Tech Stack

### **AI Infrastructure**

#### Cerebras Cloud + Llama 4 Maverick
- **Model:** `llama-4-maverick-17b-128e-instruct`
- **Architecture:** 128-expert Mixture-of-Experts (MoE)
- **Inference Speed:** 2000+ tokens/sec (20-40x faster than GPT-4)
- **Context Window:** 1 million tokens
- **Time to First Token:** <50ms

**Why Cerebras + Llama 4?**
- Ultra-fast parallel agent execution
- Massive context for maintaining research history
- Advanced reasoning for complex market analysis
- Cost-effective at scale

#### LlamaIndex Framework
- Workflow orchestration
- Agent coordination
- Tool integration
- Streaming responses

### **Backend**

```
Python 3.11 + FastAPI
├── Poetry (dependency management)
├── LlamaIndex (agent framework)
├── Cerebras SDK (inference)
├── AsyncIO (concurrent execution)
└── Server-Sent Events (real-time streaming)
```

**Key Libraries:**
- `cerebras-cloud-sdk` - AI inference
- `llama-index` - Agent orchestration
- `fastapi` - REST API
- `httpx` - Async HTTP client
- `tavily-python` - Web search
- `firecrawl-py` - Web scraping

### **Frontend**

```
Next.js 14 + React + TypeScript
├── Tailwind CSS (styling)
├── Framer Motion (animations)
├── Zustand (state management)
└── AI SDK (streaming)
```

### **Docker MCP Integration**

```
Docker Compose
├── DuckDuckGo MCP (port 8081) - Web search
├── Fetch MCP (port 8082) - URL extraction
├── Notion MCP (port 8084) - Documentation
└── MCP Gateway (port 9000) - Orchestration
```

**Additional APIs:**
- Brave Search API - Enhanced web research
- Reddit OAuth API - Community insights
- GitHub API - Technical analysis

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────┐
│           Frontend (Next.js + React)            │
│                                                  │
│  ┌────────────────────────────────────────────┐│
│  │  Real-Time Dashboard                       ││
│  │  • Agent status cards                      ││
│  │  • Progress tracking                       ││
│  │  • Live results streaming                  ││
│  └────────────────────────────────────────────┘│
└──────────────────────┬──────────────────────────┘
                       │ SSE Stream
                       ▼
┌─────────────────────────────────────────────────┐
│        Backend (FastAPI + LlamaIndex)           │
│                                                  │
│  ┌────────────────────────────────────────────┐│
│  │  Cerebras + Llama 4 Maverick               ││
│  │  • 2000+ tokens/sec inference              ││
│  │  • 1M token context window                 ││
│  │  • 128-expert MoE architecture             ││
│  │  • Real-time streaming                     ││
│  └────────────────────────────────────────────┘│
│                                                  │
│  ┌────────────────────────────────────────────┐│
│  │  Multi-Agent Workflow                      ││
│  │                                            ││
│  │  Team 1 (Research):                        ││
│  │  ├─ Market Analyst                         ││
│  │  ├─ Competitor Scout                       ││
│  │  ├─ Customer Researcher                    ││
│  │  └─ Online Trends Analyst                  ││
│  │                                            ││
│  │  Team 2 (Output):                          ││
│  │  ├─ Executive Summarizer                   ││
│  │  └─ Podcast Generator                      ││
│  └────────────────────────────────────────────┘│
│                                                  │
│  ┌────────────────────────────────────────────┐│
│  │  Research Tools & MCP                      ││
│  │                                            ││
│  │  Direct APIs:                              ││
│  │  • Brave Search → Web research             ││
│  │  • Reddit API → Community insights         ││
│  │  • GitHub API → Technical analysis         ││
│  │  • Tavily → Market data                    ││
│  │  • Firecrawl → Web scraping                ││
│  └────────────────────────────────────────────┘│
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│         Docker MCP Services                      │
│                                                  │
│  ├─ DuckDuckGo MCP (8081) → Web search          │
│  ├─ Fetch MCP (8082) → URL extraction           │
│  ├─ Notion MCP (8084) → Documentation           │
│  └─ Gateway (9000) → Service orchestration      │
└─────────────────────────────────────────────────┘
```

### Agent Workflow

```
User Input
    ↓
┌─────────────────┐
│ Research Manager│ ← Refines idea, validates concept
└────────┬────────┘
         ↓
    [Parallel Execution - Team 1]
         ↓
    ┌────┴────┬────────┬──────────┐
    ↓         ↓        ↓          ↓
┌─────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│ Market  │ │Compet│ │Customer│ │Trends  │
│Analyst  │ │Scout │ │Research│ │Analyst │
└────┬────┘ └──┬───┘ └───┬────┘ └───┬────┘
     │         │         │          │
     └─────────┴─────────┴──────────┘
                   ↓
           [Aggregated Research]
                   ↓
         ┌─────────┴─────────┐
         ↓                   ↓
    ┌─────────┐         ┌─────────┐
    │Executive│         │Podcast  │
    │Summary  │         │Generator│
    └────┬────┘         └────┬────┘
         │                   │
         └─────────┬─────────┘
                   ↓
           [Final Deliverables]
                   ↓
              User Dashboard
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11
- Node.js 18+
- Docker Desktop
- Poetry

### Installation

**1. Clone & Setup Environment**

```bash
# Backend
cd backend
cp .env.example .env

# Add your API keys to .env:
# - CEREBRAS_API_KEY (required)
# - BRAVE_API_KEY (optional)
# - REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET (optional)
# - GITHUB_TOKEN (optional)
```

**2. Install Dependencies**

```bash
# Backend
cd backend
poetry install

# Frontend
cd ../frontend
npm install
```

**3. Start Docker MCP Services**

```bash
docker compose up -d
```

**4. Run Application**

```bash
# Terminal 1 - Backend
cd backend
poetry run python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**5. Access Application**

- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8000/docs
- **MCP Gateway:** http://localhost:9000

---

## ✨ Features

### **Ultra-Fast AI Processing**
- 2000+ tokens/sec with Cerebras inference
- 20-40x faster than traditional LLMs
- Sub-50ms time to first token
- Real-time streaming responses

### **Multi-Agent Research System**
- 6 specialized AI agents
- Parallel execution
- Coordinated workflows
- Comprehensive analysis

### **Docker MCP Integration**
- 4 official MCP services running
- DuckDuckGo, Fetch, Notion, Gateway
- Async concurrent execution
- Tool isolation & standardization

### **Rich Data Sources**
- Brave Search - Web research
- Reddit API - Community insights
- GitHub API - Technical analysis
- Tavily - Market intelligence
- Firecrawl - Deep web scraping

### **Modern UI/UX**
- Real-time agent dashboard
- Live progress tracking
- Gradient glassmorphism design
- Mobile-responsive interface

---

## 🐳 Docker MCP Integration

### Running Services

```bash
$ docker ps
```

| Container | Status | Port | Purpose |
|-----------|--------|------|---------|
| **duckduckgo-mcp** | Running | 8081 | Web search |
| **fetch-mcp** | Running | 8082 | URL extraction |
| **notion-mcp** | Running | 8084 | Documentation |
| **mcp-gateway** | Running | 9000 | Orchestration |

### Implementation Details

**High-Concurrency Architecture:**
- 6 agents make concurrent MCP requests
- 10+ simultaneous tool calls during peak research
- Async I/O patterns prevent blocking
- Enables 5-minute validation vs 30+ minutes sequential

**Tool Integration:**
```python
# Example: Agent using MCP tools
mcp_tools = create_mcp_tools()  # DuckDuckGo, Fetch, etc.
agent = FunctionCallingAgent(
    tools=[
        market_search,     # Tavily API
        web_search,        # Brave/DuckDuckGo MCP
        reddit_search,     # Reddit API
        github_search,     # GitHub API
        read_webpage,      # Fetch MCP
    ]
)
```

**docker-compose.yml:**
```yaml
services:
  duckduckgo-mcp:
    image: mcp/duckduckgo:latest
    ports: ["8081:3000"]

  fetch-mcp:
    image: mcp/fetch:latest
    ports: ["8082:3000"]

  notion-mcp:
    image: mcp/notion:latest
    ports: ["8084:3000"]

  mcp-gateway:
    image: mcp/docker:latest
    ports: ["9000:8080"]
```

---

## 📁 Project Structure

```
startupscout/
├── backend/
│   ├── app/
│   │   ├── agents/              # 6 specialized AI agents
│   │   ├── engine/
│   │   │   ├── llms/            # Cerebras LLM integration
│   │   │   └── tools/           # MCP & API tools
│   │   ├── workflows/           # LlamaIndex workflows
│   │   └── settings.py          # Cerebras configuration
│   ├── main.py                  # FastAPI server
│   ├── pyproject.toml           # Poetry dependencies
│   └── .env                     # API keys
│
├── frontend/
│   ├── app/
│   │   ├── components/          # React components
│   │   ├── page.tsx             # Main dashboard
│   │   └── globals.css          # Tailwind + custom styles
│   ├── package.json             # npm dependencies
│   └── .env                     # Frontend config
│
├── docker-compose.yml           # MCP services
└── README.md                    # This file
```

---

## 🔧 Configuration

### Required Environment Variables

**Backend (.env):**
```bash
# Cerebras (Required)
CEREBRAS_API_KEY=your_key_here
MODEL_PROVIDER=cerebras
MODEL=llama-4-maverick-17b-128e-instruct

# OpenAI (for embeddings)
OPENAI_API_KEY=your_key_here
EMBEDDING_MODEL=text-embedding-3-large
```

### Optional API Keys

**Enhanced Research:**
```bash
# Web Search
BRAVE_API_KEY=your_brave_key
TAVILY_API_KEY=your_tavily_key

# Community Insights
REDDIT_CLIENT_ID=your_reddit_id
REDDIT_CLIENT_SECRET=your_reddit_secret

# Technical Analysis
GITHUB_TOKEN=your_github_token

# Documentation
NOTION_TOKEN=your_notion_token
```

---

**Made with ❤️ for FutureStack Hackathon 2025**

🚀 **StartupScout** - Validate ideas at the speed of thought
