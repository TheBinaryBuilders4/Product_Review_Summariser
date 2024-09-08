import React, { useState } from 'react';

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-white shadow-lg fixed w-full z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <a href="#" className="text-2xl font-bold text-gray-800">
              Sentiment Analyzer
            </a>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <a href="/" className="text-gray-800 hover:text-purple-600">
              Home
            </a>
            <a href="#about" className="text-gray-800 hover:text-purple-600">
              About
            </a>
          </div>
          <div className="flex items-center md:hidden">
            <button onClick={toggleMenu} className="text-gray-800 hover:text-purple-600 focus:outline-none">
              <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <a href="#home" className="block text-gray-800 hover:text-purple-600">
              Home
            </a>
            <a href="#about" className="block text-gray-800 hover:text-purple-600">
              About
            </a>
            <a href="#contact" className="block text-gray-800 hover:text-purple-600">
              Contact
            </a>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;

