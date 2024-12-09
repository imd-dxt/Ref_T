import React, { useState } from "react";
import axios from "axios"; // Optional, use fetch if not installing axios
import "./App.css";

const App = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Example API endpoint for authentication
    const apiUrl = "http://localhost:8000/api/login"; // Replace with your authentication endpoint

    // Create the request body as JSON
    const requestData = {
      email,
      password,
    };

    console.log("JSON Request Data:", JSON.stringify(requestData, null, 2));

    try {
      // Using Axios to send a POST request to your API
      const response = await axios.post(apiUrl, requestData);

      console.log("Authentication Response:", response.data);

      // Handle successful login
      alert("Login successful!");
    } catch (error) {
      console.error("Error during authentication:", error.response?.data || error.message);

      // Handle login failure
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
