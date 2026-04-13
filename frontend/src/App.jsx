import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom"
import MainLayout from "./layout/MainLayout"
import Login from "./pages/Login";


function App() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Login />} />
      </Route>

      
    )
  );
  return (
    <RouterProvider router={router} />
  )
}

export default App
