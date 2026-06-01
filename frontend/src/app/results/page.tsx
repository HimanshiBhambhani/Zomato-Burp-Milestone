"use client";
import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "@/components/Navbar";
import FiltersSidebar from "@/components/FiltersSidebar";
import RestaurantCard from "@/components/RestaurantCard";

interface Recommendation {
  name: string;
  cuisine: string;
  rating: number;
  priceRange: string;
  aiInsight: string;
  imageUrl?: string;
}

// Mock data for initial render (shown if API not available)
const MOCK_RESULTS: Recommendation[] = [
  {
    name: "Olive Bar & Kitchen",
    cuisine: "Italian, Mediterranean",
    rating: 4.6,
    priceRange: "₹2500 for two • Fine Dining",
    aiInsight:
      "Top match for Italian cuisine in New Delhi. Known for wood-fired pizzas, handmade pastas, and a beautiful Mediterranean-style courtyard setting.",
    imageUrl: "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400&h=300&fit=crop",
  },
  {
    name: "Tonino",
    cuisine: "Italian, Pizza",
    rating: 4.5,
    priceRange: "₹1800 for two • Casual Fine",
    aiInsight:
      "Authentic Italian by a native chef. Strong on budget and rating criteria. Their truffle pasta and tiramisu are city-famous.",
    imageUrl: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop",
  },
  {
    name: "Diva - The Italian Restaurant",
    cuisine: "Italian, Continental",
    rating: 4.4,
    priceRange: "₹2200 for two • Fine Dining",
    aiInsight:
      "Award-winning Italian dining by Chef Ritu Dalmia. Seasonal menu with locally sourced ingredients. Perfect for a special evening.",
    imageUrl: "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&h=300&fit=crop",
  },
];

export default function ResultsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#1a1a3e]" />}>
      <ResultsContent />
    </Suspense>
  );
}

function ResultsContent() {
  const searchParams = useSearchParams();
  const [results, setResults] = useState<Recommendation[]>(MOCK_RESULTS);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    location: searchParams.get("location") || "New Delhi",
    budget: searchParams.get("budget") || "Mid",
    cuisine: searchParams.get("cuisine") || "Italian",
    rating: searchParams.get("rating") || "4.5",
  });

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
  };

  const handleSearch = async (overrideFilters?: typeof filters) => {
    const searchFilters = overrideFilters || filters;
    // Update UI state if override filters were passed (e.g. "Show All")
    if (overrideFilters) {
      setFilters(overrideFilters);
    }
    setLoading(true);
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(searchFilters),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.recommendations && data.recommendations.length > 0) {
          setResults(
            data.recommendations.map((r: any) => ({
              name: r.name || r.restaurant_name,
              cuisine: r.cuisine || r.cuisines || "",
              rating: r.rating || r.aggregate_rating || 0,
              priceRange: r.price_range || `₹${r.average_cost_for_two} for two`,
              aiInsight: r.ai_insight || r.explanation || "A great match for your preferences.",
              imageUrl: r.image_url || undefined,
            }))
          );
        } else {
          setResults([]);
        }
      } else {
        // API error - show empty state
        setResults(MOCK_RESULTS);
      }
    } catch (e) {
      console.log("Using mock data (API not available)");
      // Keep mock results as fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const clearFilters = () => {
    setFilters({ location: "", budget: "", cuisine: "", rating: "" });
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#1a1a3e]">
      <Navbar />

      <div className="flex flex-1">
        {/* Sidebar */}
        <FiltersSidebar
          filters={filters}
          onChange={handleFilterChange}
          onSearch={handleSearch}
          mode="full"
        />

        {/* Main Content */}
        <main className="flex-1 px-8 py-6 overflow-y-auto">
          <h2 className="text-2xl font-extrabold text-white mb-4">Your AI Matches</h2>

          {/* Active Filters Pills */}
          <div className="flex items-center gap-2 flex-wrap mb-6">
            <span className="text-xs text-[#b8b8d8] uppercase font-medium">FILTERS:</span>
            {filters.location && (
              <span className="px-3 py-1 text-xs bg-[#3a3a6e] text-white rounded-full">
                {filters.location}
              </span>
            )}
            {filters.budget && (
              <span className="px-3 py-1 text-xs bg-[#3a3a6e] text-white rounded-full">
                {filters.budget} Budget
              </span>
            )}
            {filters.cuisine && (
              <span className="px-3 py-1 text-xs bg-[#3a3a6e] text-white rounded-full">
                {filters.cuisine}
              </span>
            )}
            {filters.rating && (
              <span className="px-3 py-1 text-xs bg-[#3a3a6e] text-white rounded-full">
                {filters.rating}+★
              </span>
            )}
            <button
              onClick={clearFilters}
              className="px-3 py-1 text-xs text-[#d4619b] border border-[#d4619b]/40 rounded-full hover:bg-[#d4619b]/10 transition"
            >
              Clear Filters
            </button>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-16">
              <div className="w-12 h-12 border-4 border-[#d4619b] border-t-transparent rounded-full animate-spin mb-4" />
              <p className="text-lg font-bold text-white">Analyzing the Scene</p>
              <p className="text-sm text-[#b8b8d8]">Finding your perfect matches...</p>
            </div>
          )}

          {/* Results */}
          {!loading && results.length > 0 && (
            <div className="space-y-4">
              {results.map((r) => (
                <RestaurantCard key={r.name} {...r} />
              ))}
            </div>
          )}

          {/* Empty State */}
          {!loading && results.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16">
              <div className="w-20 h-20 rounded-full bg-[#232352] border border-[#3a3a6e] flex items-center justify-center mb-4">
                <span className="text-3xl">🔍</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">
                WE COULDN&apos;T FIND THAT SPECIFIC VIBE
              </h3>
              <p className="text-sm text-[#b8b8d8] mb-4">
                No matches for: {filters.location} • {filters.budget} Budget • {filters.cuisine} • {filters.rating}+★
              </p>
              <button
                onClick={clearFilters}
                className="px-6 py-2.5 bg-[#d4619b] text-white text-sm font-semibold rounded-full hover:brightness-110 transition"
              >
                Try Different Filters
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
