import React, { useState } from "react";
import axios from "axios"; 
import { useNavigate } from "react-router-dom";

const App = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // For redirection
  const handleSubmit = async (e) => {
    e.preventDefault();

    
    const apiUrl = "http://localhost:8000/auth/login/"; // Replace with your authentication endpoint

    const requestData = {
      email,
      password,
    };

    console.log("JSON Request Data:", JSON.stringify(requestData, null, 2));

    try {
      const response = await axios.post(apiUrl, { email, password });

      // Save JWT token to localStorage
      localStorage.setItem("accessToken", response.data.jwt);

      
      navigate("/User");
    } catch (error) {
      console.error("Login error:", error.response?.data || error.message);
      alert("Login failed. Please check your credentials.");
    }
  };

  return (
    <div className="container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
        />

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default App;
