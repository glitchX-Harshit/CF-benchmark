export default function Dashboard() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Conversations Analyzed</h3>
          <p className="text-3xl font-bold mt-2">1,248</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Average Response Score</h3>
          <p className="text-3xl font-bold mt-2">76.4</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Benchmark Runs</h3>
          <p className="text-3xl font-bold mt-2">342</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-8">
        <h2 className="text-lg font-semibold mb-4">Recent Evaluations</h2>
        <div className="space-y-4">
          <div className="flex justify-between items-center py-3 border-b border-gray-100 last:border-0">
            <div>
              <p className="font-medium">Acme Corp - Price Objection</p>
              <p className="text-sm text-gray-500">Evaluated 2 hours ago</p>
            </div>
            <div className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">84 / 100</div>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-gray-100 last:border-0">
            <div>
              <p className="font-medium">Globex - Missing Feature</p>
              <p className="text-sm text-gray-500">Evaluated 5 hours ago</p>
            </div>
            <div className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm font-medium">62 / 100</div>
          </div>
        </div>
      </div>
    </div>
  );
}
