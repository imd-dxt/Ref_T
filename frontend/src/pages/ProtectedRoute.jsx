import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  
  const token = localStorage.getItem("accessToken");

  return token ? children : <Navigate to="/" />; // Redirect to login if not authenticated
};

export default ProtectedRoute;
