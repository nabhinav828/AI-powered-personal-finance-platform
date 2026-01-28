import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { type Transaction } from '../api/client';

interface Props {
    transactions: Transaction[];
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658'];

export const DashboardCharts: React.FC<Props> = ({ transactions }) => {
    
    // 1. Calculate Expenses by Category
    const categoryData = useMemo(() => {
        const expenses = transactions.filter(t => t.type === 'expense');
        const grouped: Record<string, number> = {};

        expenses.forEach(t => {
            const key = t.description || "Uncategorized"; 
            grouped[key] = (grouped[key] || 0) + t.amount;
        });

        return Object.keys(grouped).map(key => ({
            name: key,
            value: parseFloat(grouped[key].toFixed(2))
        })).sort((a, b) => b.value - a.value).slice(0, 5); 
    }, [transactions]);

    // 2. Calculate Monthly Income vs Expense
    const monthlyData = useMemo(() => {
        const grouped: Record<string, { name: string, income: number, expense: number }> = {};

        transactions.forEach(t => {
            const date = new Date(t.date);
            const monthKey = `${date.getFullYear()}-${date.getMonth() + 1}`; 
            const monthName = date.toLocaleString('default', { month: 'short' });

            if (!grouped[monthKey]) {
                grouped[monthKey] = { name: monthName, income: 0, expense: 0 };
            }

            if (t.type === 'income') {
                grouped[monthKey].income += t.amount;
            } else {
                grouped[monthKey].expense += t.amount;
            }
        });

        return Object.values(grouped);
    }, [transactions]);

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-bold mb-4 text-gray-700">Top 5 Expenses</h3>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie
                                data={categoryData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                fill="#8884d8"
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {categoryData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip formatter={(value) => `$${value}`} />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-bold mb-4 text-gray-700">Income vs Expense</h3>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                            data={monthlyData}
                            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip formatter={(value) => `$${value}`} />
                            <Legend />
                            <Bar dataKey="income" fill="#82ca9d" name="Income" />
                            <Bar dataKey="expense" fill="#ff6b6b" name="Expenses" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};