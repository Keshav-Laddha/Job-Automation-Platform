import React, { useEffect } from "react";

const Modal = ({ children, onClose }) => {
  useEffect(() => {
    document.body.classList.add("modal-open");
    return () => {
      document.body.classList.remove("modal-open");
    };
  }, []);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div
        className="bg-white rounded-lg shadow-lg w-full max-w-lg relative flex flex-col"
        style={{ maxHeight: '80vh' }}
      >
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-2xl font-bold z-10"
          aria-label="Close"
        >
          &times;
        </button>
        <div className="overflow-y-auto p-6 pt-10" style={{ maxHeight: '80vh' }}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal; 