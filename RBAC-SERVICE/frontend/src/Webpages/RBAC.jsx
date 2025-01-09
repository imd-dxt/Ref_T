import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/base.css';
import '../styles/RBAC.css';
const RBAC = () => {
    const [method, setMethod] = useState('GET');
    const [resourceType, setResourceType] = useState('');
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    const [userPermissions, setUserPermissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({});

    useEffect(() => {
        const fetchUserPermissions = async () => {
            try {
                const token = localStorage.getItem('token');
                console.log('Fetching permissions with token:', token);
                const response = await axios.get('http://127.0.0.1:8000/api/user-permissions/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                console.log('Received permissions:', response.data);
                setUserPermissions(response.data);
            } catch (err) {
                console.error('Error fetching permissions:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchUserPermissions();
    }, []);

    const hasPermission = (action, resource) => {
        if (!resource) return true;
        console.log(`Checking permission for ${action} on ${resource}`);
        console.log('Current permissions:', userPermissions);
        
        const permissionMap = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'DELETE': 'delete'
        };
        
        const permissionName = `${permissionMap[action]}_${resource.slice(0, -1)}`;
        console.log('Looking for permission:', permissionName);
        return userPermissions.includes(permissionName);
    };

    const handleMethodChange = (e) => {
        console.log('Method changed to:', e.target.value);
        setMethod(e.target.value);
        setFormData({});
    };

    const handleResourceTypeChange = (e) => {
        console.log('Resource type changed to:', e.target.value);
        setResourceType(e.target.value);
        setMethod('GET');
        setFormData({});
    };

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const renderResourceForm = () => {
        if (method === 'GET') return null;

        if (method === 'DELETE') {
            return (
                <div className="form-group">
                    <label>
                        ID to Delete:
                        <input
                            type="text"
                            name="id"
                            value={formData.id || ''}
                            onChange={handleInputChange}
                            required
                        />
                    </label>
                </div>
            );
        }

        if (method === 'POST') {
            switch (resourceType) {
                case 'clients':
                    return (
                        <div className="form-group">
                            <label>
                                Full Name:
                                <input
                                    type="text"
                                    name="full_name"
                                    value={formData.full_name || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Email:
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Phone:
                                <input
                                    type="text"
                                    name="phone"
                                    pattern="\d{10}"
                                    value={formData.phone || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                ID Number:
                                <input
                                    type="text"
                                    name="IDnumber"
                                    value={formData.IDnumber || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                        </div>
                    );
                case 'bankaccounts':
                    return (
                        <div className="form-group">
                            <label>
                                Client:
                                <input
                                    type="number"
                                    name="client"
                                    value={formData.client || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Balance:
                                <input
                                    type="number"
                                    name="balance"
                                    step="0.01"
                                    value={formData.balance || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                        </div>
                    );
                case 'transactions':
                    return (
                        <div className="form-group">
                            <label>
                                Transaction Type:
                                <select
                                    name="transaction_type"
                                    value={formData.transaction_type || ''}
                                    onChange={handleInputChange}
                                    required
                                >
                                    <option value="">Select type</option>
                                    <option value="DEPOSIT">Deposit</option>
                                    <option value="RETRIEVE">Retrieve</option>
                                </select>
                            </label>
                            <label>
                                Account:
                                <input
                                    type="number"
                                    name="source_account_id"
                                    value={formData.source_account_id || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Amount:
                                <input
                                    type="number"
                                    name="amount"
                                    step="0.01"
                                    value={formData.amount || ''}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                        </div>
                    );
                default:
                    return null;
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setResponse(null);

        if (!resourceType) {
            setError('Please select a resource type');
            return;
        }

        try {
            const token = localStorage.getItem('token');
            let url = `http://127.0.0.1:8000/api/${resourceType}/`;
            
            if (method === 'DELETE') {
                if (!formData.id) {
                    setError('Please provide an ID to delete');
                    return;
                }
                url += `${formData.id}/`;
            }

            const response = await axios({
                method: method.toLowerCase(),
                url: url,
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                data: method === 'POST' ? formData : undefined
            });
            
            console.log('Response received:', response.data);
            setResponse(response.data);
            setFormData({});
        } catch (err) {
            console.error('Request failed:', err);
            setError(err.response?.data?.detail || err.message);
        }
    };

    if (loading) {
        return <div>Loading permissions...</div>;
    }

    return (
        <div className="rbac-container">
            <h1>RBAC Interface</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>
                        Resource Type:
                        <select 
                            value={resourceType} 
                            onChange={handleResourceTypeChange}
                            className="select-input"
                        >
                            <option value="">Select a resource</option>
                            <option value="clients">Clients</option>
                            <option value="bankaccounts">Bank Accounts</option>
                            <option value="transactions">Transactions</option>
                        </select>
                    </label>
                </div>

                <div className="form-group">
                    <label>
                        Method:
                        <select 
                            value={method} 
                            onChange={handleMethodChange}
                            className="select-input"
                        >
                            {hasPermission('GET', resourceType) && <option value="GET">GET</option>}
                            {hasPermission('POST', resourceType) && <option value="POST">POST</option>}
                            {hasPermission('PUT', resourceType) && <option value="PUT">PUT</option>}
                            {hasPermission('DELETE', resourceType) && <option value="DELETE">DELETE</option>}
                        </select>
                    </label>
                </div>

                {renderResourceForm()}

                <button 
                    type="submit" 
                    className="submit-button"
                    disabled={!method || !resourceType}
                >
                    Send Request
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}
            
            {response && (
                <div className="response-container">
                    <h2>Response:</h2>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default RBAC;