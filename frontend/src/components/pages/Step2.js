import React from 'react';

const Step2 = ({ nextStep, prevStep }) => {
  return (
    <div className="bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-5xl">
                <span className="text-4xl font-bold text-gray-700 text-center mb-4 block w-full">Payment</span>
                
                <div className="w-full flex mb-10">
                    <div className="w-1/2">text</div>   
                    <div className="w-1/2">
                    <form>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="cardnumber">
                                Card Number
                            </label>
                            <input type="text" 
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                                Bank
                            </label>
                            <input type="text" 
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                                Exp Date
                            </label>
                            <input type="date" 
                            className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                        <div className="mb-6 relative">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                                CVV
                            </label>
                            <input type="number"
                                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
                            />
                        </div>
                    </form>
                    </div>    
                </div>
                <button             
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold my-2 py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                onClick={nextStep}>Pay Now</button>
                <button             
                className="bg-gray-300 hover:bg-gray-400 text-white font-bold my-2 py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                onClick={prevStep}>Back</button>

                <button             
                className="bg-gray-300 hover:bg-gray-400 text-white font-bold my-2 py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                >Cancel</button>
            </div>
        </div>  
  );
};

export default Step2;
