import React, { useState } from 'react';
import axios from 'axios';

const RBAC = () => {
    const [method, setMethod] = useState('GET');
    const [resourceType, setResourceType] = useState('');
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    const handleMethodChange = (e) => {
        setMethod(e.target.value);
    };

    const handleResourceTypeChange = (e) => {
        setResourceType(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('token');
            const url = `http://127.0.0.1:8000/api/${resourceType}/`;
            let res;
            if (method === 'GET') {
                res = await axios.get(url, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
            } else if (method === 'POST') {
                res = await axios.post(url, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
            } else if (method === 'PUT') {
                res = await axios.put(url, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
            } else if (method === 'DELETE') {
                res = await axios.delete(url, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
            }
            setResponse(res.data);
            setError(null);
        } catch (err) {
            setError(err.message);
            setResponse(null);
        }
    };

    return (
        <div>
            <h1>Test Connectivity</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Method:
                    <select value={method} onChange={handleMethodChange}>
                        <option value="GET">GET</option>
                        <option value="POST">POST</option>
                        <option value="PUT">PUT</option>
                        <option value="DELETE">DELETE</option>
                    </select>
                </label>
                <br />
                <label>
                    Resource Type:
                    <select value={resourceType} onChange={handleResourceTypeChange}>
                        <option value="">Select a resource</option>
                        <option value="clients">Clients</option>
                        <option value="bankaccounts">Bank Accounts</option>
                        <option value="transactions">Transactions</option>
                        <option value="employees">Employees</option>
                    </select>
                </label>
                <br />
                <button type="submit">Test Connectivity</button>
            </form>
            {response && (
                <div>
                    <h2>Response</h2>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
            {error && (
                <div>
                    <h2>Error</h2>
                    <pre>{error.includes('403') ? 'Prohibited' : error}</pre>
                </div>
            )}
        </div>
    );
};

export default RBAC;