import React, { useState } from 'react';
import { api } from '../api/client';

interface Props {
    userId: string;
}

export const AiAdvisor: React.FC<Props> = ({ userId }) => {
    const [advice, setAdvice] = useState<string>('');
    const [loading, setLoading] = useState(false);

    const handleAskAi = async () => {
        setLoading(true);
        try {
            const result = await api.getAdvice(userId);
            setAdvice(result);
        } catch (error) {
            console.error(error);
            setAdvice("Sorry, the financial advisor is currently offline. (Check if Port 8001 is running!)");
        }
        setLoading(false);
    };

    return (
        <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg shadow-lg p-6 text-white mb-8">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">🤖 AI Financial Coach</h2>
                {!advice && (
                    <button 
                        onClick={handleAskAi}
                        disabled={loading}
                        className="bg-white text-indigo-600 px-6 py-2 rounded-full font-bold hover:bg-gray-100 transition disabled:opacity-50"
                    >
                        {loading ? "Analyzing..." : "Analyze My Finances"}
                    </button>
                )}
            </div>

            {loading && (
                <div className="animate-pulse flex space-x-4">
                    <div className="flex-1 space-y-4 py-1">
                        <div className="h-4 bg-purple-400 rounded w-3/4"></div>
                        <div className="h-4 bg-purple-400 rounded"></div>
                    </div>
                </div>
            )}

            {advice && (
                <div className="bg-white/10 p-4 rounded-lg border border-white/20 backdrop-blur-sm">
                    {/* Render newlines correctly */}
                    <div className="whitespace-pre-wrap leading-relaxed">
                        {advice}
                    </div>
                    <button 
                        onClick={() => setAdvice('')}
                        className="mt-4 text-sm text-purple-200 hover:text-white underline"
                    >
                        Refresh Analysis
                    </button>
                </div>
            )}
        </div>
    );
};