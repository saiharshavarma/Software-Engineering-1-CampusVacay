import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';


const RegisterSuccessPage = () => {
  const [loginType, setLoginType] = useState('Student');

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md flex w-full max-w-4xl">
        <div className="w-full bg-cover bg-center rounded-l-lg" style={{backgroundImage: "url('/api/placeholder/600/800')"}}>
          
            <div className="text-center text-4xl font-bold py-5">CampusVacay.</div>
            <span></span>
            <div className="text-center text-5xl font-bold ">Account Created Successfully</div>
            <div className="text-center text-2xl py-10">Please Check Your Email</div>
            <div className='flex items-center'>
              <Link className="text-center bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
               to='/login'>
                Book Now
              </Link>
            </div>
          
        </div>
      </div>
    </div>
  );
};

export default RegisterSuccessPage;