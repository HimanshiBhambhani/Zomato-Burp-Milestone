export default function Footer() {
  return (
    <footer className="flex items-center justify-between px-8 py-6 border-t border-[#3a3a6e]/30 mt-auto">
      <span className="text-sm font-bold text-white">BURP</span>
      <div className="flex gap-6 text-sm text-[#b8b8d8]">
        <a href="#" className="hover:text-white transition-colors">Privacy</a>
        <a href="#" className="hover:text-white transition-colors">Terms</a>
        <a href="#" className="hover:text-white transition-colors">Contact</a>
      </div>
      <span className="text-xs text-[#8888aa]">© 2024 BURP. All rights reserved.</span>
    </footer>
  );
}
