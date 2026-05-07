import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
import EmployeeLayout from "./pages/employee/EmployeeLayout";
import AdminOverview from "./pages/AdminOverview";
import EmployeeCourses from "./pages/employee/EmployeeCourses";
import EmployeeOverview from "./pages/employee/EmployeeOverview"
import {courseData} from "./pages/employee/courseData.js"

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <Login /> },
      {
        path: "admin",
        element: (
          <ProtectedRoute allowRoles={["admin"]}>
            <AdminDashboard />
          </ProtectedRoute>
        ),
        children: [
          { index: true, element: <AdminOverview /> }
        ]
      },
      {
        path: "employee",
        element: (
          <ProtectedRoute allowRoles={["employee"]}>
            <EmployeeLayout />
          </ProtectedRoute>
        ),
        children: [
          { index: true, element: <EmployeeOverview courseData={courseData} /> },
          { path: "courses", element: <EmployeeCourses courseData={courseData} /> },
        ]
      }
    ]
  }
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;