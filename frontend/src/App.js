import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/pages/HomePage';
import LoginPage from './components/pages/LoginPage';
import RegisterPage from './components/pages/RegisterPage';
import RegisterSuccessPage from './components/pages/RegisterSuccessPage';
import HotelRegister from './components/pages/HotelRegister';
import PaymentPage from './components/pages/PaymentPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/register/hotel" element={<HotelRegister />} />
          <Route path="/register/success" element={<RegisterSuccessPage /> } />
          <Route path="/payment" element={<PaymentPage /> } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;