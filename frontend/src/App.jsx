import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import Home from "./pages/Home";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import AdminOverview from "./pages/AdminOverview";

function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/">
        <Route index element={<Home />} />
        <Route
          path="admin"
          element={
            <ProtectedRoute allowRoles={["admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        >
          <Route index element={<AdminOverview />} />
        </Route>
        <Route
          path="employee"
          element={
            <ProtectedRoute allowRoles={["employee"]}>
              <EmployeeDashboard />
            </ProtectedRoute>
          }
        >
          <Route index element={<h2>Employee Dashboard</h2>} />
        </Route>
      </Route>
      )
  )
  return <RouterProvider router={router} />;
}

export default App;
