"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/results", label: "Trending" },
    { href: "#", label: "Events" },
  ];

  return (
    <nav className="flex items-center justify-between px-8 py-4 bg-[#1a1a3e]/80 backdrop-blur-sm sticky top-0 z-50 border-b border-[#3a3a6e]/30">
      <Link href="/" className="flex items-baseline gap-1.5">
        <span className="text-2xl font-bold text-white tracking-wide">BURP</span>
        <span className="text-[10px] text-[#b8b8d8] font-medium">by <span className="text-[#e23744]">Zomato</span></span>
      </Link>

      <div className="flex items-center gap-8">
        {navLinks.map((link) => (
          <Link
            key={link.label}
            href={link.href}
            className={`text-sm font-medium transition-colors ${
              pathname === link.href
                ? "text-white border-b-2 border-[#a4d65e] pb-0.5"
                : "text-[#b8b8d8] hover:text-white"
            }`}
          >
            {link.label}
          </Link>
        ))}
      </div>

      <button className="px-5 py-2 text-sm font-medium text-white border border-[#d4619b] rounded-full hover:bg-[#d4619b]/20 transition-colors">
        Sign In
      </button>
    </nav>
  );
}
