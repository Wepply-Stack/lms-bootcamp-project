import React from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "@/auth/useAuth";
import { useState } from "react";

const Home = () => {
  const [formdata, setFormData] = useState({ email: "", password: "" });
  const navigate = useNavigate();
  const { login, user, isAuthenticated } = useAuth();
  function handleChange(e) {
    setFormData({ ...formdata, [e.target.name]: e.target.value });
  }
  async function handleSubmit(e) {
    e.preventDefault();
    const data = await login(formdata);
    const role = data?.user?.role;
    if (role === "admin") {
      navigate("/admin");
    } else if (role === "employee") {
      navigate("/employee");
    }

  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Enter your email"
          value={formdata.email}
          onChange={handleChange}
        />
        <input
          type="password"
          placeholder="Enter your password"
          name="password"
          id="pwd"
          value={formdata.password}
          onChange={handleChange}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Home;
