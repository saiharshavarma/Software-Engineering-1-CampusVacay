// import React, { useState, useEffect } from 'react';
// import { Search, User, MapPin } from 'lucide-react';
// import { Link } from 'react-router-dom';

// const Header = () => {
//   const [token, setToken] = useState(null);
//   useEffect(() => {
//     const storedToken = localStorage.getItem('authToken');
//     if (storedToken) {
//       console.log(storedToken)
//       setToken(storedToken);
//     }
//   }, []);
//   const [message, setMessage] = useState({ type: '', content: '' });

//   const handleLogout = async() => {
//     try {
//       const url = `http://10.18.191.34:8000/student/api/logout/`;
//       console.log('Sending request to:', url);
      
//       const response = await fetch(url, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': ' Token ' + localStorage.getItem('authToken')
//         },
//         body: JSON.stringify(''),
//       });

//       console.log('Response status:', response.status);
//       console.log('Response headers:', Object.fromEntries(response.headers.entries()));

//       const responseText = await response.text();
//       console.log('Full response text:', responseText);

//       let responseData;
//       try {
//         responseData = JSON.parse(responseText);
//         console.log('Parsed JSON response:', responseData);
//       } catch (e) {
//         console.error('Error parsing JSON:', e);
//         setMessage({ type: 'error', content: 'Server returned an unexpected response. Please try again.' });
//         return;
//       }

//       if (!response.ok) {
//         if (response.status === 400 && typeof responseData === 'object') {
//           const errorMessages = Object.entries(responseData)
//             .map(([key, value]) => `${key}: ${value.join(', ')}`)
//             .join('; ');
//           throw new Error(errorMessages);
//         } else {
//           throw new Error(responseData.detail || JSON.stringify(responseData) || 'Login failed');
//         }
//       }

//       console.log('Logout successful:', responseData);
//       setMessage({ type: 'success', content: 'Logout successful!' });
//       localStorage.removeItem('authToken');
//       setToken(null);
//     } catch (error) {
//       console.error('Logout error:', error);
//       setMessage({ type: 'error', content: error.message });
//     }
//   };

//   return(
//     <header className="flex justify-between items-center py-4 px-8 bg-white">
//       <div className="text-2xl font-bold text-blue-600">CampusVacay.</div>
//       <nav>
//         <ul className="flex space-x-8">
//           {['Home', 'Hotels', 'Rooms', 'About', 'Contact'].map((item) => (
//             <li key={item} className="text-gray-600 hover:text-blue-600 cursor-pointer">{item}</li>
//           ))}
//         </ul>
//       </nav>
//       { token ? (
//         <button onClick={handleLogout} className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition duration-300">
//           Logout
//         </button>
//       ) : (
//         <Link to="/login" className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition duration-300">
//           Login
//         </Link> 
//       )}
//     </header>
//   );
// };

// const Hero = () => (
//   <section className="flex justify-between items-center py-12 px-8 bg-white">
//     <div className="w-1/2 pr-12">
//       <h1 className="text-4xl font-bold mb-4 leading-tight text-gray-800">Forget Busy Work,<br />Start Next Vacation</h1>
//       <p className="text-gray-600 mb-8">Where dreams come true! Start your unforgettable journey with us. Book a vacation you'll never forget!</p>
//       <button className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg hover:bg-blue-700 transition duration-300">Show More</button>
//       <div className="flex space-x-12 mt-12">
//         {[['2500+', 'stays'], ['250', 'cities'], ['100', 'locations']].map(([number, label]) => (
//           <div key={label}>
//             <strong className="text-2xl block text-blue-600">{number}</strong>
//             <span className="text-gray-600">{label}</span>
//           </div>
//         ))}
//       </div>
//     </div>
//     <div className="w-1/2">
//       <img src="/api/placeholder/500/300" alt="Vacation room" className="rounded-2xl shadow-lg w-full h-auto" />
//     </div>
//   </section>
// );

// const SearchBar = () => {
//   const [searchData, setSearchData] = useState({
//     location: '',
//     check_in: '',
//     check_out: '',
//     guests: '2'
//   });
//   const [searchResults, setSearchResults] = useState(null);
//   const [error, setError] = useState(null);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setSearchData(prev => ({
//       ...prev,
//       [name]: value
//     }));
//   };

//   const handleSearch = async (e) => {
//     e.preventDefault();
//     setError(null);
    
//     try {
//       const response = await fetch('http://10.18.191.34:8000/hotel/api/search/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(searchData),
//       });

//       const data = await response.json();

//       if (!response.ok) {
//         throw new Error(data.detail || 'Search failed');
//       }

//       setSearchResults(data);
//       console.log('Search results:', data);
//     } catch (error) {
//       setError(error.message);
//       console.error('Search error:', error);
//     }
//   };

//   return (
//     <div className="bg-white p-6 rounded-xl shadow-md max-w-4xl mx-auto -mt-8 relative z-10">
//       <form onSubmit={handleSearch} className="flex flex-wrap gap-4">
//         {/* Location Search */}
//         <div className="flex-1 min-w-[200px]">
//           <div className="flex items-center space-x-2">
//             <MapPin size={20} className="text-gray-400" />
//             <input
//               type="text"
//               name="location"
//               value={searchData.location}
//               onChange={handleChange}
//               placeholder="Where are you going?"
//               className="w-full p-2 focus:outline-none border-b"
//             />
//           </div>
//         </div>

//         {/* Check-in Date */}
//         <div className="flex-1 min-w-[200px]">
//           <div className="flex items-center space-x-2">
//             <span className="text-gray-400">Check In</span>
//             <input
//               type="date"
//               name="check_in"
//               value={searchData.check_in}
//               onChange={handleChange}
//               className="w-full p-2 focus:outline-none border-b"
//             />
//           </div>
//         </div>

//         {/* Check-out Date */}
//         <div className="flex-1 min-w-[200px]">
//           <div className="flex items-center space-x-2">
//             <span className="text-gray-400">Check Out</span>
//             <input
//               type="date"
//               name="check_out"
//               value={searchData.check_out}
//               onChange={handleChange}
//               className="w-full p-2 focus:outline-none border-b"
//             />
//           </div>
//         </div>

//         {/* Number of Guests */}
//         <div className="flex-1 min-w-[150px]">
//           <div className="flex items-center space-x-2">
//             <User size={20} className="text-gray-400" />
//             <select
//               name="guests"
//               value={searchData.guests}
//               onChange={handleChange}
//               className="w-full p-2 focus:outline-none border-b appearance-none"
//             >
//               <option value="1">1 Guest</option>
//               <option value="2">2 Guests</option>
//               <option value="3">3 Guests</option>
//               <option value="4">4 Guests</option>
//               <option value="5">5+ Guests</option>
//             </select>
//           </div>
//         </div>

//         {/* Search Button */}
//         <button 
//           type="submit" 
//           className="bg-blue-600 text-white px-8 py-3 rounded-full hover:bg-blue-700 transition duration-300 flex-shrink-0"
//         >
//           <Search className="inline mr-2" size={20} />
//           Search
//         </button>
//       </form>

//       {error && (
//         <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">
//           {error}
//         </div>
//       )}

//       {searchResults && (
//         <div className="mt-4">
//           {/* Display search results here */}
//           {/* You can map through searchResults and use PropertyCard to display them */}
//           <div className="grid grid-cols-3 gap-6">
//             {searchResults.map((result, index) => (
//               <PropertyCard
//                 key={index}
//                 image={result.image || "/api/placeholder/300/200"}
//                 price={result.price}
//                 name={result.name}
//                 location={result.location}
//                 popular={result.popular}
//               />
//             ))}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// const PropertyCard = ({ image, price, name, location, popular, size = "small" }) => (
//   <div className={`bg-white rounded-xl overflow-hidden shadow-lg transition duration-300 hover:shadow-xl ${size === "large" ? "col-span-2 row-span-2" : ""}`}>
//     <div className="relative">
//       <img src={image} alt={name} className={`w-full object-cover ${size === "large" ? "h-96" : "h-48"}`} />
//       <span className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">${price}/night</span>
//       {popular && <span className="absolute top-4 right-4 bg-yellow-400 text-white px-3 py-1 rounded-full text-sm">Popular Choice</span>}
//     </div>
//     <div className="p-4">
//       <h3 className="font-semibold text-lg mb-1">{name}</h3>
//       <p className="text-gray-600">{location}</p>
//     </div>
//   </div>
// );

// const PropertyGrid = () => (
//   <section className="py-12 px-8 bg-gray-100">
//     <h2 className="text-2xl font-bold mb-8">Most Picked</h2>
//     <div className="grid grid-cols-3 gap-6">
//       <PropertyCard image="/api/placeholder/300/400" price={99} name="Blue Origin Farms" location="Indonesia" popular size="large" />
//       <PropertyCard image="/api/placeholder/300/200" price={129} name="Ocean View" location="Maldives" />
//       <PropertyCard image="/api/placeholder/300/200" price={105} name="Green Valley" location="Switzerland" />
//       <PropertyCard image="/api/placeholder/300/200" price={75} name="Wooden Pit" location="Canada" />
//       <PropertyCard image="/api/placeholder/300/200" price={110} name="Modern Vill" location="Japan" />
//     </div>
//     <div className="grid grid-cols-4 gap-6 mt-6">
//       <PropertyCard image="/api/placeholder/300/200" price={130} name="Shangri-La" location="Singapore" popular />
//       <PropertyCard image="/api/placeholder/300/200" price={85} name="Top View" location="Thailand" />
//       <PropertyCard image="/api/placeholder/300/200" price={140} name="Green Villa" location="Bali" />
//       <PropertyCard image="/api/placeholder/300/200" price={120} name="Wooden Pit" location="Norway" />
//     </div>
//   </section>
// );

// const HomePage = () => (
//   <div className="bg-gray-50 min-h-screen">
//     <Header />
//     <Hero />
//     <SearchBar />
//     <PropertyGrid />
//   </div>
// );

// export default HomePage;








import React, { useState, useEffect } from 'react';
import { Search, User, MapPin } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Header = () => {
  const [token, setToken] = useState(null);
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    if (storedToken) {
      console.log(storedToken)
      setToken(storedToken);
    }
  }, []);
  const [message, setMessage] = useState({ type: '', content: '' });

  const handleLogout = async() => {
    try {
      const url = `http://10.18.191.34:8000/student/api/logout/`;
      console.log('Sending request to:', url);
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': ' Token ' + localStorage.getItem('authToken')
        },
        body: JSON.stringify(''),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || JSON.stringify(responseData) || 'Logout failed');
      }

      console.log('Logout successful:', responseData);
      setMessage({ type: 'success', content: 'Logout successful!' });
      localStorage.removeItem('authToken');
      setToken(null);
    } catch (error) {
      console.error('Logout error:', error);
      setMessage({ type: 'error', content: error.message });
    }
  };

  return(
    <header className="flex justify-between items-center py-4 px-8 bg-white">
      <div className="text-2xl font-bold text-blue-600">CampusVacay.</div>
      <nav>
        <ul className="flex space-x-8">
          {['Home', 'Hotels', 'Rooms', 'About', 'Contact'].map((item) => (
            <li key={item} className="text-gray-600 hover:text-blue-600 cursor-pointer">{item}</li>
          ))}
        </ul>
      </nav>
      {token ? (
        <button onClick={handleLogout} className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition duration-300">
          Logout
        </button>
      ) : (
        <a href="/login" className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition duration-300">
          Login
        </a>
      )}
    </header>
  );
};

const Hero = () => (
  <section className="flex justify-between items-center py-12 px-8 bg-white">
    <div className="w-1/2 pr-12">
      <h1 className="text-4xl font-bold mb-4 leading-tight text-gray-800">Forget Busy Work,<br />Start Next Vacation</h1>
      <p className="text-gray-600 mb-8">Where dreams come true! Start your unforgettable journey with us. Book a vacation you'll never forget!</p>
      <button className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg hover:bg-blue-700 transition duration-300">Show More</button>
      <div className="flex space-x-12 mt-12">
        {[['2500+', 'stays'], ['250', 'cities'], ['100', 'locations']].map(([number, label]) => (
          <div key={label}>
            <strong className="text-2xl block text-blue-600">{number}</strong>
            <span className="text-gray-600">{label}</span>
          </div>
        ))}
      </div>
    </div>
    <div className="w-1/2">
      <img src="/api/placeholder/500/300" alt="Vacation room" className="rounded-2xl shadow-lg w-full h-auto" />
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

  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSearchData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setError(null);
    
    // Create the request body with only the necessary fields
    const requestBody = {
      location: searchData.location,
      check_in: searchData.check_in,  
      check_out: searchData.check_out,
      guests: searchData.guests
    };

    console.log('Sending request with:', requestBody); // Debug log

    try {
      const response = await fetch('http://10.18.191.34:8000/hotel/api/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('Response status:', response.status); // Debug log

      const data = await response.json();
      console.log('Response data:', data); // Debug log

      if (!response.ok) {
        throw new Error(data.detail || 'Search failed');
      }

      // Navigate to search page with results
      navigate('/search', { state: { searchResults: data } });

    } catch (error) {
      console.error('Search error:', error);
      setError('Failed to perform search. Please try again.');
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md max-w-4xl mx-auto -mt-8 relative z-10">
      <form onSubmit={handleSearch} className="flex flex-wrap gap-4">
        {/* Location Search */}
        <div className="flex-1 min-w-[200px]">
          <div className="flex items-center space-x-2">
            <MapPin size={20} className="text-gray-400" />
            <input
              type="text"
              name="location"
              value={searchData.location}
              onChange={handleChange}
              placeholder="Where are you going?"
              className="w-full p-2 focus:outline-none border-b"
            />
          </div>
        </div>

        {/* Check-in Date */}
        <div className="flex-1 min-w-[200px]">
          <div className="flex items-center space-x-2">
            <span className="text-gray-400">Check In</span>
            <input
              type="date"
              name="check_in"
              value={searchData.check_in}
              onChange={handleChange}
              className="w-full p-2 focus:outline-none border-b"
            />
          </div>
        </div>

        {/* Check-out Date */}
        <div className="flex-1 min-w-[200px]">
          <div className="flex items-center space-x-2">
            <span className="text-gray-400">Check Out</span>
            <input
              type="date"
              name="check_out"
              value={searchData.check_out}
              onChange={handleChange}
              className="w-full p-2 focus:outline-none border-b"
            />
          </div>
        </div>

        {/* Number of Guests */}
        <div className="flex-1 min-w-[150px]">
          <div className="flex items-center space-x-2">
            <User size={20} className="text-gray-400" />
            <select
              name="guests"
              value={searchData.guests}
              onChange={handleChange}
              className="w-full p-2 focus:outline-none border-b appearance-none"
            >
              <option value="">Select Guests</option>
              <option value="1">1 Guest</option>
              <option value="2">2 Guests</option>
              <option value="3">3 Guests</option>
              <option value="4">4 Guests</option>
              <option value="5">5+ Guests</option>
            </select>
          </div>
        </div>

        {/* Search Button */}
        <button 
          type="submit" 
          className="bg-blue-600 text-white px-8 py-3 rounded-full hover:bg-blue-700 transition duration-300 flex-shrink-0"
        >
          <Search className="inline mr-2" size={20} />
          Search
        </button>
      </form>

      {error && (
        <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
    </div>
  );
};

const PropertyCard = ({ image, price, name, location, popular, size = "small" }) => (
  <div className={`bg-white rounded-xl overflow-hidden shadow-lg transition duration-300 hover:shadow-xl ${size === "large" ? "col-span-2 row-span-2" : ""}`}>
    <div className="relative">
      <img src={image} alt={name} className={`w-full object-cover ${size === "large" ? "h-96" : "h-48"}`} />
      <span className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">${price}/night</span>
      {popular && <span className="absolute top-4 right-4 bg-yellow-400 text-white px-3 py-1 rounded-full text-sm">Popular Choice</span>}
    </div>
    <div className="p-4">
      <h3 className="font-semibold text-lg mb-1">{name}</h3>
      <p className="text-gray-600">{location}</p>
    </div>
  </div>
);

const PropertyGrid = () => (
  <section className="py-12 px-8 bg-gray-100">
    <h2 className="text-2xl font-bold mb-8">Most Picked</h2>
    <div className="grid grid-cols-3 gap-6">
      <PropertyCard image="/api/placeholder/300/400" price={99} name="Blue Origin Farms" location="Indonesia" popular size="large" />
      <PropertyCard image="/api/placeholder/300/200" price={129} name="Ocean View" location="Maldives" />
      <PropertyCard image="/api/placeholder/300/200" price={105} name="Green Valley" location="Switzerland" />
      <PropertyCard image="/api/placeholder/300/200" price={75} name="Wooden Pit" location="Canada" />
      <PropertyCard image="/api/placeholder/300/200" price={110} name="Modern Vill" location="Japan" />
    </div>
    <div className="grid grid-cols-4 gap-6 mt-6">
      <PropertyCard image="/api/placeholder/300/200" price={130} name="Shangri-La" location="Singapore" popular />
      <PropertyCard image="/api/placeholder/300/200" price={85} name="Top View" location="Thailand" />
      <PropertyCard image="/api/placeholder/300/200" price={140} name="Green Villa" location="Bali" />
      <PropertyCard image="/api/placeholder/300/200" price={120} name="Wooden Pit" location="Norway" />
    </div>
  </section>
);

const HomePage = () => (
  <div className="bg-gray-50 min-h-screen">
    <Header />
    <Hero />
    <SearchBar />
    <PropertyGrid />
  </div>
);

export default HomePage;