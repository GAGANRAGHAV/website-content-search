"use client";
import { useState } from "react";

interface SearchResult {
  content: string;
  relevance_score: number;
  chunk_id: string;
}

interface SearchResponse {
  url: string;
  query: string;
  total_matches: number;
  results: SearchResult[];
  error?: string;
}

export default function Home() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searchInfo, setSearchInfo] = useState<{url: string, query: string, total: number} | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);
    setSearchInfo(null);
    setError(null);
    
    try {
      const res = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, query }),
      });
      
      const data: SearchResponse = await res.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data.results || []);
        setSearchInfo({
          url: data.url,
          query: data.query,
          total: data.total_matches
        });
      }
    } catch (err) {
      setError("Failed to connect to the server. Please try again.");
      console.error(err);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-black tracking-tight flex flex-col items-center justify-center p-6 font-sans ">
      <h1 className="text-3xl font-bold mb-6">Website Content Search</h1>
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-lg p-6 w-full max-w-md"
      >
        <label className="block mb-4">
          <span className="text-gray-700">Website URL</span>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="mt-1 block w-full border rounded p-2"
            required
          />
        </label>
        <label className="block mb-4">
          <span className="text-gray-700">Search Query</span>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search something..."
            className="mt-1 block w-full border rounded p-2"
            required
          />
        </label>
        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      <div className="mt-8 w-full max-w-4xl">
        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex">
              <div className="text-red-600">
                <h3 className="text-sm font-medium">Error</h3>
                <p className="text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Search Info */}
        {searchInfo && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h2 className="text-lg font-semibold text-blue-900 mb-2">
              Search Results ({searchInfo.total} matches found)
            </h2>
            <p className="text-sm text-blue-700">
              <strong>URL:</strong> <span className="break-all">{searchInfo.url}</span>
            </p>
            <p className="text-sm text-blue-700">
              <strong>Query:</strong> "{searchInfo.query}"
            </p>
          </div>
        )}

        {/* Results Grid */}
        {results.length > 0 && (
          <div className="grid gap-4">
            {results.map((result, idx) => (
              <div
                key={result.chunk_id}
                className="bg-white shadow-md rounded-lg p-6 border border-gray-200 hover:shadow-lg transition-shadow"
              >
                {/* Result Header */}
                <div className="flex justify-between items-center mb-3">
                  <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    Result #{idx + 1}
                  </span>
                  <span className="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    Relevance: {(result.relevance_score * 100).toFixed(1)}%
                  </span>
                </div>
                
                {/* Content */}
                <div className="text-gray-800">
                  <p className="leading-relaxed whitespace-pre-wrap break-words">
                    {result.content}
                  </p>
                </div>
                
                {/* Chunk ID (for debugging) */}
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <span className="text-xs text-gray-500">
                    Chunk ID: {result.chunk_id}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* No Results Message */}
        {searchInfo && results.length === 0 && !error && (
          <div className="text-center py-8">
            <p className="text-gray-500">No relevant content found for your search query.</p>
          </div>
        )}
      </div>
    </div>
  );
}
