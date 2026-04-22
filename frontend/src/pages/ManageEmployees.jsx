import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ManageEmployees() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedEmployees, setSelectedEmployees] = useState(new Set());
  const [selectedCourses, setSelectedCourses] = useState(new Set());

  const employees = [
    { id: 1, name: "John", email: "john@example.com", department: "IT", group: "Department", assigned: ["Task-development"] },
    { id: 2, name: "Jane", email: "jane@example.com", department: "HR", group: "Department", assigned: [] },
  ];

  const courses = [
    { id: 1, name: "Course Name", status: "Active" },
    { id: 2, name: "Course Name", status: "Active" },
    { id: 3, name: "Course Name", status: "Active" },
  ];

  const toggleEmployee = (id) => {
    const newSet = new Set(selectedEmployees);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelectedEmployees(newSet);
  };

  const toggleCourse = (id) => {
    const newSet = new Set(selectedCourses);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelectedCourses(newSet);
  };

  const handleAssign = () => {
    if (selectedEmployees.size === 0 || selectedCourses.size === 0) {
      alert("Please select at least one employee and one course");
      return;
    }
    console.log(
      "Assigning courses:",
      Array.from(selectedCourses),
      "to employees:",
      Array.from(selectedEmployees)
    );
    alert(`Assigned ${selectedCourses.size} course(s) to ${selectedEmployees.size} employee(s)!`);
    setSelectedEmployees(new Set());
    setSelectedCourses(new Set());
  };

  // ✅ FIX: define handleCancel so the page loads
  const handleCancel = () => {
    navigate(-1);
  };

  const filteredEmployees = employees.filter(
    (emp) =>
      emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      emp.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex-1 overflow-auto bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-8 py-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Manage Employees</h1>
        <p className="text-gray-600 text-sm">
          Assign courses to group, courses or users as a manager
        </p>
      </div>

      {/* Main Content */}
      <div className="p-8 space-y-6">
        {/* Select Group Assignment */}
        <div className="bg-white rounded-xl shadow-sm p-8 border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Select Group Assignment</h2>
          <p className="text-sm text-gray-600 mb-6">
            Select a group or persons or teams you want to them to assign the new role
          </p>

          {/* Search Box */}
          <div className="mb-6">
            <input
              type="text"
              placeholder="Search Employee"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none text-sm"
            />
          </div>

          {/* Employees Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-gray-50">
                  <th className="px-4 py-3 text-left">
                    <input type="checkbox" className="rounded" />
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Employee</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Email</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Department</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Group</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Assigned Course</th>
                  <th className="px-4 py-3"></th>
                </tr>
              </thead>
              <tbody>
                {filteredEmployees.map((emp) => (
                  <tr key={emp.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={selectedEmployees.has(emp.id)}
                        onChange={() => toggleEmployee(emp.id)}
                        className="rounded"
                      />
                    </td>
                    <td className="px-4 py-3 font-medium text-gray-900 text-sm">{emp.name}</td>
                    <td className="px-4 py-3 text-gray-600 text-sm">{emp.email}</td>
                    <td className="px-4 py-3 text-gray-600 text-sm">{emp.department}</td>
                    <td className="px-4 py-3 text-gray-600 text-sm">{emp.group}</td>
                    <td className="px-4 py-3">
                      {emp.assigned.length > 0 && (
                        <span className="px-3 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                          {emp.assigned[0]}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button className="text-gray-600 hover:text-gray-800">⋮</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Select Course */}
        <div className="bg-white rounded-xl shadow-sm p-8 border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Select Course</h2>
          <p className="text-sm text-gray-600 mb-6">Select courses to be assigned to a person</p>

          <div className="space-y-3">
            {courses.map((course) => (
              <label
                key={course.id}
                className="flex items-center gap-3 p-3 border border-gray-300 rounded-lg hover:bg-gray-50 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedCourses.has(course.id)}
                  onChange={() => toggleCourse(course.id)}
                  className="rounded"
                />
                <div className="flex-1">
                  <p className="font-medium text-gray-900 text-sm">{course.name}</p>
                  <p className="text-xs text-gray-600">Status: {course.status}</p>
                </div>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                  Active
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 justify-end">
          <button
            onClick={handleCancel}
            className="px-6 py-2.5 border border-gray-300 rounded-lg text-gray-700 font-medium hover:bg-gray-50 transition-colors text-sm"
          >
            Cancel
          </button>
          <button
            onClick={handleAssign}
            className="px-6 py-2.5 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors text-sm"
          >
            Assign
          </button>
        </div>
      </div>
    </div>
  );
}