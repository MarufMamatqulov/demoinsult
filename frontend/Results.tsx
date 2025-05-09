import React from 'react';

const Results: React.FC<{ prediction: string }> = ({ prediction }) => {
    return (
        <div className="p-4">
            <h1 className="text-xl font-bold">Prediction Results</h1>
            <p className="mt-2">The predicted happiness score is: <strong>{prediction}</strong></p>
        </div>
    );
};

export default Results;
