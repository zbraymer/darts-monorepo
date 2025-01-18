import React, { useState } from "react";

const Dartboard = () => {
    const [clicks, setClicks] = useState([]); // Store click positions
    const markerSize = 10; // Marker size in pixels
    const offset = markerSize / 2; // Half of the marker size for centering
    const dartboardRadius = 250; // Assume the dartboard's displayed radius in pixels

    const handleClick = async (event) => {
      const rect = event.target.getBoundingClientRect();
  
      // Get click position relative to the dartboard image
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
  
      // Calculate relative position to the center of the dartboard
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const relativeX = x - centerX;
      const relativeY = centerY - y; // Invert Y because screen coordinates are flipped
  
      // Calculate polar coordinates
      const radius = Math.sqrt(relativeX ** 2 + relativeY ** 2) / (rect.width / 2); // Normalize radius
      const angle = Math.atan2(relativeY, relativeX) * (180 / Math.PI); // Angle in degrees
  
      try {
          // Make a GET request to the API
          const response = await fetch(`http://localhost:8000/calculate-score?radius=${radius}&angle=${angle}`);
  
          if (!response.ok) {
              console.error("API Error:", response.statusText);
              return;
          }
  
          const data = await response.json();
          console.log("API Response:", data);
  
          // Add the click and backend result to the state
          setClicks((prevClicks) => [
              ...prevClicks,
              {
                  x,
                  y,
                  radius: radius.toFixed(4), // Actual radius
                  angle: angle.toFixed(4),   // Angle in degrees
                  zone: data.zone,           // Zone returned from API
                  score: data.score,         // Score returned from API
              },
          ]);
      } catch (error) {
          console.error("Error fetching from API:", error);
      }
  };
  

    const handleClear = () => {
        setClicks([]); // Reset the clicks state
    };

    return (
        <div style={styles.container}>
            <div style={styles.dartboardContainer}>
                {/* Dartboard Image */}
                <img
                    src="/dartboard.png"
                    alt="Dartboard"
                    onClick={handleClick}
                    style={styles.dartboard}
                />

                {/* Render Click Markers and Details */}
                {clicks.map((click, index) => (
                    <React.Fragment key={index}>
                        {/* Marker */}
                        <div
                            style={{
                                position: "absolute",
                                top: click.y - offset,
                                left: click.x - offset,
                                width: `${markerSize}px`,
                                height: `${markerSize}px`,
                                backgroundColor: "red",
                                borderRadius: "50%",
                                pointerEvents: "none", // Prevent markers from blocking clicks
                            }}
                        />
                        {/* Polar Coordinates and Zone Display */}
                        <div
                            style={{
                                position: "absolute",
                                top: click.y - offset - 20, // Slightly above the marker
                                left: click.x - offset + 10, // Slightly to the right of the marker
                                backgroundColor: "rgba(255, 255, 255, 0.8)",
                                color: "black",
                                padding: "2px 5px",
                                borderRadius: "4px",
                                fontSize: "12px",
                                pointerEvents: "none",
                            }}
                        >
                          zone: {click.zone}, score: {click.score}
                        </div>
                    </React.Fragment>
                ))}
            </div>

            {/* Reset Button */}
            <button onClick={handleClear} style={styles.resetButton}>
                Reset Markers
            </button>
        </div>
    );
};

const styles = {
    container: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        height: "100vh",
        justifyContent: "center",
        backgroundColor: "#f5f5f5", // Light background for contrast
    },
    dartboardContainer: {
        position: "relative",
        maxWidth: "60%",
        marginBottom: "20px", // Add space between the dartboard and the button
    },
    dartboard: {
        width: "100%",
        cursor: "pointer",
    },
    resetButton: {
        padding: "10px 20px",
        fontSize: "16px",
        color: "white",
        backgroundColor: "#007BFF", // Blue button
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
    },
};

export default Dartboard;
