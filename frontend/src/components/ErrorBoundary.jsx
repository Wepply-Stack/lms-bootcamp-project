import { useRouteError } from "react-router-dom";

export default function ErrorBoundary() {
  const error = useRouteError();

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          {error?.status || "Error"}
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          {error?.statusText || error?.message || "Something went wrong"}
        </p>
        <a
          href="/"
          className="px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700"
        >
          Back to Home
        </a>
      </div>
    </div>
  );
}
