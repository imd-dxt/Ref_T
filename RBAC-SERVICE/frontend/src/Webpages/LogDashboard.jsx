import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/LogDashboard.css';

const LogDashboard = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [logsPerPage] = useState(10);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const token = localStorage.getItem('token');
                console.log('Fetching logs...');
                const response = await axios.get('http://127.0.0.1:8000/api/logs/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                console.log('Received logs:', response.data);
                setLogs(response.data);
            } catch (err) {
                console.error('Error fetching logs:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchLogs();
    }, []);

    const indexOfLastLog = currentPage * logsPerPage;
    const indexOfFirstLog = indexOfLastLog - logsPerPage;
    const currentLogs = logs.slice(indexOfFirstLog, indexOfLastLog);

    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    if (loading) return <div className="loading">Loading logs...</div>;
    if (error) return <div className="error">Error: {error}</div>;
    if (!logs.length) return <div className="no-logs">No logs found</div>;

    return (
        <div className="log-dashboard">
            <h2>Request Logs</h2>
            <div className="log-table-container">
                <table className="log-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>User</th>
                            <th>Method</th>
                            <th>Endpoint</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {currentLogs.map((log) => (
                            <tr key={log.id}>
                                <td>{log.id}</td>
                                <td>{log.user}</td>
                                <td>
                                    <span className={`log-method ${log.method?.toLowerCase()}`}>
                                        {log.method}
                                    </span>
                                </td>
                                <td>
                                    <span className="log-endpoint">{log.endpoint}</span>
                                </td>
                                <td className="log-timestamp">
                                    {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'N/A'}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="log-pagination">
                <button 
                    onClick={() => paginate(currentPage - 1)} 
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <button 
                    onClick={() => paginate(currentPage + 1)} 
                    disabled={indexOfLastLog >= logs.length}
                >
                    Next
                </button>
            </div>
        </div>
    );
};

export default LogDashboard;

