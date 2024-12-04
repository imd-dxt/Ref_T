import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [requestType, setRequestType] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const apiUrl = "https://api.spotify.com/v1/search";
    const accessToken = "BQAHZGtQIHpENoEnuyCN3nQxHvKd0Wr9s_PdtcvNPbLG0QbGwkGrZecENCLWm_C2gkHj8YulieSy8IJ6w3d9-r8U528R4ogIHz_9-Q0jWbrFKfPnq0AEms_JkyjcAtdBpwDLURiXOLKATb0XSGWgxQBPVYPFmSlb00nfzaIT2U689FH5TXgmzrx123-0LIf_VujqmpQAgfKFStvOpxhcchL7QO0HlCVjnYf0rwbu9Ao2ISmczzN6P7vpUz64HC4a4V8UrAOBy1xxUQfIpDKBuU6ib8ywIn7T"; // Replace with your actual token

    const requestData = {
      requestType,
      title,
      description,
    };

    console.log("JSON Request Data:", JSON.stringify(requestData, null, 2));

    try {
      if (requestType === "POST" || requestType === "GET") {
        const response = await axios.get(apiUrl, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
          params: {
            q: title, // Search query
            type: "track", // Searching for tracks
            limit: 10, // Limit the results to 10 items
          },
        });
  
        const tracks = response.data.tracks.items;
  
        console.log("Tracks Found:");
        tracks.forEach((track) => {
          console.log(`Track: ${track.name}, Artist: ${track.artists.map((a) => a.name).join(", ")}`);
        });
  
        // Example: display a formatted version of the results in JSON
        console.log("Full API Response:", JSON.stringify(response.data, null, 2));
      } else {
        console.log("Request Type not supported for this test.");
      }
    } catch (error) {
      console.error("Error with Spotify API:", error.response?.data || error.message);
    }
  };

  return (
    <div className="container">
      <h1>Spotify Request Form</h1>
      <form onSubmit={handleSubmit}>
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
          <option value="DELETE">DELETE</option>
          <option value="PUT">PUT</option>
        </select>

        <label htmlFor="title">Title</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter the request title (e.g., Song Name)"
          required
        />

        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter the request description"
          required
        ></textarea>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default App;
