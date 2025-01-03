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
        <div>
            <h1>URL Scanner</h1>
            <form onSubmit={handleScan}>
                <label>
                    URL:
                    <input type="url" value={url} onChange={(e) => setUrl(e.target.value)} required />
                </label>
                <button type="submit">Scan URL</button>
            </form>
            {scanResult && (
                <div>
                    <h2>Scan Results</h2>
                    <pre>{JSON.stringify(scanResult, null, 2)}</pre>
                </div>
            )}
            {error && (
                <div>
                    <h2>Error</h2>
                    <pre>{error}</pre>
                </div>
            )}
        </div>
    );
};

export default URLScanner;