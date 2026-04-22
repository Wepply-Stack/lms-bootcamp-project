import { useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CreateCourse() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [currentStep, setCurrentStep] = useState(1);
  const [courseData, setCourseData] = useState({
    title: "",
    description: "",
    category: "",
    thumbnail: null,
  });


const [modules, setModules] = useState([
  {
    id: 1,
    name: "Module 1",
    objective: "",
    lessons: [
      { id: 1, name: "Lesson 1", objective: "" },
      { id: 2, name: "Lesson 2", objective: "" },
    ],
  },
]);

// which module/lesson is currently selected in the left sidebar
const [selectedModuleId, setSelectedModuleId] = useState(1);
const [selectedLessonId, setSelectedLessonId] = useState(1);





  const [thumbnailPreview, setThumbnailPreview] = useState(null);

  const steps = useMemo(
    () => [
      { number: 1, name: "Basic Information" },
      { number: 2, name: "Course Material" },
      { number: 3, name: "Review & Publish" },
    ],
    []
  );

  

  const handleNext = () => {
    if (currentStep < 3) setCurrentStep((s) => s + 1);
    else handlePublish();
  };

  const handleBack = () => {
    if (currentStep > 1) setCurrentStep((s) => s - 1);
  };

  const handleSaveDraft = () => {
    console.log("Course saved as draft:", courseData);
    navigate("/admin/dashboard");
  };

  const handlePublish = () => {
    console.log("Course published:", courseData);
    alert("Course published successfully!");
    navigate("/admin/dashboard");
  };

  const handleThumbnailChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setCourseData((prev) => ({ ...prev, thumbnail: file }));

    const reader = new FileReader();
    reader.onloadend = () => setThumbnailPreview(reader.result);
    reader.readAsDataURL(file);
  };

  const handleAddModule = () => {
  setModules((prev) => {
    const nextId = prev.length ? Math.max(...prev.map((m) => m.id)) + 1 : 1;

    const newModule = {
      id: nextId,
      name: `Module ${nextId}`,
      objective: "",
      lessons: [],
    };

    // auto-select the newly created module (like the screenshot UX)
    setSelectedModuleId(nextId);
    setSelectedLessonId(null);

    return [...prev, newModule];
  });
};



const handleDeleteModule = (id) => {
  setModules((prev) => {
    const filtered = prev.filter((m) => m.id !== id);

    if (selectedModuleId === id) {
      const fallbackModule = filtered[0] ?? null;
      setSelectedModuleId(fallbackModule?.id ?? null);
      setSelectedLessonId(fallbackModule?.lessons?.[0]?.id ?? null);
    }

    return filtered;
  });
};

  const handleAddLesson = () => {
    const newLesson = {
      id: lessons.length + 1,
      name: `Lesson ${lessons.length + 1}`,
    };
    setLessons([...lessons, newLesson]);
  };

  const handleDeleteLesson = (id) => {
    setLessons(lessons.filter((l) => l.id !== id));
  };

  const StepHeader = () => (
    <div className="mb-6">
      <h1 className="text-[18px] font-semibold text-[#0F2F2A]">
        {steps[currentStep - 1].name}
      </h1>
      {currentStep === 1 && (
        <p className="mt-1 text-[12px] text-gray-500">
          Provide the basic course details below
        </p>
      )}
    </div>
  );

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left column */}
            <div className="lg:col-span-2 space-y-5">
              {/* Course Title */}
              <div>
                <label className="block text-[13px] font-semibold text-[#0F2F2A] mb-2">
                  <span className="text-red-500">*</span> Course Title
                </label>
                <input
                  type="text"
                  className="w-full h-10 px-3 border border-gray-300 rounded-md bg-white text-sm outline-none focus:ring-2 focus:ring-green-600/20 focus:border-green-700"
                  value={courseData.title}
                  onChange={(e) =>
                    setCourseData({ ...courseData, title: e.target.value })
                  }
                />
              </div>

              {/* Course Description */}
              <div>
                <label className="block text-[13px] font-semibold text-[#0F2F2A] mb-2">
                  <span className="text-red-500">*</span> Course Description
                </label>
                <textarea
                  rows={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-sm outline-none resize-none focus:ring-2 focus:ring-green-600/20 focus:border-green-700"
                  value={courseData.description}
                  onChange={(e) =>
                    setCourseData({
                      ...courseData,
                      description: e.target.value,
                    })
                  }
                />
              </div>

              {/* Course Category */}
              <div>
                <label className="block text-[13px] font-semibold text-[#0F2F2A] mb-2">
                  <span className="text-red-500">*</span> Course Category
                </label>
                <select
                  className="w-full h-10 px-3 border border-gray-300 rounded-md bg-white text-sm outline-none focus:ring-2 focus:ring-green-600/20 focus:border-green-700"
                  value={courseData.category}
                  onChange={(e) =>
                    setCourseData({ ...courseData, category: e.target.value })
                  }
                >
                  <option value=""> </option>
                  <option value="tech">Technology</option>
                  <option value="business">Business</option>
                  <option value="design">Design</option>
                </select>
              </div>
            </div>

            {/* Right column */}
            <div>
              <label className="block text-[13px] font-semibold text-[#0F2F2A] mb-2">
                <span className="text-red-500">*</span> Course Thumbnail
              </label>

              <div className="border border-green-300 bg-green-100/70 rounded-md p-4">
                <div className="h-[92px] flex items-center justify-center">
                  {thumbnailPreview ? (
                    <img
                      src={thumbnailPreview}
                      alt="Preview"
                      className="w-full h-[92px] object-cover rounded"
                    />
                  ) : (
                    <div className="text-center">
                      <p className="text-[10px] text-gray-600 mb-2">
                        Upload Image .jpeg, .png
                      </p>
                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="px-8 h-9 rounded-full bg-[#0F2F2A] text-white text-sm font-medium hover:bg-[#0b241f] transition-colors"
                      >
                        Upload
                      </button>
                    </div>
                  )}
                </div>

                <input
                  ref={fileInputRef}
                  type="file"
                  className="hidden"
                  accept="image/*"
                  onChange={handleThumbnailChange}
                />
              </div>

              <div className="mt-2 flex items-center justify-between text-[12px] text-gray-600">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="hover:text-gray-800"
                >
                  / Edit Cover Image
                </button>
                <button
                  type="button"
                  className="hover:text-gray-800"
                  onClick={() => {
                    // simple preview behavior: open image in new tab if exists
                    if (thumbnailPreview) window.open(thumbnailPreview, "_blank");
                  }}
                >
                  Preview Image
                </button>
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Course Structure
              </h3>
              <div className="bg-white border border-gray-300 rounded-lg p-4 space-y-2">
                {modules.map((module) => (
                  <div key={module.id} className="flex items-center gap-3 mb-4">
                    <input
                      type="text"
                      value={module.name}
                      onChange={(e) => {
                        const updated = modules.map((m) =>
                          m.id === module.id
                            ? { ...m, name: e.target.value }
                            : m
                        );
                        setModules(updated);
                      }}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded"
                    />
                    <button className="px-3 py-2 text-gray-600 hover:bg-gray-100 rounded">
                      ✎
                    </button>
                    <button
                      onClick={() => handleDeleteModule(module.id)}
                      className="px-3 py-2 text-gray-600 hover:bg-gray-100 rounded"
                    >
                      🗑
                    </button>
                  </div>
                ))}
              </div>
              <button
                onClick={handleAddModule}
                className="mt-3 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                + Add Module
              </button>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Enter Learning Objective
              </h3>
              <textarea
                placeholder="Enter learning objectives..."
                rows="4"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none resize-none"
              />
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Lessons
              </h3>
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 px-4 font-medium text-gray-700">
                      ID
                    </th>
                    <th className="text-left py-2 px-4 font-medium text-gray-700">
                      Lesson Name
                    </th>
                    <th className="text-right py-2 px-4"></th>
                  </tr>
                </thead>
                <tbody>
                  {lessons.map((lesson) => (
                    <tr key={lesson.id} className="border-b hover:bg-gray-50">
                      <td className="py-2 px-4 text-gray-600">{lesson.id}</td>
                      <td className="py-2 px-4 text-gray-600">{lesson.name}</td>
                      <td className="text-right py-2 px-4">
                        <button
                          onClick={() => handleDeleteLesson(lesson.id)}
                          className="text-gray-600 hover:text-gray-800"
                        >
                          ⋮
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <button
                onClick={handleAddLesson}
                className="mt-3 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                + Add Lesson
              </button>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Review & Publish
              </h3>
              <div className="bg-gray-50 border border-gray-300 rounded-lg p-6 space-y-4">
                <div>
                  <p className="text-sm text-gray-600">Course Title</p>
                  <p className="text-lg font-semibold text-gray-800">
                    {courseData.title || "Not set"}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Description</p>
                  <p className="text-gray-700">
                    {courseData.description || "Not set"}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Category</p>
                  <p className="text-gray-700">
                    {courseData.category || "Not set"}
                  </p>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="flex-1 overflow-auto bg-gray-50">
      {/* Back */}
      <div className="px-8 py-4">
        <button
          onClick={() => navigate("/admin/dashboard")}
          className="text-gray-600 hover:text-gray-800 font-medium flex items-center gap-2 transition-colors text-sm"
        >
          ← Back
        </button>
      </div>

      {/* Centered card like screenshot */}
      <div className="px-8 pb-10">
        <div className="max-w-5xl mx-auto bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="p-8">
            <StepHeader />

            {/* (Optional) keep step indicator but subtle; remove if you want exact screenshot */}
            <div className="mb-6">
              <div className="flex items-center gap-4">
                {steps.map((step) => (
                  <div key={step.number} className="flex items-center gap-4">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all text-sm ${
                        step.number <= currentStep
                          ? "bg-green-700 text-white"
                          : "bg-gray-200 text-gray-600"
                      }`}
                    >
                      {step.number}
                    </div>
                    {step.number < steps.length && (
                      <div
                        className={`h-1 w-20 transition-all ${
                          step.number < currentStep
                            ? "bg-green-700"
                            : "bg-gray-200"
                        }`}
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="pb-10">{renderStepContent()}</div>

            {/* Bottom actions */}
            <div className="flex justify-end gap-3">
              <button
                onClick={handleSaveDraft}
                className="h-9 px-4 border border-gray-300 rounded-md text-gray-700 text-sm hover:bg-gray-50 transition-colors"
              >
                Save as Draft
              </button>
              <button
                onClick={handleNext}
                className="h-9 px-6 rounded-md bg-[#0F2F2A] text-white text-sm font-medium hover:bg-[#0b241f] transition-colors"
              >
                {currentStep === 3 ? "Publish" : "Continue"}
              </button>
            </div>

            {/* Back step (if needed for steps 2/3) */}
            {currentStep > 1 && (
              <div className="mt-4">
                <button
                  type="button"
                  onClick={handleBack}
                  className="text-sm text-gray-600 hover:text-gray-800"
                >
                  ← Previous
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
