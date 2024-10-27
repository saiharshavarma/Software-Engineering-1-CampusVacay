import React from 'react';
import { Link } from 'react-router-dom';

const Step3 = ({ prevStep }) => {
  return (
    <div className="bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-5xl">
                <span className="text-4xl font-bold text-gray-700 text-center mb-4 block w-full">Payment Completed</span>
                
                <Link  
                to="/"           
                className="w-full bg-gray-300 hover:bg-gray-400 text-white font-bold my-2 py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >Go to Dashboard</Link>
            </div>
        </div>
  );
};

export default Step3;
