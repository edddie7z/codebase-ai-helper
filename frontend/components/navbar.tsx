import React from "react";
import Link from "next/link";

function Navbar() {
  return (
    <nav className="bg-neutral-900 border-b border-neutral-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-amber-50 text-2xl font-bold">
              ProgAssist
            </Link>
          </div>
          <div className="flex items-center space-x-8">
            <Link
              href="/"
              className="text-amber-50 text-lg font-semibold hover:text-amber-200 transition-colors duration-200"
            >
              Home
            </Link>
            <Link
              href="/assistant"
              className="text-amber-50 text-lg font-semibold hover:text-amber-200 transition-colors duration-200"
            >
              Assistant
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
