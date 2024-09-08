import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const RatingsComponent = ({ features }) => {
    // Convert features object into an array of {key, value} objects
    const featureArray = Object.entries(features).map(([key, value]) => ({ key, value }));

    return (
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-around' }}>
            {featureArray.map((feature, index) => (
                <div className='center' key={index} style={{ margin: '20px', textAlign: 'center', width: 70, height: 70 }}>
                    <CircularProgressbar
                        value={feature.value}
                        maxValue={5}
                        text={`${feature.value}`}
                        styles={buildStyles({
                            textSize: '30px',
                            pathColor: `#05a168`,
                            trailColor: '#ddd',
                            textColor: '#000',
                            backgroundColor: '#fff',
                        })}
                    />
                    <div className='flex justify-center' style={{ marginTop: '10px', fontSize: '14px' }}>{feature.key}</div>
                </div>
            ))}
        </div>
    );
};

export default RatingsComponent;
