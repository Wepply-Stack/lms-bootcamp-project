import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider, Outlet } from "react-router-dom"
import Login from "./pages/Login"
import AdminLayout from "./layout/AdminLayout"
import Dashboard from "./pages/Dashboard"
import CreateCourse from "./pages/CreateCourse"
import ManageEmployees from "./pages/ManageEmployees"
import TrackProgress from "./pages/TrackProgress"
import Analytics from "./pages/Analytics"
import ErrorBoundary from "./components/ErrorBoundary"

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
