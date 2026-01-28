import { useEffect, useState } from 'react';
import { api, type Transaction } from './api/client';
import { AddTransaction } from './components/AddTransaction';
import { DashboardCharts } from './components/DashboardCharts';
import { AiAdvisor } from './components/AiAdvisor';

function App() {
  const [userId, setUserId] = useState<string>(''); // We will store our ID here
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  // 1. On Load: Create a fake user or use existing one
  useEffect(() => {
    const initUser = async () => {
      // In a real app, this is Auth. 
      // For now, we try to create a user "test@example.com".
      // If it fails (already exists), we just hardcode the ID or handle it.
      const email = "test@example.com";
      try {
        const user = await api.createUser(email);
        setUserId(user.id);
      } catch (e) {
        // If user already exists, we need their ID. 
        // For this MVP, let's just use a hardcoded known ID if create fails, 
        // OR (Better for now) check your Python terminal for the ID if you created one earlier.
        console.log("User likely exists.");
        // TEMPORARY: If you have a User ID from Postman/Swagger, paste it here as fallback
        setUserId("f15afe20-9c37-4f64-997a-9f3d51a58caa"); 
      }
    };
    initUser();
  }, []);

  // 2. Function to fetch data
  const loadData = async () => {
    if (!userId) return;
    const data = await api.getTransactions(userId);
    setTransactions(data);
  };

  // Watch for userId changes
  useEffect(() => {
    if (userId) loadData();
  }, [userId]);

  return (
    <div className="min-h-screen container mx-auto p-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">💰 SmartFinance Dashboard</h1>

      {/* Show User ID for debugging */}
      <div className="mb-4 text-sm text-gray-500">User ID: {userId || "Loading..."}</div>

      {/* Input Form */}
      {userId && <AddTransaction userId={userId} onSuccess={loadData} />}

      {/* 1. NEW: AI Advisor Section */}
      {userId && <AiAdvisor userId={userId} />}

      {/* 2. NEW: Visualization Charts */}
      {transactions.length > 0 && <DashboardCharts transactions={transactions} />}

      {/* Transaction List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50 bg-opacity-75">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((t) => (
              <tr key={t.id || Math.random()}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{t.date}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{t.description}</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-bold ${t.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                  ${t.amount}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">{t.type}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {transactions.length === 0 && (
          <div className="p-6 text-center text-gray-500">No transactions yet. Add one above!</div>
        )}
      </div>
    </div>
  );
}

export default App;