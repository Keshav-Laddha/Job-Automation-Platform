import React from "react";
import { Link, Outlet } from "react-router-dom";

const Layout = () => {
    return (
        <>
            <nav className="bg-white shadow sticky top-0 z-50">
                <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
                    <h1 className="text-xl font-bold text-blue-700">AI Job Assistant</h1>
                    <div className="flex space-x-6 text-sm">
                        <a href="/" className="hover:underline">🏠 Dashboard</a>
                        <a href="/form" className="hover:underline">🧠 Optimize</a>
                        <a href="/applied" className="hover:underline">📋 Applied Jobs</a>
                        <a href="/analytics" className="hover:underline">📊 Analytics</a>
                        <a href="/interview-questions" className="hover:underline">📝 Interview Questions</a>
                    </div>
                </div>
            </nav>


            <main className="p-6">
                <Outlet />
            </main>
        </>
    );
};

export default Layout;