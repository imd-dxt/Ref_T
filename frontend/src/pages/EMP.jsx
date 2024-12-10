import React, { useState } from 'react';
import axios from 'axios';
import './EMP.css';

const EMP = ({ token }) => {
  const [requestType, setRequestType] = useState('');
  const [resourceType, setResourceType] = useState('');
  const [queryParams, setQueryParams] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const apiUrl = `http://localhost:8000/api/${resourceType}/?${queryParams}`;

    try {
      let res;
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };

      if (requestType === 'GET') {
        res = await axios.get(apiUrl, config);
      } else if (requestType === 'POST') {
        res = await axios.post(apiUrl, {}, config);
      }

      setResponse(res.data);
      setError(null);
    } catch (error) {
      if (error.response && error.response.status === 403) {
        setError('You are not allowed to make this request.');
      } else {
        setError('Error with API: ' + (error.response?.data || error.message));
      }
      setResponse(null);
    }
  };

  return (
    <div className="container">
      <div className="title">
        <h1>Request Form</h1>
      </div>
      <form className="form-style" onSubmit={handleSubmit}>
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

        <label htmlFor="resourceType">Resource Type</label>
        <select
          id="resourceType"
          value={resourceType}
          onChange={(e) => setResourceType(e.target.value)}
          required
        >
          <option value="" disabled>
            Select Resource Type
          </option>
          <option value="employees">Employee</option>
          <option value="bankaccounts">Bank Account</option>
          <option value="clients">Client</option>
        </select>

        <label htmlFor="queryParams">Query Parameters</label>
        <input
          id="queryParams"
          type="text"
          value={queryParams}
          onChange={(e) => setQueryParams(e.target.value)}
          placeholder="Enter query parameters"
          required
        />

        <button type="submit">Submit</button>
      </form>
      {error && <div className="error">{error}</div>}
      {response && (
        <div className="response">
          <h2>Response</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default EMP;