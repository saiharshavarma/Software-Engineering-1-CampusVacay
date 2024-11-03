
// import React, { useState } from 'react';
// import { Link } from 'react-router-dom';
// import { Eye, EyeOff } from 'lucide-react';

// const RegisterForm = ({ type }) => {
//   const [formData, setFormData] = useState({
//     username: '',
//     password: '',
//     first_name: '',
//     last_name: '',
//     email: '',
//     dob: '',
//     phone_number: '',
//     address: '',
//     university_name: '',
//     university_id_proof: null
//   });

//   const [showPassword, setShowPassword] = useState(false);
//   const [message, setMessage] = useState({ type: '', content: '' });

//   const handleChange = (event) => {
//     const { name, value, type, files } = event.target;
//     setFormData(prevState => ({
//       ...prevState,
//       [name]: type === 'file' ? files[0] : value
//     }));
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     setMessage({ type: '', content: '' });

//     const formDataToSend = new FormData();
//     Object.keys(formData).forEach(key => {
//       if (key === 'university_id_proof') {
//         if (formData[key]) {
//           formDataToSend.append(key, formData[key]);
//         }
//       } else {
//         formDataToSend.append(key, formData[key]);
//       }
//     });

//     try {
//       const url = `http://3.16.159.54/${type.toLowerCase()}/api/register/`;
//       console.log('Sending request to:', url);
//       console.log('Request data:', Object.fromEntries(formDataToSend));

//       const response = await fetch(url, {
//         method: 'POST',
//         body: formDataToSend,
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
//         // Handle validation errors
//         if (response.status === 400 && typeof responseData === 'object') {
//           const errorMessages = Object.entries(responseData)
//             .map(([key, value]) => `${key}: ${value.join(', ')}`)
//             .join('; ');
//           throw new Error(errorMessages);
//         } else {
//           throw new Error(responseData.detail || JSON.stringify(responseData) || 'Registration failed');
//         }
//       }

//       console.log('Registration successful:', responseData);
//       setMessage({ type: 'success', content: 'Registration successful!' });
//     } catch (error) {
//       console.error('Registration error:', error);
//       setMessage({ type: 'error', content: error.message });
//     }
//   };

//   const renderField = (name, label, type = 'text') => (
//     <div className="mb-4" key={name}>
//       <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={name}>
//         {label}
//       </label>
//       <input
//         className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//         id={name}
//         type={type}
//         name={name}
//         value={formData[name]}
//         onChange={handleChange}
//         placeholder={`Enter ${label.toLowerCase()}`}
//       />
//     </div>
//   );

//   return (
//     <div className="w-full max-w-md">
//       <h2 className="text-2xl font-bold mb-6">{type} Registration</h2>
//       <form onSubmit={handleSubmit}>
//         {renderField('username', 'Username')}
//         <div className="mb-6 relative">
//           <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
//             Password
//           </label>
//           <input
//             className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline pr-10"
//             id="password"
//             name="password"
//             type={showPassword ? "text" : "password"}
//             value={formData.password}
//             onChange={handleChange}
//             placeholder="6+ characters"
//           />
//           <button
//             type="button"
//             className="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5 mt-6"
//             onClick={() => setShowPassword(!showPassword)}
//           >
//             {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
//           </button>
//         </div>
//         {renderField('first_name', 'First Name')}
//         {renderField('last_name', 'Last Name')}
//         {renderField('email', 'Email', 'email')}
//         {renderField('dob', 'Date of Birth', 'date')}
//         {renderField('phone_number', 'Phone Number')}
//         {renderField('address', 'Address')}
//         {type === 'Student' && (
//           <>
//             {renderField('university_name', 'University Name')}
//             <div className="mb-4">
//               <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="university_id_proof">
//                 University ID Proof
//               </label>
//               <input
//                 className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//                 type="file"
//                 id="university_id_proof"
//                 name="university_id_proof"
//                 onChange={(e) => {
//                   const file = e.target.files[0];
//                   console.log('Selected file:', file);
//                   setFormData({ ...formData, university_id_proof: file });
//                 }}
//                 accept="image/png, image/jpeg, application/pdf"
//               />
//             </div>
//           </>
//         )}

//         {message.content && (
//           <div className={`mt-4 p-2 ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
//             {message.content}
//           </div>
//         )}

//         <div className="flex items-center justify-between mt-6">
//           <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
//             Register
//           </button>
//           <Link to="/login" className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800">
//             Login
//           </Link>
//         </div>
//       </form>
//     </div>
//   );
// };

// const RegisterPage = () => {
//   const [registerType, setRegisterType] = useState('Student');

//   return (
//     <div className="min-h-screen bg-gray-100 flex items-center justify-center">
//       <div className="bg-white p-8 rounded-lg shadow-md flex w-full max-w-4xl">
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
//                 onChange={() => setRegisterType(registerType === 'Student' ? 'Hotel' : 'Student')}
//               />
//               <label
//                 htmlFor="toggle"
//                 className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"
//               ></label>
//             </div>
//             <span className="text-gray-700">{registerType} Registration</span>
//           </div>
//           <RegisterForm type={registerType} />
//         </div>
//       </div>
//     </div>
//   );
// };

// export default RegisterPage;



import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Register.css';

function RegisterPage() {
  const [registerType, setRegisterType] = useState('Student');
  const [formData, setFormData] = useState(
    registerType === 'Student'
      ? {
          username: '',
          password: '',
          first_name: '',
          last_name: '',
          email: '',
          dob: null,
          phone_number: '',
          address: '',
          university_name: '',
          university_id_proof: null
        }
      : {
          username: '',
          password: '',
          email: '',
          hotel_name: '',
          phone_number: '',
          address: '',
          description: '',
          facilities: '',
          check_in_time: null,
          check_out_time: null,
          cancellation_policy: '',
          student_discount: null,
          special_offers: ''
        }
  );

  const [message, setMessage] = useState({ type: '', content: '' });
  const [isVisible, setIsVisible] = useState(false);

  function handleChange(event) {
    const { name, value, type, files } = event.target;
    setFormData({
      ...formData,
      [name]: type === 'file' ? files[0] : value
    });
  }

  async function handleSubmit(event) {
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
      const url = `http://10.18.191.34:8000/${registerType.toLowerCase()}/api/register/`;
      const response = await fetch(url, {
        method: 'POST',
        body: formDataToSend,
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.detail || JSON.stringify(responseData));
      }

      console.log('Registration successful:', responseData);
      setMessage({ type: 'success', content: 'Registration successful!' });
    } catch (error) {
      console.error('Registration error:', error);
      setMessage({ type: 'error', content: error.message });
    }
  }

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const renderField = (name, label, type = 'text') => (
    <>
      <h2 className="label-wrapper">
        <label>{label}</label>
      </h2>
      {type === 'textarea' ? (
        <textarea
          id={name}
          className="input input__lg"
          name={name}
          value={formData[name]}
          onChange={handleChange}
          autoComplete="off"
          placeholder={`Enter ${label.toLowerCase()}`}
        />
      ) : (
        <input
          type={type}
          id={name}
          className="input input__lg"
          name={name}
          value={formData[name]}
          onChange={handleChange}
          autoComplete="off"
          placeholder={`Enter ${label.toLowerCase()}`}
        />
      )}
    </>
  );

  return (
    <form onSubmit={handleSubmit}>
      <div className="container">
        <div className='left-panel'>
          <h1>CampusVacay.</h1>
          <div className="flex justify-end mb-4">
            <div className="relative inline-block w-10 mr-2 align-middle select-none">
              <input
                type="checkbox"
                name="toggle"
                id="toggle"
                className="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                onChange={() => {
                  setRegisterType(registerType === 'Student' ? 'Hotel' : 'Student');
                  setFormData(registerType === 'Student'
                    ? {
                        username: '',
                        password: '',
                        email: '',
                        hotel_name: '',
                        phone_number: '',
                        address: '',
                        description: '',
                        facilities: '',
                        check_in_time: null,
                        check_out_time: null,
                        cancellation_policy: '',
                        student_discount: null,
                        special_offers: ''
                      }
                    : {
                        username: '',
                        password: '',
                        first_name: '',
                        last_name: '',
                        email: '',
                        dob: null,
                        phone_number: '',
                        address: '',
                        university_name: '',
                        university_id_proof: null
                      }
                  );
                }}
              />
              <label
                htmlFor="toggle"
                className="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"
              ></label>
            </div>
            <span className="text-gray-700">{registerType} Registration</span>
          </div>
        </div>
        <div className='right-panel'>
          <h1>{registerType} Registration</h1>
          {renderField('username', 'Username')}
          <h2 className="label-wrapper">
            <label>Password</label>
          </h2>
          <div>
            <div className='inline-block3'>
              <input
                type={isVisible ? 'text' : 'password'}
                id="password"
                className="input input__lg"
                name="password"
                autoComplete="off"
                value={formData.password}
                onChange={handleChange}
                placeholder="6+ characters"
              />
            </div>
            <div className="inline-block4" onClick={toggleVisibility}>
              {isVisible ? 'Hide' : 'Show'}
            </div>
          </div>
          {renderField('email', 'E-mail', 'email')}
          {registerType === 'Student' ? (
            <>
              {renderField('first_name', 'First Name')}
              {renderField('last_name', 'Last Name')}
              {renderField('dob', 'Date of Birth', 'date')}
              {renderField('phone_number', 'Phone Number')}
              {renderField('address', 'Address')}
              {renderField('university_name', 'University Name')}
              <h2 className="label-wrapper">
                <label>University ID Proof</label>
              </h2>
              <input
                type="file"
                id="university_id_proof"
                className="input input__lg"
                name="university_id_proof"
                onChange={handleChange}
                accept="image/png, image/jpeg, application/pdf"
              />
            </>
          ) : (
            <>
              {renderField('hotel_name', 'Hotel Name')}
              {renderField('phone_number', 'Phone Number')}
              {renderField('address', 'Address')}
              {renderField('description', 'Description', 'textarea')}
              {renderField('facilities', 'Facilities')}
              {renderField('check_in_time', 'Check-in Time', 'time')}
              {renderField('check_out_time', 'Check-out Time', 'time')}
              {renderField('cancellation_policy', 'Cancellation Policy', 'textarea')}
              {renderField('student_discount', 'Student Discount (%)', 'number')}
              {renderField('special_offers', 'Special Offers', 'textarea')}
            </>
          )}
          <button type="submit" className="btn btn__primary btn__lg">
            Register
          </button>
          {message.content && (
            <div className={`mt-4 p-2 ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {message.content}
            </div>
          )}
          <div className='btn'>
            <Link to="/login">Login</Link>
          </div>
        </div>
      </div>
    </form>
  );
}

export default RegisterPage;