import React, { useState } from 'react';
import './Register.css';

function HotelAccRegister() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    country: '',
    username: '',
    password: '',
    address: ''
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  }

  function handleSubmit(event) {
    event.preventDefault();
    console.log(formData);
    setFormData({
      name: '',
      email: '',
      phone: '',
      country: '',
      username: '',
      password: '',
      address: ''
    })
  }

  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
      setIsVisible(!isVisible);
  };

  return (
    <div className="container">
      <div className='left-panel'>
        <div className='logo'>CampusVacay.</div>
      </div>
      <div className='right-panel'>
        <h1>Hotel Account</h1>
        <form onSubmit={handleSubmit}>

          <h2 className="label-wrapper">
            <label>Hotel Name</label>
          </h2>
          <input
            type="text"
            id="hotel-name"
            className="input input__lg"
            name="name"
            value={formData.name}
            onChange={handleChange}
            autoComplete="off"
            placeholder="Enter hotel Name"
            required
          />
          
          <h2 className="label-wrapper">
            <label>Official Email</label>
          </h2>
          <input
            type="text"
            id="hotel-email"
            className="input input__lg"
            name="email"
            value={formData.email}
            onChange={handleChange}
            autoComplete="off"
            placeholder="name@gmail.com"
            required
          />
          <h2 className="label-wrapper">
            <label>Phone NO.</label>
          </h2>
          <input
            type="text"
            id="hotel-phone"
            className="input input__lg"
            name="phone"
            autoComplete="off"
            value={formData.phone}
            onChange={handleChange}
            placeholder="With Country Code"
            required
          />

          <h2 className="label-wrapper">
            <label>Country</label>
          </h2>
          <input
            type="text"
            id="hotel-country"
            className="input input__lg"
            name="country"
            autoComplete="off"
            value={formData.country}
            onChange={handleChange}
            placeholder="Country Name"
            required
          />

          <h2 className="label-wrapper">
            <label>Username</label>
          </h2>
          <input
            type="text"
            id="hotel-username"
            className="input input__lg"
            name="username"
            autoComplete="off"
            value={formData.username}
            onChange={handleChange}
            placeholder="Username"
            required
          />

          <h2 className="label-wrapper">
            <label>Password</label>
          </h2>
          <div>
          <div className='inline-block3'>
          <input
            type={isVisible ? 'text' : 'password'}
            id="hotel-password"
            className="input input__lg"
            name="password"
            autoComplete="off"
            value={formData.password}
            onChange={handleChange}
            placeholder="6+ characters"
            required
          /></div>
          <div className="inline-block4" onClick={toggleVisibility}>
            {isVisible ? 'Hide' : 'Show'}
          </div>
          </div>

          <h2 className="label-wrapper">
            <label>Hotel Address</label>
          </h2>
          <input
            type="text"
            id="hotel-address"
            className="input input__lg"
            name="address"
            value={formData.address}
            onChange={handleChange}
            autoComplete="off"
            placeholder="Enter hotel address"
            required
          />

          <button type="submit" className="btn btn__primary btn__lg">
            Register
          </button>
        </form>
        {/*render to login page*/}
        <div className='btn'><a href="">Login</a></div>
        <br/>
      </div>
    </div>
  );
}


export default HotelAccRegister;
