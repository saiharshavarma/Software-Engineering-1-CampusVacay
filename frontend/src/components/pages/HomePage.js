


import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Star, Navigation, Calendar, Users } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './edits.css';
import LoginPage from './LoginPage';

// Fallback images array
const HOTEL_IMAGES = [
  'https://images.pexels.com/photos/1134176/pexels-photo-1134176.jpeg',
  'https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg',
  'https://images.pexels.com/photos/2506990/pexels-photo-2506990.jpeg',
  'https://images.pexels.com/photos/2869215/pexels-photo-2869215.jpeg',
  'https://images.pexels.com/photos/3225531/pexels-photo-3225531.jpeg',
  'https://images.pexels.com/photos/1743229/pexels-photo-1743229.jpeg',
  'https://images.pexels.com/photos/2096983/pexels-photo-2096983.jpeg',
  'https://images.pexels.com/photos/2417842/pexels-photo-2417842.jpeg',
  'https://images.pexels.com/photos/3155666/pexels-photo-3155666.jpeg',
  'https://images.pexels.com/photos/2373201/pexels-photo-2373201.jpeg'
];

const Header = () => {
  const [token, setToken] = useState(null);
  const [loginType, setLoginType] = useState(null);
  const [isScrolled, setIsScrolled] = useState(false);
  const [message, setMessage] = useState({ type: '', content: '' });
  
  useEffect(() => {
    setLoginType(localStorage.getItem('type'));
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      setToken(storedToken);
    }
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = async () => {
    try {
      const url = `http://campusvacay-env.eba-mdfmvvfe.us-east-1.elasticbeanstalk.com/student/api/logout/`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token ' + localStorage.getItem('authToken'),
        },
        body: JSON.stringify(''),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || JSON.stringify(responseData) || 'Logout failed');
      }

      setMessage({ type: 'success', content: 'Logout successful!' });
      localStorage.removeItem('authToken');
      setToken(null);
    } catch (error) {
      console.error('Logout error:', error);
      setMessage({ type: 'error', content: error.message });
    }
  };

  return (
    <header className={`fixed w-full z-50 transition-all duration-300 ${isScrolled ? 'bg-white shadow-md py-2' : 'bg-transparent py-4'}`}>
      <div className="max-w-6xl mx-auto px-6 flex justify-between items-center">
        <a href="#home" className="text-3xl font-bold text-blue-700 flex items-center no-underline">
          <Navigation className="mr-2" />
          CampusVacay.
        </a>
        <div className="flex items-center space-x-4">
          {token && loginType == 'Student' ? (
            <a href="/student/dashboard" className="list-none text-gray-600 hover:text-blue-700 cursor-pointer transition duration-300">
              Dashboard
            </a>
          ) : token && loginType === 'Hotel' ? (
            <a href="/dashboard" className="list-none text-gray-600 hover:text-blue-700 cursor-pointer transition duration-300">
              Dashboard
            </a>
          ) : (<div></div>)
          }
          {token ? (
            <button onClick={handleLogout} className="bg-blue-700 text-white px-5 py-2 rounded-lg hover:bg-blue-800 transition duration-300">
              Logout
            </button>
          ) : (
            <a href="/login" className="bg-blue-700 text-white px-5 py-2 rounded-lg hover:bg-blue-800 transition duration-300">
              Login
            </a>
          )}
        </div>
      </div>
      {message.content && (
        <div className={`fixed top-16 right-8 p-4 rounded-lg ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {message.content}
        </div>
      )}
    </header>
  );
};

const Hero = () => (
  <section className="flex justify-between items-center py-32 px-6 bg-gradient-to-br from-white to-blue-50">
    <div className="max-w-6xl mx-auto flex flex-wrap lg:flex-nowrap items-center w-full">
      <div className="lg:w-1/2 pr-8">
        <h1 className="text-6xl font-bold mb-6 text-gray-800 leading-tight">
          Forget Busy Work,
          <br />
          <span className="text-blue-700">Start Next Vacation</span>
        </h1>
        <p className="text-gray-600 mb-8 text-lg">
          Where student adventures meet budget-friendly getaways.
          Book smart, travel easy, and create memories that last!
        </p>
        <button className="bg-blue-700 text-white px-8 py-4 rounded-lg text-lg hover:bg-blue-800 transition duration-300">
          Show More
        </button>
        <div className="flex space-x-12 mt-10">
          {[
            ['2500', 'Users', '🏨'],
            ['200', 'Treasure', '📸'],
            ['100', 'Cities', '📍']
          ].map(([number, label, emoji]) => (
            <div key={label} className="text-center">
              <div className="text-4xl">{emoji}</div>
              <strong className="text-3xl block font-bold text-blue-700">{number}</strong>
              <span className="text-gray-600 capitalize">{label}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="lg:w-1/2">
        <img
          src={HOTEL_IMAGES[0]}
          alt="Luxury Room"
          className="rounded-2xl shadow-lg object-cover w-full h-80"
        />
      </div>
    </div>
  </section>
);

const SearchBar = () => {
  const navigate = useNavigate();
  const [searchData, setSearchData] = useState({
    location: '',
    check_in: '',
    check_out: '',
    guests: ''
  });

  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const autocompleteService = useRef(null);
  const wrapperRef = useRef(null);

  useEffect(() => {
    const initializeAutocomplete = () => {
      if (window.google && window.google.maps && window.google.maps.places) {
        autocompleteService.current = new window.google.maps.places.AutocompleteService();
      } else {
        setTimeout(initializeAutocomplete, 500);
      }
    };

    initializeAutocomplete();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const fetchPlacePredictions = (input) => {
    if (!input || !autocompleteService.current) {
      setSuggestions([]);
      return;
    }

    const searchConfig = {
      input,
      componentRestrictions: { country: 'us' }
    };

    autocompleteService.current.getPlacePredictions(
      searchConfig,
      (predictions, status) => {
        if (status === 'OK' && predictions) {
          const processedSuggestions = predictions.map(prediction => ({
            id: prediction.place_id,
            description: prediction.description
          }));
          setSuggestions(processedSuggestions);
          setShowSuggestions(true);
        } else {
          setSuggestions([]);
        }
      }
    );
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearchData(prev => ({
      ...prev,
      [name]: value
    }));

    if (name === 'location') {
      fetchPlacePredictions(value);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchData(prev => ({
      ...prev,
      location: suggestion.description
    }));
    setShowSuggestions(false);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    const requestBody = {
      location: searchData.location,
      check_in: searchData.check_in,
      check_out: searchData.check_out,
      guests: searchData.guests
    };

    try {
      const response = await fetch('http://campusvacay-env.eba-mdfmvvfe.us-east-1.elasticbeanstalk.com/hotel/api/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Search failed');
      }

      navigate('/search', { 
        state: { 
          searchResults: data,
          searchData: searchData 
        } 
      });
    } catch (error) {
      setError('Failed to perform search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-lg max-w-6xl mx-auto -mt-14 relative z-10 border border-gray-200">
      <form onSubmit={handleSearch} className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px]">
          <label className="block mb-1 text-gray-600">Check Available</label>
          <input
            type="date"
            name="check_in"
            value={searchData.check_in}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg p-3"
            min={new Date().toISOString().split('T')[0]}
          />
        </div>
        <div className="flex-1 min-w-[200px]">
          <label className="block mb-1 text-gray-600">Check Out</label>
          <input
            type="date"
            name="check_out"
            value={searchData.check_out}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg p-3"
            min={searchData.check_in || new Date().toISOString().split('T')[0]}
          />
        </div>
        <div className="flex-1 min-w-[150px]">
          <label className="block mb-1 text-gray-600">Guests</label>
          <input
            type="number"
            name="guests"
            value={searchData.guests}
            onChange={handleChange}
            placeholder="Number of guests"
            className="w-full border border-gray-300 rounded-lg p-3"
            min="1"
          />
        </div>
        <div className="flex-1 min-w-[200px] relative" ref={wrapperRef}>
          <label className="block mb-1 text-gray-600">Location</label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              name="location"
              value={searchData.location}
              onChange={handleChange}
              placeholder="Enter a city"
              className="w-full border border-gray-300 rounded-lg p-3 pl-10"
              autoComplete="off"
            />
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                {suggestions.map(suggestion => (
                  <div
                    key={suggestion.id}
                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    <MapPin size={16} className="mr-2 text-gray-400" />
                    <span>{suggestion.description}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className="bg-blue-700 text-white px-6 py-3 rounded-lg hover:bg-blue-800 transition duration-300 flex items-center self-end"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Searching...</span>
            </>
          ) : (
            <>
              <Search className="mr-2" size={18} />
              Search
            </>
          )}
        </button>
      </form>
      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}
    </div>
  );
};

const PropertyCard = ({ hotel }) => {
  const baseUrl = 'http://campusvacay-env.eba-mdfmvvfe.us-east-1.elasticbeanstalk.com';
  const hotelImage = hotel.hotel_photos ? `${baseUrl}${hotel.hotel_photos}` : HOTEL_IMAGES[0];
  const lowestPrice = hotel.rooms && hotel.rooms.length > 0
    ? Math.min(...hotel.rooms.map(room => room.price_per_night))
    : null;

  return (
    <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition transform hover:-translate-y-1">
      <div className="relative">
        <img
          src={hotelImage}
          alt={hotel.hotel_name}
          className="w-full h-60 object-cover"
          onError={(e) => {
            e.target.src = HOTEL_IMAGES[0]; // Fallback image if API image fails to load
          }}
        />
        {hotel.average_rating >= 4.5 && (
          <div className="absolute top-4 right-4 bg-blue-700 text-white px-2 py-1 rounded-full text-xs">
            Popular Choice
          </div>
        )}
        {lowestPrice && (
          <div className="absolute bottom-4 left-4 bg-blue-700 text-white px-3 py-1 rounded-md text-sm">
            ${lowestPrice} per night
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-bold text-lg mb-1">{hotel.hotel_name}</h3>
        <p className="text-sm text-gray-600">{hotel.address}</p>
        {hotel.student_discount > 0 && (
          <p className="text-sm text-green-600 mt-1">
            {hotel.student_discount}% Student Discount
          </p>
        )}
        {hotel.facilities && (
          <p className="text-sm text-gray-500 mt-1">
            {hotel.facilities}
          </p>
        )}
      </div>
    </div>
  );
};

const PropertyGrid = () => {
  const [hotels, setHotels] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHotels = async () => {
      try {
        const response = await fetch('http://campusvacay-env.eba-mdfmvvfe.us-east-1.elasticbeanstalk.com/hotel/api/top-hotels/');
        if (!response.ok) {
          throw new Error('Failed to fetch hotels');
        }
        const data = await response.json();
        setHotels(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching hotels:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHotels();
  }, []);

  if (loading) {
    return (
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">Most Picked</h2>
          <div className="text-center text-gray-600">Loading...</div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">Most Picked</h2>
          <div className="text-center text-red-600">Error: {error}</div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 px-6">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-gray-800 mb-8">Most Picked</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {hotels.map((hotel) => (
            <PropertyCard key={hotel.hotel_id} hotel={hotel} />
          ))}
        </div>
      </div>
    </section>
  );
};

const Footer = () => (
  <footer className="bg-gray-800 text-gray-200 py-6">
    <div className="max-w-6xl mx-auto px-6 flex flex-wrap justify-between items-start">
      <div className="w-full md:w-1/3 mb-4 md:mb-0">
        <a href="#home" className="text-3xl font-bold text-blue-500 flex items-center mb-2 no-underline">
          <Navigation className="mr-2" />
          CampusVacay.
        </a>
        <p className="text-gray-400 text-sm">We kaboom your beauty holiday instantly and memorable.</p>
      </div>
      <div className="w-full md:w-1/3 text-right">
        <h4 className="text-lg font-semibold mb-2">Contact Us</h4>
        <ul className="text-gray-400 text-sm space-y-1">
          <li>Phone: +1-234-567-890</li>
          <li>Email: support@campusvacay.com</li>
          <li>Address: 123 Vacation Lane, Dream City, Holiday State</li>
        </ul>
      </div>
    </div>
  </footer>
);

const CopyrightBar = () => (
  <div className="bg-[#3252DF] text-white h-11 flex items-center justify-center text-center text-sm">
    <p>&copy; {new Date().getFullYear()} CampusVacay. All rights reserved.</p>
  </div>
);

const HomePage = () => (
  <div className="bg-gray-50 min-h-screen flex flex-col" id="home">
    <Header />
    <Hero />
    <SearchBar />
    <PropertyGrid />
    <Footer />
    <CopyrightBar />
  </div>
);

export default HomePage;