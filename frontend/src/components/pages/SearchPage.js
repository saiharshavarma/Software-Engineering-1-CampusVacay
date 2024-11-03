import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Search, User, MapPin } from 'lucide-react';

const SearchPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const searchResults = location.state?.searchResults || [];

  const handleBackToHome = () => {
    navigate('/');
  };

  const HotelCard = ({ hotel }) => (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="relative">
        <img 
          src={hotel.image || "/api/placeholder/400/300"} 
          alt={hotel.name}
          className="w-full h-64 object-cover"
        />
        <div className="absolute top-4 left-4">
          <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm">
            ${hotel.price}/night
          </span>
        </div>
        {hotel.student_discount && (
          <div className="absolute top-4 right-4">
            <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm">
              {hotel.student_discount}% Student Discount
            </span>
          </div>
        )}
      </div>
      
      <div className="p-6">
        <h3 className="text-xl font-bold mb-2">{hotel.name}</h3>
        <div className="flex items-center text-gray-600 mb-2">
          <MapPin size={16} className="mr-2" />
          <span>{hotel.location}</span>
        </div>
        
        <div className="mb-4">
          <p className="text-gray-600">{hotel.description}</p>
        </div>
        
        <div className="border-t pt-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <span className="text-gray-600 block">Check-in</span>
              <span className="font-semibold">{hotel.check_in_time}</span>
            </div>
            <div>
              <span className="text-gray-600 block">Check-out</span>
              <span className="font-semibold">{hotel.check_out_time}</span>
            </div>
          </div>
        </div>

        <div className="mt-4 border-t pt-4">
          <h4 className="font-semibold mb-2">Facilities</h4>
          <div className="flex flex-wrap gap-2">
            {hotel.facilities?.split(',').map((facility, index) => (
              <span 
                key={index}
                className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
              >
                {facility.trim()}
              </span>
            ))}
          </div>
        </div>
        
        <button 
          onClick={() => navigate(`/hotel/${hotel.id}`)}
          className="mt-6 w-full bg-blue-600 text-white py-2 px-4 rounded-full hover:bg-blue-700 transition duration-300"
        >
          Book Now
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Search Results</h1>
          <button
            onClick={handleBackToHome}
            className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition duration-300"
          >
            Back to Home
          </button>
        </div>

        {searchResults.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600">No hotels found matching your criteria.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {searchResults.map((hotel, index) => (
              <HotelCard key={index} hotel={hotel} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;