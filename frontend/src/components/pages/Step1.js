import React, { useState } from 'react';
import { Form } from 'react-router-dom';


const Step1 = ({ nextStep }) => {
    const [FormData, setFormData] = useState({
        startDate: '', endDate: ''
    });
    
    const [difference, setDifference] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...FormData, [e.target.name]: e.target.value });
        calculateDifference();
    }

    const calculateDifference = () => {
        
        const start = new Date(FormData.startDate);
        const end = new Date(FormData.endDate);
        
        const diffTime = Math.abs(end - start);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
        setDifference(diffDays);
    };
    return (
        
        <div className="bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-5xl items-center justify-center">
                <span className="text-4xl font-bold text-gray-700 text-center mb-4 block w-full">Booking Information</span>
                <div className="flex items-center justify-center w-full px-4 my-4">
                    <div className="flex w-1/3">
                   
                    <div className="w-1/2">1</div>
                   
                   
                    <div className="w-1/2">2</div>
                    <div>3</div>
                    </div>
                </div>
                <div className="w-full flex mb-10">
                    <div className="w-1/2">Hotel Information</div>   
                    <div className="w-1/2">
                    <form>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                                Pick Start Date
                            </label>
                            <input type="date" 
                            name="startDate"
                            value={FormData.startDate}
                            onChange={handleChange}
                            on
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                                Pick End Date
                            </label>
                            <input type="date" 
                            name="endDate"
                            value={FormData.endDate}
                            onChange={handleChange}
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        
                        <div className="mb-6 relative">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                                First Name
                            </label>
                            <input type="text"
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        <div className="mb-6 relative">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                                Last Name
                            </label>
                            <input type="text"
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        <div>
                            You will pay ${100} USD
                            <br/>
                            per {difference} Days
                        </div>
                    </form>
                    </div>    
                </div>
                <button             
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold my-2 py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                onClick={nextStep}>Book Now</button>

                <button             
                className="bg-gray-300 hover:bg-gray-400 text-white font-bold my-2 py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                >Cancel</button>
            </div>
        </div>
  );
};

export default Step1;
