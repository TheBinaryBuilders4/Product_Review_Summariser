import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/navbar';
import ProductReview from './pages/ProductReview';

function App() {
  const [loadingPage, setLoadingPage] = useState(true); 

   // Simulate page loading completion
   useState(() => {
    setTimeout(() => {
      setLoadingPage(false);
    }, 2000); // Adjust this time as needed for your actual page load
  }, []);

  if (loadingPage) {
    return (
      <div className="flex justify-center items-center h-screen bg-gradient-to-r from-slate-100 via-slate-200 to-slate-300">
        <div className="banter-loader">
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
          <div className="banter-loader__box"></div>
        </div> {/* Add your loader here */}
      </div>
    );
  }
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<ProductReview />} />
      </Routes>
    </Router>
  );
}

export default App;
