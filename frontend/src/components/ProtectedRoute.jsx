import { Navigate } from "react-router-dom";
import useAuth from "@/auth/useAuth";

function ProtectedRoute({children, allowRoles}) {
    const {isAuthenticated, loading, user} = useAuth();
    if (loading) {
        return <div>Loading...</div>;
    }
    if (!isAuthenticated) {
        return <Navigate to="/" replace/>;
    }
    if (allowRoles && !allowRoles.includes(user.role)) {
        return <Navigate to="/unauthorized" />;
    }
  return children;
  
}

export default ProtectedRoute