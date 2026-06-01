"use client";

interface RestaurantCardProps {
  name: string;
  cuisine: string;
  rating: number;
  priceRange: string;
  aiInsight: string;
  imageUrl?: string;
}

export default function RestaurantCard({
  name,
  cuisine,
  rating,
  priceRange,
  aiInsight,
  imageUrl,
}: RestaurantCardProps) {
  return (
    <div className="bg-[#232352] rounded-2xl overflow-hidden border border-[#3a3a6e]/30 flex flex-row hover:border-[#d4619b]/30 transition-all">
      {/* Image Area */}
      <div className="w-52 h-48 shrink-0 relative overflow-hidden">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-[#3a1a4a] to-[#1a2a4a] flex items-center justify-center">
            <span className="text-5xl">🍽️</span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent to-[#232352]/20" />
      </div>

      {/* Content */}
      <div className="flex-1 p-5">
        <div className="flex items-start justify-between mb-2">
          <div>
            <h3 className="text-lg font-bold text-white">{name}</h3>
            <p className="text-xs font-semibold text-[#a4d65e] uppercase tracking-wide">{cuisine}</p>
          </div>
          <span className="px-2.5 py-1 text-xs font-bold bg-[#a4d65e] text-[#1a1a3e] rounded-full">
            {rating.toFixed(1)}
          </span>
        </div>

        <p className="text-xs text-[#b8b8d8] mb-3">{priceRange}</p>

        {/* AI Insight */}
        <div className="bg-[#1a1a3e]/60 border border-[#3a3a6e]/40 rounded-lg p-3 mb-4">
          <div className="flex items-center gap-1.5 mb-1.5">
            <svg className="w-3.5 h-3.5 text-[#d4619b]" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
            </svg>
            <span className="text-xs font-bold text-[#d4619b] uppercase tracking-wider">AI INSIGHT</span>
          </div>
          <p className="text-xs text-[#b8b8d8] leading-relaxed">{aiInsight}</p>
        </div>

        <button className="px-5 py-2 bg-[#d4619b] text-white text-xs font-semibold rounded-full hover:brightness-110 transition shadow-lg shadow-[#d4619b]/20">
          Reserve Now
        </button>
      </div>
    </div>
  );
}
