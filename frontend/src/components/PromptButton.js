import React from "react";

const PromptButton = ({ text, href }) => {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-xl text-sm transition-all"
    >
      {text}
    </a>
  );
};

export default PromptButton;