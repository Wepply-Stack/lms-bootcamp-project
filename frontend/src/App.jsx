import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import AdminOverview from "./pages/AdminOverview";
import EmployeeOverview from "./pages/EmployeeOverview";

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
            <EmployeeDashboard />
          </ProtectedRoute>
        ),
        children: [
          { index: true, element: <EmployeeOverview /> }
        ]
      }
    ]
  }
]);

function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<Login />} errorElement={<ErrorBoundary />} />
        
        {/* Admin Routes with Layout */}
        <Route 
          path="/admin/*" 
          element={
            <AdminLayout>
              <Outlet />
            </AdminLayout>
          }
          errorElement={<ErrorBoundary />}
        >
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="create-course" element={<CreateCourse />} />
          <Route path="manage-employees" element={<ManageEmployees />} />
          <Route path="track-progress" element={<TrackProgress />} />
          <Route path="analytics" element={<Analytics />} />
          <Route index element={<Dashboard />} />
        </Route>
      </>
    )
  );
  
  return <RouterProvider router={router} />
}

export default App
