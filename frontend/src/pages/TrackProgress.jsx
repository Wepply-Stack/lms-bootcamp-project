import { useState } from "react";

export default function TrackProgress() {
  const [selectedCourse, setSelectedCourse] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");
  const [searchEmployee, setSearchEmployee] = useState("");

  const progressData = [
    {
      id: 1,
      employeeName: "John Doe",
      course: "Technical Skills",
      progress: 75,
      status: "In Progress",
      lastAccessed: "2 hours ago",
    },
    {
      id: 2,
      employeeName: "Jane Smith",
      course: "Leadership",
      progress: 100,
      status: "Completed",
      lastAccessed: "1 day ago",
    },
    {
      id: 3,
      employeeName: "Mike Johnson",
      course: "Technical Skills",
      progress: 45,
      status: "In Progress",
      lastAccessed: "3 days ago",
    },
    {
      id: 4,
      employeeName: "Sarah Williams",
      course: "Communication",
      progress: 0,
      status: "Not Started",
      lastAccessed: "N/A",
    },
  ];

  const getProgressColor = (progress) => {
    if (progress === 100) return "bg-green-500";
    if (progress >= 50) return "bg-blue-500";
    if (progress > 0) return "bg-yellow-500";
    return "bg-gray-300";
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case "Completed":
        return "bg-green-100 text-green-700";
      case "In Progress":
        return "bg-blue-100 text-blue-700";
      case "Not Started":
        return "bg-gray-100 text-gray-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  const filteredData = progressData.filter((record) => {
    const matchesCourse = selectedCourse === "all" || record.course.toLowerCase().includes(selectedCourse);
    const matchesStatus = selectedStatus === "all" || record.status === selectedStatus;
    const matchesSearch = record.employeeName.toLowerCase().includes(searchEmployee.toLowerCase());
    return matchesCourse && matchesStatus && matchesSearch;
  });

  const handleViewDetails = (employeeId) => {
    console.log("Viewing details for employee:", employeeId);
    alert(`Viewing performance details for employee ${employeeId}`);
  };

  const handleDownloadReport = () => {
    console.log("Downloading performance report...");
    alert("Report download started!");
    // In a real app, this would trigger a file download
  };

  const handleSendNotifications = () => {
    console.log("Sending notifications to employees...");
    alert("Notifications sent to all employees!");
  };

  return (
    <div className="flex-1 overflow-auto bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-8 py-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Track Progress</h1>
        <p className="text-gray-600 text-sm">Monitor employee learning progress and course completion</p>
      </div>

      {/* Main Content */}
      <div className="p-8 space-y-6">
        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Course Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">Filter by Course</label>
              <select
                value={selectedCourse}
                onChange={(e) => setSelectedCourse(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none text-sm"
              >
                <option value="all">All Courses</option>
                <option value="technical">Technical Skills</option>
                <option value="leadership">Leadership</option>
                <option value="communication">Communication</option>
              </select>
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">Filter by Status</label>
              <select 
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none text-sm"
              >
                <option value="all">All Status</option>
                <option value="Completed">Completed</option>
                <option value="In Progress">In Progress</option>
                <option value="Not Started">Not Started</option>
              </select>
            </div>

            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">Search Employee</label>
              <input
                type="text"
                placeholder="Search by name..."
                value={searchEmployee}
                onChange={(e) => setSearchEmployee(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none text-sm"
              />
            </div>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <p className="text-gray-600 text-xs font-medium mb-2 uppercase">Total Enrolled</p>
            <p className="text-3xl font-bold text-gray-900">24</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <p className="text-gray-600 text-xs font-medium mb-2 uppercase">Completed</p>
            <p className="text-3xl font-bold text-green-600">18</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <p className="text-gray-600 text-xs font-medium mb-2 uppercase">In Progress</p>
            <p className="text-3xl font-bold text-blue-600">4</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
            <p className="text-gray-600 text-xs font-medium mb-2 uppercase">Not Started</p>
            <p className="text-3xl font-bold text-gray-600">2</p>
          </div>
        </div>

        {/* Progress Table */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Employee Name</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Course</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Progress</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Last Accessed</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((record) => (
                  <tr key={record.id} className="border-b hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <p className="font-medium text-gray-900 text-sm">{record.employeeName}</p>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-gray-600 text-sm">{record.course}</p>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-24 bg-gray-200 rounded-full h-2.5">
                          <div
                            className={`h-2.5 rounded-full ${getProgressColor(record.progress)}`}
                            style={{ width: `${record.progress}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-700 min-w-10">{record.progress}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1.5 rounded-full text-xs font-medium ${getStatusBadge(record.status)}`}>
                        {record.status}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-sm text-gray-600">{record.lastAccessed}</p>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <button 
                        onClick={() => handleViewDetails(record.id)}
                        className="px-4 py-2 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200 font-medium transition-colors"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Export Button */}
        <div className="flex justify-end gap-3">
          <button 
            onClick={handleDownloadReport}
            className="px-6 py-2.5 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors text-sm"
          >
            Download Report
          </button>
          <button 
            onClick={handleSendNotifications}
            className="px-6 py-2.5 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors text-sm"
          >
            Send Notifications
          </button>
        </div>
      </div>
    </div>
  );
}
