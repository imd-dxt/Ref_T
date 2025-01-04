import React, { useState } from 'react';
import axios from 'axios';

const URLScanner = () => {
    const [url, setUrl] = useState('');
    const [scanResult, setScanResult] = useState(null);
    const [error, setError] = useState(null);

    const handleScan = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/rbac/scan-url/', { url });
            setScanResult(response.data);
            setError(null);
        } catch (err) {
            setError(err.message);
            setScanResult(null);
        }
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>Endpoint Check</h1>
            <form onSubmit={handleScan} style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '10px' }}>
                    URL:
                    <input
                        type="url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        required
                        style={{ marginLeft: '10px', padding: '5px', width: '300px' }}
                    />
                </label>
                <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>Scan</button>
            </form>
            {scanResult && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Scan Results</h2>
                    <div style={{ backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
                        <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                            {JSON.stringify(scanResult, null, 2)}
                        </pre>
                    </div>
                </div>
            )}
            {error && (
                <div style={{ marginTop: '20px', color: 'red' }}>
                    <h2>Error</h2>
                    <pre>{error}</pre>
                </div>
            )}
        </div>
    );
};

export default URLScanner;