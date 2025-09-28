export default function Welcome() {
  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4 text-gray-900 dark:text-white">
          Welcome to Financial Toolkit
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
          Your personal financial dashboard for tracking investments, capital gains, and portfolio performance.
        </p>
        <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold mb-3 text-blue-900 dark:text-blue-100">
            Dashboard Overview
          </h2>
          <p className="text-blue-800 dark:text-blue-200">
            Monitor your financial progress, analyze investment performance, and make informed decisions with comprehensive financial insights.
          </p>
        </div>
      </div>
    </div>
  );
}