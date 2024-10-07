import React, { useState } from 'react';
import './Register.css';

function UserRegister() {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    email: '',
    phone: '',
    country: '',
    username: '',
    password: '',
    university_name: '',
    university_id: ''
  });

  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  }

  const handleSubmit = async(event) => {
    event.preventDefault();

    console.log(formData);
    try {
      const res = await fetch('http://3.16.159.54/student/api/register', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
      });

      if (!res.ok) {
          throw new Error('Network response was not ok');
      }

      const data = await res.json();
      setResponse(data);
      setError(null); // Clear previous errors
    } catch (err) {
        setError(err.message);
        setResponse(null); // Clear previous response
    }

    
    setFormData({
      name: '',
      age: '',
      email: '',
      phone: '',
      country: '',
      username: '',
      password: '',
      university_name: '',
      university_id: ''
    })
  };

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
        <h1>Student Account</h1>
        <form className="form" onSubmit={handleSubmit}>

          <div className="inline-block1">
          <h2 className="label-wrapper">
            <label>Name</label>
          </h2>
          <input
            type="text"
            id="student-name"
            className="input input__lg"
            name="name"
            value={formData.name}
            onChange={handleChange}
            autoComplete="off"
            placeholder="Enter your Name"
            required
          />
          </div>
          <div className="inline-block2">
          <h2 className="label-wrapper">
            <label>Age</label>
          </h2>
          <input
            type="text"
            id="student-age"
            className="input input__lg"
            name="age"
            value={formData.age}
            onChange={handleChange}
            autoComplete="off"
            placeholder="Enter Age"
            required
          />
          </div>
          <h2 className="label-wrapper">
            <label>University Email</label>
          </h2>
          <input
            type="text"
            id="student-email"
            className="input input__lg"
            name="email"
            value={formData.email}
            onChange={handleChange}
            autoComplete="off"
            placeholder="name@university.edu"
            required
          />
          <h2 className="label-wrapper">
            <label>Phone NO.</label>
          </h2>
          <input
            type="text"
            id="student-phone"
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
            id="student-country"
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
            id="student-username"
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
              id="student-password"
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
            <label>University Name</label>
          </h2>
          <input
            type="text"
            id="student-university-name"
            className="input input__lg"
            name="university_name"
            value={formData.university_name}
            onChange={handleChange}
            autoComplete="off"
            placeholder="Enter your University Name"
            required
          />

          <h2 className="label-wrapper">
            <label>University ID</label>
          </h2>
          <input
            type="text"
            id="student-university-id"
            className="input input__lg"
            name="university_id"
            value={formData.university_id}
            onChange={handleChange}
            autoComplete="off"
            placeholder="Enter University ID Number"
            required
          />
          <br/><br/>
          <label>By signing up you agree to <a href="">terms and conditions</a></label>
          <br/>

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



export default UserRegister;
