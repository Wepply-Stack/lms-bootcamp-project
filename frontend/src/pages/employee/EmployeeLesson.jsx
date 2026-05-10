import React from "react";
import { useState } from "react";
import { useParams } from "react-router-dom";

// const lessons = [
//   { id: 1, title: "Introduction to safety", status: "done" },
//   { id: 2, title: "Hazard types", status: "done" },
//   { id: 3, title: "Emergency procedures", status: "active" },
//   { id: 4, title: "PPE guidelines", status: "todo" },
//   { id: 5, title: "Reporting incidents", status: "todo" },
//   { id: 6, title: "Review & summary", status: "todo" },
// ];

const LessonIcon = ({ status }) => {
  const base =
    "w-6 h-6 rounded-full border flex items-center justify-center flex-shrink-0 text-xs";

  if (status === "done")
    return (
      <div className={`${base} bg-[#1F4842] border-[#1F4842] text-white`}>
        ✓
      </div>
    );

  if (status === "active")
    return (
      <div className={`${base} bg-[#1F4842] border-[#1F4842] text-white`}>
        ▷
      </div>
    );

  return (
    <div className={`${base} border-[#c8ddd9] text-gray-400`}>
      ☰
    </div>
  );
};

export default function EmployeeLesson({ courseData, setCourseData }) {
  const { courseId } = useParams();

  const [course, setCourse] = useState(
    courseData.find((c) => c.id === parseInt(courseId))
  );

  const [lessons, setLessons] = useState(course?.lessons || []);
  const [selectedLesson, setSelectedLesson] = useState(lessons[0]);

  // modal state
  const [showModal, setShowModal] = useState(false);

  const openLessonModal = (lesson) => {
    setSelectedLesson(lesson);
    setShowModal(true);
  };

  const closeLessonModal = () => {
    setShowModal(false);
  };

  return (
    <>
      <div className="flex min-h-[580px] overflow-hidden rounded-2xl border border-gray-200 bg-gray-50 font-sans">
        {/* Sidebar */}
        <div className="flex w-60 min-w-[240px] flex-col border-r border-gray-200 bg-white py-4">
          {/* Back */}
          <button className="px-4 pb-3 text-left text-sm text-gray-500 hover:text-gray-800">
            ‹ Back
          </button>

          {/* Thumbnail */}
          <div className="mx-4 mb-3 h-24 rounded-xl bg-[#cce8e2]" />

          {/* Course info */}
          <p className="px-4 text-sm font-medium text-gray-800">
            {course?.title}
          </p>

          <p className="mt-0.5 mb-2 px-4 text-xs text-gray-500">
            {course?.lessons?.length} Lessons · 38%
          </p>

          {/* Progress bar */}
          <div className="mx-4 mb-4 h-1.5 overflow-hidden rounded-full bg-[#d6eee8]">
            <div className="h-full w-[38%] rounded-full bg-[#1F4842]" />
          </div>

          {/* Lesson list */}
          <div className="flex flex-col gap-0.5 px-2">
            {lessons.map((lesson) => (
              <div
                key={lesson.id}
                onClick={() => setSelectedLesson(lesson)}
                className={`cursor-pointer rounded-xl px-2.5 py-2 text-sm transition-colors flex items-center gap-2.5 ${
                  selectedLesson?.id === lesson.id
                    ? "bg-[#e6f4f0] text-[#1F4842] font-medium"
                    : "text-gray-500 hover:bg-gray-50"
                }`}
              >
                <LessonIcon status={lesson.status} />
                <span>{lesson.title}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Main content */}
        <div className="flex flex-1 flex-col gap-3.5 bg-white p-6">
          {/* Lesson header */}
          <div>
            <h2 className="text-xl font-medium text-gray-900">
              {selectedLesson?.title}
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              {selectedLesson?.id} of {lessons.length} ·{" "}
              {selectedLesson?.type} · {selectedLesson?.duration}
            </p>
          </div>

          {/* Clickable Preview Box */}
          <div
            onClick={() => openLessonModal(selectedLesson)}
            className="flex h-[280px] cursor-pointer items-center justify-center rounded-2xl bg-[#cce8e2]"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/70">
              <span className="ml-0.5 text-xl text-[#1F4842]">▷</span>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-2.5">
            <button className="rounded-xl border border-[#a8d5c7] bg-[#e8f5f0] px-4 py-2 text-sm font-medium text-[#1F4842] transition-colors hover:bg-[#d4eee5]">
              Mark as Completed
            </button>

            <button className="rounded-xl border border-gray-300 bg-white px-5 py-2 text-sm text-gray-800 transition-colors hover:bg-gray-50">
              Next
            </button>

            <button
              onClick={() => openLessonModal(selectedLesson)}
              className="ml-auto flex items-center gap-1.5 rounded-xl bg-[#1F4842] px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-[#17352e]"
            >
              ▷ Resume
            </button>
          </div>

          {/* Course description */}
          <div>
            <h3 className="mb-1.5 text-base font-medium text-gray-900">
              {selectedLesson?.title}
            </h3>

            <p className="text-sm leading-relaxed text-gray-500">
              {selectedLesson?.description}
            </p>
          </div>
        </div>
      </div>

      {/* MODAL */}
      {showModal && selectedLesson && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="w-[90%] max-w-3xl rounded-2xl bg-white p-6 shadow-xl">
            {/* Header */}
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-xl font-bold text-[#1F4842]">
                {selectedLesson.title}
              </h2>

              <button
                onClick={closeLessonModal}
                className="text-2xl font-bold text-gray-500 hover:text-black"
              >
                ×
              </button>
            </div>

            {/* VIDEO SECTION */}
            {selectedLesson.video_url ? (
              <div className="mb-5">
                <p className="mb-2 font-medium text-[#1F4842]">
                  Watch Lesson Video
                </p>

                <video
                  controls
                  className="w-full rounded-xl"
                  src={selectedLesson.video_url}
                />
              </div>
            ) : null}

            {/* FILE DOWNLOAD SECTION */}
            {selectedLesson.file_url ? (
              <div className="mb-5">
                <p className="mb-2 font-medium text-[#1F4842]">
                  Download Lesson Material
                </p>

                <a
                  href={selectedLesson.file_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-block rounded-xl bg-[#1F4842] px-5 py-2 text-white"
                >
                  Download File
                </a>
              </div>
            ) : null}

            {/* FALLBACK */}
            {!selectedLesson.video_url && !selectedLesson.file_url && (
              <p className="text-gray-500">
                No video or downloadable material available for this lesson.
              </p>
            )}
          </div>
        </div>
      )}
    </>
  );
}