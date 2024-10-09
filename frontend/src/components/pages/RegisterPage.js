// import React, { useState } from 'react';
// import './Register.css';
// import { Link } from 'react-router-dom';
// import { Eye, EyeOff } from 'lucide-react';

// const RegisterForm = ({type}) => {
//   const [formData, setFormData] = useState({
//     name: '',
//     age: '',
//     email: '',
//     phone: '',
//     country: '',
//     username: '',
//     password: '',
//     university_name: '',
//     university_id: '',
//     file: ''
//   });

//   const [response, setResponse] = useState(null);
//   const [error, setError] = useState(null);

//   function handleChange(event) {
//     const { name, value } = event.target;
//     setFormData({
//       ...formData,
//       [name]: value
//     });
//   }

//   const handleSubmit = async(event) => {
//     event.preventDefault();
//     console.log(formData);
//     const test={
//       "username": formData.username,
//       "password": formData.password,
//       "first_name": formData.name,
//       "last_name": formData.name,
//       "email": formData.email,
//       "dob": "1999-06-16",
//       "phone_number": formData.phone,
//       "address": "testaddress",
//       "university_name": formData.university_name,
//       "university_id_proof": formData.file
//     }
//     console.log(test);
//     try {
//       const res = await fetch('http://3.16.159.54/student/api/register/', {
//           method: 'POST',
//           headers: {
//               'Content-Type': 'application/json',
//           },
//           body: JSON.stringify(test),
//       });

//       if (!res.ok) {
//         const data = await res.json();
//         console.log(data);
//         throw new Error('Network response was not ok');
//       }
      
//       setError(null); 
//     } catch (err) {
//         setError(err.message);
//         setResponse(null); 
//     }

    
//     setFormData({
//       name: '',
//       age: '',
//       email: '',
//       phone: '',
//       country: '',
//       username: '',
//       password: '',
//       university_name: '',
//       university_id: '',
//       file: ''
//     })
//   };

//   const [showPassword, setShowPassword] = useState(true);


//   return (
//       <div className="right-panel">
//         <h1>Student Account</h1>
//         <form className="form" onSubmit={handleSubmit}>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
//             Name
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="name"
//             type="text"
//             name="name"
//             value={formData.name}
//             onChange={handleChange}
//             placeholder="Enter your Name"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="age">
//             Age
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="age"
//             type="text"
//             name="age"
//             value={formData.age}
//             onChange={handleChange}
//             placeholder="Enter age"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
//             University Email
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="email"
//             type="text"
//             name="email"
//             value={formData.email}
//             onChange={handleChange}
//             placeholder="name@university.edu"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="phone">
//             Phone No.
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="phone"
//             type="text"
//             name="phone"
//             value={formData.phone}
//             onChange={handleChange}
//             placeholder="With Country Code"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="country">
//             Country
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="country"
//             type="text"
//             name="country"
//             value={formData.country}
//             onChange={handleChange}
//             placeholder="Country Name"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
//             Username
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="username"
//             type="text"
//             name="username"
//             value={formData.username}
//             onChange={handleChange}
//             placeholder="Username"
//           />
//           </div>

//           <div className="mb-6 relative">
//             <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
//               Password
//             </label>
//             <input
//               className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
//               id="password"
//               name="password"
//               type={showPassword ? "text" : "password"}
//               value={formData.password}
//               onChange={handleChange}
//               placeholder="6+ characters"
//             />
//             <button
//               type="button"
//               className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6"
//               onClick={() => setShowPassword(!showPassword)}
//             >
//               {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
//             </button>
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="university_name">
//             University Name
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="university_name"
//             type="text"
//             name="university_name"
//             value={formData.university_name}
//             onChange={handleChange}
//             placeholder="Enter your University Name"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="university_id">
//             University ID
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="university_id"
//             type="text"
//             name="university_id"
//             value={formData.university_id}
//             onChange={handleChange}
//             placeholder="Enter University ID Number"
//           />
//           </div>

//           <input className="hidden" type="file" value={formData.file} onChange={handleChange} id="file" name="file" accept="image/png, image/jpeg, application/pdf" />

      
//           <br/><br/>
//           <label>By signing up you agree to <a href="#">terms and conditions</a></label>
//           <br/>

//           <button type="submit" className="btn btn__primary btn__lg">
//             Register
//           </button>
//           <Link to="/login" className="font-bold text-blue-500 hover:text-blue-800">
//             Login
//           </Link>
//         </form>
        
//       </div>
    
//   );
// };

// const HotelRegisterForm = ({type}) => {
//   const [formData, setFormData] = useState({
//     name: '',
//     age: '',
//     email: '',
//     phone: '',
//     country: '',
//     username: '',
//     password: '',
//     university_name: '',
//     university_id: '',
//     file: ''
//   });

//   const [response, setResponse] = useState(null);
//   const [error, setError] = useState(null);

//   function handleChange(event) {
//     const { name, value } = event.target;
//     setFormData({
//       ...formData,
//       [name]: value
//     });
//   }

//   const handleSubmit = async(event) => {
//     event.preventDefault();
    
//     const test={
//       "username": formData.username,
//       "password": formData.password,
//       "first_name": formData.name,
//       "last_name": formData.name,
//       "email": formData.email,
//       "dob": "1999-06-16",
//       "phone_number": formData.phone,
//       "address": "testaddress",
//       "university_name": formData.university_name,
//       "university_id_proof": formData.file
//     }

//     try {
//       const res = await fetch('http://3.16.159.54/student/api/register/', {
//           method: 'POST',
//           headers: {
//               'Content-Type': 'application/json',
//           },
//           body: JSON.stringify(test),
//       });

//       if (!res.ok) {
//         const data = await res.json();
//         throw new Error('Network response was not ok');
//       }
      
//       setError(null); 
//     } catch (err) {
//         setError(err.message);
//         setResponse(null); 
//     }

    
//     setFormData({
//       name: '',
//       age: '',
//       email: '',
//       phone: '',
//       country: '',
//       username: '',
//       password: '',
//       university_name: '',
//       university_id: '',
//       file: ''
//     })
//   };

//   const [showPassword, setShowPassword] = useState(true);


//   return (
//       <div className='right-panel'>
//         <h1>Hotel Account</h1>
//         <form className="form" onSubmit={handleSubmit}>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
//             Hotel Name
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="name"
//             type="text"
//             name="name"
//             value={formData.name}
//             onChange={handleChange}
//             placeholder="Enter Hotel Name"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
//             Official Email
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="email"
//             type="text"
//             name="email"
//             value={formData.email}
//             onChange={handleChange}
//             placeholder="name@gmail.com"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="phone">
//             Phone No.
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="phone"
//             type="text"
//             name="phone"
//             value={formData.phone}
//             onChange={handleChange}
//             placeholder="With Country Code"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="country">
//             Country
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="country"
//             type="text"
//             name="country"
//             value={formData.country}
//             onChange={handleChange}
//             placeholder="Country Name"
//           />
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
//             Username
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="username"
//             type="text"
//             name="username"
//             value={formData.username}
//             onChange={handleChange}
//             placeholder="Username"
//           />
//           </div>

//           <div className="mb-6 relative">
//             <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
//               Password
//             </label>
//             <input
//               className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
//               id="password"
//               name="password"
//               type={showPassword ? "text" : "password"}
//               value={formData.password}
//               onChange={handleChange}
//               placeholder="6+ characters"
//             />
//             <button
//               type="button"
//               className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6"
//               onClick={() => setShowPassword(!showPassword)}
//             >
//               {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
//             </button>
//           </div>

//           <div className="mb-4">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="address">
//             Hotel Address
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//             id="address"
//             type="text"
//             name="address"
//             value={formData.address}
//             onChange={handleChange}
//             placeholder="Enter Hotel Address"
//           />
//           </div>

//           <input className="hidden" type="file" value={formData.file} onChange={handleChange} id="file" name="file" accept="image/png, image/jpeg, application/pdf" />

      
//           <br/><br/>
//           <label>By signing up you agree to <a href="#">terms and conditions</a></label>
//           <br/>

//           <button type="submit" className="btn btn__primary btn__lg">
//             Register
//           </button>
//           <Link to="/login" className="content-center font-bold text-blue-500 hover:text-blue-800">
//             Login
//           </Link>
//         </form>
        
//       </div>
    
//   );
// };

// function RegisterPage() {
//   const [loginType, setLoginType] = useState('Student');

//   return (
//     <div className="min-h-screen bg-gray-100 flex items-center justify-center">
//       <div className="bg-white p-8 rounded-lg shadow-md flex w-full">
//         <div className="w-1/2 bg-cover bg-center rounded-l-lg" style={{backgroundImage: "url('/api/placeholder/600/800')"}}>
//           <div className="h-full w-full bg-blue-500 bg-opacity-50 flex items-center justify-center rounded-l-lg">
//             <h1 className="text-4xl font-bold text-white">CampusVacay.</h1>
//           </div>
//         </div>
//         <div className="w-1/2 p-8">
//           <div className="flex justify-end mb-4">
//             <div className="relative inline-block w-10 mr-2 align-middle select-none">
//               <input
//                 type="checkbox"
//                 name="toggle"
//                 id="toggle"
//                 className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
//                 onChange={() => setLoginType(loginType === 'Student' ? 'Hotel' : 'Student')}
//               />
//               <label
//                 htmlFor="toggle"
//                 className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"
//               ></label>
//             </div>
//             <span className="text-gray-700">{loginType}</span>
//           </div>
//           {loginType=='Student' ? (
//             <RegisterForm/>
//           ) : (
//             <HotelRegisterForm/>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }



// export default RegisterPage;





import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';

const RegisterForm = ({ type }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    email: '',
    dob: '',
    phone_number: '',
    address: '',
    university_name: '',
    university_id_proof: null
  });

  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState({ type: '', content: '' });

  const handleChange = (event) => {
    const { name, value, type, files } = event.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'file' ? files[0] : value
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage({ type: '', content: '' });

    const formDataToSend = new FormData();
    Object.keys(formData).forEach(key => {
      if (key === 'university_id_proof') {
        if (formData[key]) {
          formDataToSend.append(key, formData[key]);
        }
      } else {
        formDataToSend.append(key, formData[key]);
      }
    });

    try {
      const url = `http://3.16.159.54/${type.toLowerCase()}/api/register/`;
      console.log('Sending request to:', url);
      console.log('Request data:', Object.fromEntries(formDataToSend));

      const response = await fetch(url, {
        method: 'POST',
        body: formDataToSend,
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries(response.headers.entries()));

      const responseText = await response.text();
      console.log('Full response text:', responseText);

      let responseData;
      try {
        responseData = JSON.parse(responseText);
        console.log('Parsed JSON response:', responseData);
      } catch (e) {
        console.error('Error parsing JSON:', e);
        setMessage({ type: 'error', content: 'Server returned an unexpected response. Please try again.' });
        return;
      }

      if (!response.ok) {
        // Handle validation errors
        if (response.status === 400 && typeof responseData === 'object') {
          const errorMessages = Object.entries(responseData)
            .map(([key, value]) => `${key}: ${value.join(', ')}`)
            .join('; ');
          throw new Error(errorMessages);
        } else {
          throw new Error(responseData.detail || JSON.stringify(responseData) || 'Registration failed');
        }
      }

      console.log('Registration successful:', responseData);
      setMessage({ type: 'success', content: 'Registration successful!' });
    } catch (error) {
      console.error('Registration error:', error);
      setMessage({ type: 'error', content: error.message });
    }
  };

  const renderField = (name, label, type = 'text') => (
    <div className="mb-4" key={name}>
      <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={name}>
        {label}
      </label>
      <input
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        id={name}
        type={type}
        name={name}
        value={formData[name]}
        onChange={handleChange}
        placeholder={`Enter ${label.toLowerCase()}`}
      />
    </div>
  );

  return (
    <div className="w-full max-w-md">
      <h2 className="text-2xl font-bold mb-6">{type} Registration</h2>
      <form onSubmit={handleSubmit}>
        {renderField('username', 'Username')}
        <div className="mb-6 relative">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
            Password
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
            id="password"
            name="password"
            type={showPassword ? "text" : "password"}
            value={formData.password}
            onChange={handleChange}
            placeholder="6+ characters"
          />
          <button
            type="button"
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
          </button>
        </div>
        {renderField('first_name', 'First Name')}
        {renderField('last_name', 'Last Name')}
        {renderField('email', 'Email', 'email')}
        {renderField('dob', 'Date of Birth', 'date')}
        {renderField('phone_number', 'Phone Number')}
        {renderField('address', 'Address')}
        {type === 'Student' && (
          <>
            {renderField('university_name', 'University Name')}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="university_id_proof">
                University ID Proof
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                type="file"
                id="university_id_proof"
                name="university_id_proof"
                onChange={(e) => {
                  const file = e.target.files[0];
                  console.log('Selected file:', file);
                  setFormData({ ...formData, university_id_proof: file });
                }}
                accept="image/png, image/jpeg, application/pdf"
              />
            </div>
          </>
        )}

        {message.content && (
          <div className={`mt-4 p-2 ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
            {message.content}
          </div>
        )}

        <div className="flex items-center justify-between mt-6">
          <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Register
          </button>
          <Link to="/login" className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
            Login
          </Link>
        </div>
      </form>
    </div>
  );
};

const RegisterPage = () => {
  const [registerType, setRegisterType] = useState('Student');

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md flex w-full max-w-4xl">
        <div className="w-1/2 bg-cover bg-center rounded-l-lg" style={{backgroundImage: "url('/api/placeholder/600/800')"}}>
          <div className="h-full w-full bg-blue-500 bg-opacity-50 flex items-center justify-center rounded-l-lg">
            <h1 className="text-4xl font-bold text-white">CampusVacay.</h1>
          </div>
        </div>
        <div className="w-1/2 p-8">
          <div className="flex justify-end mb-4">
            <div className="relative inline-block w-10 mr-2 align-middle select-none">
              <input
                type="checkbox"
                name="toggle"
                id="toggle"
                className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                onChange={() => setRegisterType(registerType === 'Student' ? 'Hotel' : 'Student')}
              />
              <label
                htmlFor="toggle"
                className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"
              ></label>
            </div>
            <span className="text-gray-700">{registerType} Registration</span>
          </div>
          <RegisterForm type={registerType} />
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;