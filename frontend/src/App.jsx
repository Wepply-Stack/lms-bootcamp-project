import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
import EmployeeLayout from "./pages/employee/EmployeeLayout";
import AdminOverview from "./pages/AdminOverview";
import EmployeeHome from "./pages/employee/EmployeeHome";
import EmployeeCourses from "./pages/employee/EmployeeCourses";
import EmployeeOverview from "./pages/employee/EmployeeOverview"

const assignedCourses = [
  {
    id: 1,
    title: "Project Management",
    lessons: 8,
    completedLessons: 3,
    progress: 36,
    status: "in_progress",
    description: "A project management course equips professionals with essential skills to plan,",
  },
  {
    id: 2,
    title: "Workplace Safety",
    lessons: 6,
    completedLessons: 2,
    progress: 28,
    status: "in_progress",
    description: "A project management course equips professionals with essential skills to plan,",
  },
];

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
          { index: true, element: <EmployeeOverview assignedCourses={assignedCourses} /> },
          { path: "courses", element: <EmployeeCourses assignedCourses={assignedCourses} /> },
        ]
      }
    ]
  }
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;