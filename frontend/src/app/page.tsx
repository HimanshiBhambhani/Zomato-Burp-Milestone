"use client";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex flex-col bg-[#1a1a3e]">
      <Navbar />

      {/* Hero Section */}
      <section className="px-8 py-16 max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-12">
          {/* Left Content */}
          <div className="flex-1">
            <span className="inline-block px-3 py-1 text-xs font-medium bg-[#a4d65e] text-[#1a1a3e] rounded-full mb-4">
              AI-POWERED RECOMMENDATIONS
            </span>
            <h1 className="text-5xl font-extrabold text-white leading-tight mb-4">
              DISCOVER YOUR<br />
              PERFECT RESTAURANT<br />
              WITH AI!
            </h1>
            <p className="text-[#b8b8d8] text-base mb-6 max-w-md">
              Our AI analyzes thousands of restaurants based on your preferences. Get personalized recommendations ranked just for you. Filter by location, budget, cuisine, and ratings.
            </p>
            <button
              onClick={() => router.push("/results")}
              className="px-7 py-3 bg-[#d4619b] text-white font-semibold text-sm rounded-full hover:brightness-110 transition-all shadow-lg shadow-[#d4619b]/30"
            >
              START YOUR AI SEARCH
            </button>
          </div>

          {/* Right Illustration */}
          <div className="flex-1 flex justify-center">
            <div className="relative w-[420px] h-[320px] rounded-2xl overflow-hidden border border-[#3a3a6e]/50">
              <img
                src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop"
                alt="Restaurant atmosphere"
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#1a1a3e]/80 to-transparent" />
              <div className="absolute bottom-4 left-4 right-4">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-[#a4d65e] text-[#1a1a3e] rounded-full">AI POWERED</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-[#d4619b] text-white rounded-full">5000+ REVIEWS</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Email Signup Bar */}
      <section className="px-8 max-w-7xl mx-auto w-full mb-12">
        <div className="bg-[#232352] rounded-2xl px-8 py-5 flex items-center justify-between border border-[#3a3a6e]/30">
          <div className="flex items-center gap-4">
            <div className="flex -space-x-2">
              <div className="w-8 h-8 rounded-full bg-[#d4619b] border-2 border-[#232352]" />
              <div className="w-8 h-8 rounded-full bg-[#a4d65e] border-2 border-[#232352]" />
              <div className="w-8 h-8 rounded-full bg-[#6e6ea8] border-2 border-[#232352]" />
            </div>
            <div>
              <p className="text-white font-semibold text-sm">Join 2,400+ foodies discovery tonight</p>
              <p className="text-[#b8b8d8] text-xs">Get exclusive AI-powered recommendations</p>
            </div>
          </div>
          <div className="flex items-center bg-white/5 border border-[#3a3a6e] rounded-full overflow-hidden">
            <input
              type="email"
              placeholder="Enter your email"
              className="bg-transparent px-4 py-2.5 text-sm text-white placeholder-[#8888aa] outline-none w-56"
            />
            <button className="px-5 py-2.5 bg-[#d4619b] text-white text-sm font-medium rounded-full mr-1 hover:brightness-110 transition">
              JOIN NOW
            </button>
          </div>
        </div>
      </section>

      {/* Featured Experiences */}
      <section className="px-8 max-w-7xl mx-auto w-full mb-16">
        <h3 className="text-xs font-bold text-[#a4d65e] uppercase tracking-wider mb-6">FEATURED EXPERIENCES</h3>
        <div className="grid grid-cols-4 gap-4">
          {/* Restaurant Cards */}
          <div className="bg-[#232352] rounded-xl overflow-hidden border border-[#3a3a6e]/30">
            <div className="h-32 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&h=200&fit=crop" alt="Umami Central" className="w-full h-full object-cover" />
            </div>
            <div className="p-3 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Umami Central</p>
                <p className="text-xs text-[#b8b8d8]">Japanese Fusion</p>
              </div>
              <span className="text-xs font-bold bg-[#a4d65e] text-[#1a1a3e] px-2 py-0.5 rounded-full">4.9</span>
            </div>
          </div>

          <div className="bg-[#232352] rounded-xl overflow-hidden border border-[#3a3a6e]/30">
            <div className="h-32 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=200&fit=crop" alt="Midnight Tapas" className="w-full h-full object-cover" />
            </div>
            <div className="p-3 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-white">Midnight Tapas</p>
                <p className="text-xs text-[#b8b8d8]">Spanish Modern</p>
              </div>
              <span className="text-xs font-bold bg-[#a4d65e] text-[#1a1a3e] px-2 py-0.5 rounded-full">4.7</span>
            </div>
          </div>

          {/* 98% AI Accuracy */}
          <div className="bg-[#e8a0c8] rounded-xl flex flex-col items-center justify-center p-6">
            <div className="w-12 h-12 rounded-full border-2 border-[#1a1a3e]/30 flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-[#1a1a3e]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <p className="text-3xl font-extrabold text-[#1a1a3e]">98%</p>
            <p className="text-xs font-medium text-[#1a1a3e] tracking-wider">AI ACCURACY</p>
          </div>

          {/* Exclusive Mixology */}
          <div className="bg-[#232352] rounded-xl p-5 flex flex-col justify-between border border-[#3a3a6e]/30">
            <div>
              <p className="text-sm font-bold text-white mb-1">Exclusive Mixology</p>
              <p className="text-xs text-[#b8b8d8] leading-relaxed">
                Unlock secret menus and priority seating at the city&apos;s best cocktail lounges.
              </p>
            </div>
            <a href="#" className="text-xs text-[#d4619b] font-medium mt-3 flex items-center gap-1">
              Learn More <span>→</span>
            </a>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="px-8 max-w-7xl mx-auto w-full mb-16">
        <h2 className="text-3xl font-extrabold text-white text-center mb-10">HOW IT WORKS</h2>
        <div className="grid grid-cols-3 gap-6">
          {[
            { icon: "🎯", title: "Set Your Filters", desc: "Choose location, budget, cuisine, ratings to narrow down your search." },
            { icon: "🤖", title: "AI Analyzes", desc: "Our AI scores and ranks restaurants specifically for your unique palate." },
            { icon: "⭐", title: "Get Personal Recs", desc: "See top matches with detailed explanations on why they fit you." },
          ].map((step) => (
            <div key={step.title} className="bg-[#232352]/50 border border-[#3a3a6e]/30 rounded-2xl p-8 text-center">
              <div className="w-14 h-14 rounded-full bg-[#1a1a3e] border border-[#3a3a6e] flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">{step.icon}</span>
              </div>
              <h4 className="text-base font-bold text-white mb-2">{step.title}</h4>
              <p className="text-sm text-[#b8b8d8] leading-relaxed">{step.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Customize Filters Section */}
      <section className="px-8 max-w-7xl mx-auto w-full mb-16">
        <div className="bg-[#232352]/50 border border-[#3a3a6e]/30 rounded-2xl p-10 flex items-center gap-12">
          {/* Filters Preview */}
          <div className="w-[220px] shrink-0">
            <h4 className="text-base font-bold text-white mb-1">Filters</h4>
            <p className="text-xs text-[#b8b8d8] mb-4">Refine your discovery</p>
            <div className="space-y-2">
              <div className="flex items-center gap-2 px-3 py-2 bg-[#a4d65e] text-[#1a1a3e] rounded-lg text-sm font-medium">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /></svg>
                Location
              </div>
              <div className="flex items-center gap-2 px-3 py-2 text-[#b8b8d8] text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                Budget
              </div>
              <div className="flex items-center gap-2 px-3 py-2 text-[#b8b8d8] text-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" /></svg>
                Cuisine
              </div>
              <div className="flex items-center gap-2 px-3 py-2 text-[#b8b8d8] text-sm">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" /></svg>
                Rating
              </div>
            </div>
            <button className="mt-4 w-full py-2 text-sm font-medium bg-[#d4619b] text-white rounded-full hover:brightness-110 transition">
              Apply Filters
            </button>
          </div>

          {/* Right Content */}
          <div className="flex-1">
            <h3 className="text-3xl font-extrabold text-white mb-3">
              Customize your search with powerful filters
            </h3>
            <p className="text-sm text-[#b8b8d8] leading-relaxed mb-5">
              The BURP recommendation engine doesn&apos;t just guess. It uses granular data points—from neighborhood vibes to specific ingredient preferences—to ensure every meal is an event to remember.
            </p>
            <div className="flex gap-2">
              {["#Sushi", "#PetFriendly", "#OutdoorSeating", "#LateNight"].map((tag) => (
                <span key={tag} className="px-3 py-1 text-xs bg-[#3a3a6e]/50 text-[#b8b8d8] rounded-full border border-[#3a3a6e]">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
