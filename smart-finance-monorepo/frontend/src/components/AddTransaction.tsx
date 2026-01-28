import React, { useState } from 'react';
import { api, type Transaction } from '../api/client';

interface Props {
    userId: string;
    onSuccess: () => void; // Function to refresh list after adding
}

export const AddTransaction: React.FC<Props> = ({ userId, onSuccess }) => {
    const [amount, setAmount] = useState('');
    const [description, setDescription] = useState('');
    const [type, setType] = useState<'income' | 'expense'>('expense');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!amount || !userId) return;

        const newTx: Transaction = {
            user_id: userId,
            amount: parseFloat(amount),
            description,
            date: new Date().toISOString().split('T')[0], // Today's date YYYY-MM-DD
            type: type
        };

        try {
            await api.addTransaction(newTx);
            // Clear form
            setAmount('');
            setDescription('');
            onSuccess(); // Tell parent to reload data
        } catch (error) {
            console.error("Failed to add transaction", error);
            alert("Error adding transaction!");
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
            <h2 className="text-xl font-bold mb-4">Add New Transaction</h2>
            <form onSubmit={handleSubmit} className="flex gap-4 items-end">

                {/* Description Input */}
                <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700">Description</label>
                    <input
                        type="text"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                        placeholder="e.g. Kroger"
                    />
                </div>

                {/* Amount Input */}
                <div className="w-32">
                    <label className="block text-sm font-medium text-gray-700">Amount</label>
                    <input
                        type="number"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                        placeholder="0.00"
                    />
                </div>

                {/* Type Selector */}
                <div className="w-32">
                    <label className="block text-sm font-medium text-gray-700">Type</label>
                    <select
                        value={type}
                        onChange={(e) => setType(e.target.value as 'income' | 'expense')}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                    >
                        <option value="expense">Expense</option>
                        <option value="income">Income</option>
                    </select>
                </div>

                <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
                >
                    Add
                </button>
            </form>
        </div>
    );
};