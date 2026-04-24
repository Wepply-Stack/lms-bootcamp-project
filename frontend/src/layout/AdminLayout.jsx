import AdminTopNav from "../components/AdminTopNav"; // adjust relative path if needed
import { Outlet } from "react-router-dom";

export default function AdminLayout() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <AdminTopNav />
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}