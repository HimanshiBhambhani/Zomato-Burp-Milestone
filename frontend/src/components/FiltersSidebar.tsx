"use client";

interface Filters {
  location: string;
  budget: string;
  cuisine: string;
  rating: string;
}

interface FiltersProps {
  filters: Filters;
  onChange: (f: Filters) => void;
  onSearch: (f?: Filters) => void;
  mode?: "full" | "compact";
}

export default function FiltersSidebar({
  filters,
  onChange,
  onSearch,
  mode = "full",
}: FiltersProps) {
  const budgetOptions = ["Low", "Mid", "High"];
  const { location, budget, cuisine, rating } = filters;

  if (mode === "compact") {
    return (
      <aside className="w-[160px] shrink-0 py-6 px-4">
        <h3 className="text-lg font-bold text-white mb-1">Filters</h3>
        <p className="text-xs text-[#b8b8d8] mb-4">Refine your discovery</p>
        <div className="space-y-3 text-sm">
          <div className="flex items-center gap-2 text-[#b8b8d8]">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            <span>{location || "Location"}</span>
          </div>
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${budget ? "bg-[#a4d65e] text-[#1a1a3e]" : "text-[#b8b8d8]"}`}>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
            <span>Budget: {budget || "Any"}</span>
          </div>
          <div className="flex items-center gap-2 text-[#b8b8d8]">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" /></svg>
            <span>{cuisine || "Cuisine"}</span>
          </div>
          <div className="flex items-center gap-2 text-[#b8b8d8]">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" /></svg>
            <span>Rating: {rating}+</span>
          </div>
        </div>
        <button
          onClick={() => onSearch(filters)}
          className="mt-6 w-full py-2 text-sm font-medium bg-[#a4d65e] text-[#1a1a3e] rounded-full hover:brightness-110 transition"
        >
          Apply Filters
        </button>
      </aside>
    );
  }

  return (
    <aside className="w-[200px] shrink-0 bg-[#1e1e4a]/50 rounded-2xl p-5 h-fit sticky top-24">
      <h3 className="text-lg font-bold text-white mb-1">Filters</h3>
      <p className="text-xs text-[#b8b8d8] mb-5">Refine your discovery</p>

      {/* Location */}
      <div className="mb-4">
        <label className="text-xs font-medium text-[#b8b8d8] mb-1 block">Location</label>
        <div className="relative">
          <select
            value={location}
            onChange={(e) => onChange({ ...filters, location: e.target.value })}
            className="w-full bg-[#232352] border border-[#3a3a6e] rounded-lg px-3 py-2 text-sm text-white appearance-none cursor-pointer focus:border-[#d4619b] outline-none"
          >
            <option value="New Delhi">New Delhi</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Bangalore">Bangalore</option>
            <option value="Kolkata">Kolkata</option>
            <option value="Chennai">Chennai</option>
            <option value="Hyderabad">Hyderabad</option>
          </select>
          <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#b8b8d8] pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
        </div>
      </div>

      {/* Budget */}
      <div className="mb-4">
        <label className="text-xs font-medium text-[#b8b8d8] mb-2 block">Budget</label>
        <div className="flex gap-1.5">
          {budgetOptions.map((opt) => (
            <button
              key={opt}
              onClick={() => onChange({ ...filters, budget: opt })}
              className={`px-3 py-1 text-xs font-medium rounded-full transition-colors ${
                budget === opt
                  ? "bg-[#a4d65e] text-[#1a1a3e]"
                  : "bg-[#232352] text-[#b8b8d8] border border-[#3a3a6e] hover:border-[#d4619b]"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Cuisine */}
      <div className="mb-4">
        <label className="text-xs font-medium text-[#b8b8d8] mb-1 block">Cuisine</label>
        <div className="relative">
          <select
            value={cuisine}
            onChange={(e) => onChange({ ...filters, cuisine: e.target.value })}
            className="w-full bg-[#232352] border border-[#3a3a6e] rounded-lg px-3 py-2 text-sm text-white appearance-none cursor-pointer focus:border-[#d4619b] outline-none"
          >
            <option value="">All Cuisines</option>
            <option value="Italian">Italian</option>
            <option value="Chinese">Chinese</option>
            <option value="North Indian">North Indian</option>
            <option value="South Indian">South Indian</option>
            <option value="Japanese">Japanese</option>
            <option value="Thai">Thai</option>
            <option value="Mexican">Mexican</option>
            <option value="Continental">Continental</option>
            <option value="Mughlai">Mughlai</option>
            <option value="Seafood">Seafood</option>
            <option value="Bengali">Bengali</option>
            <option value="Biryani">Biryani</option>
            <option value="French">French</option>
            <option value="American">American</option>
            <option value="Mediterranean">Mediterranean</option>
          </select>
          <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#b8b8d8] pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
        </div>
      </div>

      {/* Rating */}
      <div className="mb-6">
        <label className="text-xs font-medium text-[#b8b8d8] mb-2 block">Rating</label>
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#b8b8d8]">Rating</span>
          <span className="text-sm font-bold text-[#a4d65e]">{rating}+ ★</span>
        </div>
        <input
          type="range"
          min="0"
          max="5"
          step="0.5"
          value={rating}
          onChange={(e) => onChange({ ...filters, rating: e.target.value })}
          className="w-full mt-1 accent-[#a4d65e]"
        />
      </div>

      {/* Apply Button */}
      <button
        onClick={() => onSearch(filters)}
        className="w-full py-2.5 text-sm font-medium bg-[#a4d65e] text-[#1a1a3e] rounded-full hover:brightness-110 transition"
      >
        Apply Filters
      </button>

      {/* Show All Button */}
      <button
        onClick={() => onSearch({ location: filters.location, budget: "", cuisine: "", rating: "0" })}
        className="w-full mt-2 py-2.5 text-sm font-medium text-[#b8b8d8] border border-[#3a3a6e] rounded-full hover:border-[#d4619b] hover:text-white transition"
      >
        Show All in {filters.location || "Location"}
      </button>
    </aside>
  );
}
