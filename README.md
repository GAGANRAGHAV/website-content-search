# Website Content Search

A full-stack web application that enables intelligent content search within any website using vector embeddings and semantic similarity. The application fetches content from a provided URL, processes it into chunks, stores vector embeddings in Pinecone, and provides semantic search capabilities.

## 🌟 Features

- **URL Content Extraction**: Automatically fetches and processes content from any public website
- **Intelligent Text Processing**: Cleans HTML content and chunks text for optimal processing
- **Vector Embeddings**: Uses advanced language models to create semantic embeddings
- **Semantic Search**: Find relevant content using natural language queries
- **Real-time Results**: Fast search with relevance scoring
- **Modern UI**: Clean, responsive React interface with Tailwind CSS
- **Scalable Backend**: FastAPI-powered REST API with async support

## 🏗️ Architecture

```
Frontend (Next.js + React)  ←→  Backend (FastAPI)  ←→  Pinecone Vector Database
```

### Tech Stack

**Frontend:**
- Next.js 15.5.4 with Turbopack
- React 19.1.0
- TypeScript
- Tailwind CSS 4
- ESLint for code quality

**Backend:**
- FastAPI (Python)
- Pinecone Vector Database
- Transformers
- BeautifulSoup for HTML parsing


## 📁 Project Structure

```
├── frontend/                 # Next.js React application
│   ├── app/
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout component
│   │   └── page.tsx         # Main search interface
│   ├── public/              # Static assets
│   ├── package.json
│   └── tsconfig.json
├── server/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py          # FastAPI application entry
│   │   ├── routes.py        # API route handlers
│   │   ├── config.py        # Environment configuration
│   │   ├── helpers.py       # Utility functions
│   │   └── pinecone_client.py # Pinecone database client
│   └── .env                 # Environment variables
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Pinecone account and API key

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd assignment
   ```

2. **Backend Setup**
   ```bash
   cd server
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install fastapi uvicorn python-dotenv pinecone-client transformers beautifulsoup4 requests torch
   ```

3. **Environment Variables**
   Create a `.env` file in the `server` directory:
   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=smartercodes143
   EMBED_MODEL=llama-text-embed-v2
   PINECONE_ENV=gcp-starter
   FRONTEND_ORIGIN=http://localhost:3000
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd server
   uvicorn main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm run dev
   ```
   The application will be available at `http://localhost:3000`

## 🔧 API Endpoints

### POST `/search`
Performs semantic search on website content.

**Request Body:**
```json
{
  "url": "https://example.com",
  "query": "your search query"
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "query": "your search query",
  "total_matches": 5,
  "results": [
    {
      "content": "relevant text content...",
      "relevance_score": 0.95,
      "chunk_id": "unique-chunk-id"
    }
  ]
}
```

### GET `/`
Health check endpoint that returns API status.

## 🎯 How It Works

1. **Content Fetching**: When a URL is provided, the system fetches the webpage content
2. **Text Processing**: HTML is cleaned and converted to plain text, then chunked into manageable pieces
3. **Vectorization**: Each text chunk is converted into vector embeddings using transformer models
4. **Storage**: Vectors are stored in Pinecone with metadata including the original text and URL
5. **Search**: User queries are converted to vectors and compared against stored embeddings
6. **Results**: Most relevant chunks are returned with similarity scores

## 🛠️ Key Components

### Frontend Components
- **Search Interface**: Input form for URL and search query
- **Results Display**: Formatted search results with relevance scores
- **Loading States**: User feedback during processing
- **Error Handling**: Graceful error message display

### Backend Services
- **Content Extraction**: HTML parsing and text cleaning
- **Text Chunking**: Intelligent text segmentation
- **Vector Embeddings**: Semantic representation generation
- **Database Operations**: Pinecone vector storage and retrieval
- **Search Logic**: Query processing and result ranking

## 🔍 Usage Example

1. Enter a website URL (e.g., `https://docs.python.org`)
2. Enter your search query (e.g., "list comprehensions")
3. Click "Search" to process and search the content
4. View relevant content chunks with similarity scores

## 🧪 Development

### Scripts

**Frontend:**
- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

**Backend:**
- `uvicorn main:app --reload` - Start development server with auto-reload
- `python -m pytest` - Run tests (if test suite is added)


---

**Built with ❤️ for intelligent content discovery**