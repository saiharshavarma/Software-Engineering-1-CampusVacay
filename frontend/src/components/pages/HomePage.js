import React from 'react';
import { Search, User, MapPin } from 'lucide-react';

const Header = () => (
  <header className="flex justify-between items-center py-4 px-8 bg-white">
    <div className="text-2xl font-bold text-blue-600">CampusVacay.</div>
    <nav>
      <ul className="flex space-x-8">
        {['Home', 'Hotels', 'Rooms', 'About', 'Contact'].map((item) => (
          <li key={item} className="text-gray-600 hover:text-blue-600 cursor-pointer">{item}</li>
        ))}
      </ul>
    </nav>
    <button className="bg-blue-600 text-white px-6 py-2 rounded-full hover:bg-blue-700 transition duration-300">Login</button>
  </header>
);

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

const SearchBar = () => (
  <div className="bg-white p-4 rounded-full shadow-md flex justify-between items-center space-x-4 max-w-4xl mx-auto -mt-8 relative z-10">
    <div className="flex items-center space-x-2 flex-grow">
      <Search size={20} className="text-gray-400" />
      <input type="text" placeholder="Check Available" className="w-full p-2 focus:outline-none" />
    </div>
    <div className="flex items-center space-x-2 border-l border-r px-4">
      <User size={20} className="text-gray-400" />
      <select className="p-2 focus:outline-none appearance-none">
        <option>Person 2</option>
        <option>Person 1</option>
        <option>Person 3</option>
        <option>Person 4</option>
      </select>
    </div>
    <div className="flex items-center space-x-2 flex-grow">
      <MapPin size={20} className="text-gray-400" />
      <input type="text" placeholder="Select Location" className="w-full p-2 focus:outline-none" />
    </div>
    <button className="bg-blue-600 text-white px-8 py-3 rounded-full hover:bg-blue-700 transition duration-300">Search</button>
  </div>
);

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