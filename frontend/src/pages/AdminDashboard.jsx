import React from "react";
import { NavLink, Outlet } from "react-router-dom";

function AdminDashboard() {
  return (
    <div className="container">
      <header className="flex items-center justify-evenly py-4">
        <span>LOGO</span>
        <nav>
          <ul>
            <NavLink to="/admin">Dashboard</NavLink>
            <NavLink to="/admin/create-course">Create Course</NavLink>
            <NavLink to="/admin/manage-employees">Manage Employees</NavLink>
            <NavLink to="/admin/track-progress">Track Progress</NavLink>
          </ul>
        </nav>
      </header>
      <Outlet />
    </div>
  );
}

export default AdminDashboard;
