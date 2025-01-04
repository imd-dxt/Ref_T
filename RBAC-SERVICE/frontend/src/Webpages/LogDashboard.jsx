// RBAC-SERVICE/frontend/src/Webpages/LogDashboard.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LogDashboard = () => {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const fetchLogs = async () => {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://127.0.0.1:8000/api/logs/', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setLogs(response.data);
        };
        fetchLogs();
    }, []);

    return (
        <div>
            <h1>Log Dashboard</h1>
            <table>
                <thead>
                    <tr>
                        <th>User</th>
                        <th>Method</th>
                        <th>Endpoint</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.map(log => (
                        <tr key={log.id}>
                            <td>{log.user.username}</td>
                            <td>{log.method}</td>
                            <td>{log.endpoint}</td>
                            <td>{log.timestamp}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default LogDashboard;