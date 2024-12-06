import React, { useState } from 'react';
import axios from "axios";
import './EMP.css';

const EMP = () => {
  const [requestType, setRequestType] = useState("");
  const [name, setName] = useState("");
  const [userID, setUserID] = useState("");
  const [organizationID, setOrganizationID] = useState("");
  const [role, setRole] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const apiUrl = "http://localhost:8000/api/employees/";

    try {
      let response;
      if (requestType === "GET") {
        response = await axios.get(apiUrl,{params: { name, userID, organizationID, role }});
      } else if (requestType === "POST") {
        response = await axios.post(apiUrl, { name, userID, organizationID, role });
      }

      console.log("API Response:", response.data);
    } catch (error) {
      console.error("Error with API:", error.response?.data || error.message);
    }
  };

  return (
    <div className="container">
        <div className='title'><h1>Request Form</h1></div>
        <div></div>
        <form className='form-style' onSubmit={handleSubmit}>
          <label htmlFor="requestType">Request Type</label>
          <select
            id="requestType"
            value={requestType}
            onChange={(e) => setRequestType(e.target.value)}
            required
          >
            <option value="" disabled>
              Select Request Type
            </option>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
          </select>

          <label htmlFor="name">Name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter the name"
            required
          />

          <label htmlFor="userID">User ID</label>
          <input
            id="userID"
            type="text"
            value={userID}
            onChange={(e) => setUserID(e.target.value)}
            placeholder="Enter the user ID"
            required
          />

          <label htmlFor="organizationID">Organization ID</label>
          <input
            id="organizationID"
            type="text"
            value={organizationID}
            onChange={(e) => setOrganizationID(e.target.value)}
            placeholder="Enter the organization ID"
            required
          />

          <label htmlFor="role">Role</label>
          <input
            id="role"
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="Enter the role"
            required
          />
          <button type="submit">Submit</button>
        </form>
    </div>
    
  );
};
export default EMP;