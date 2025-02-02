import React, { useState } from "react";

const Dartboard = () => {
    const [clicks, setClicks] = useState([]); // Store click data
    const [target, setTarget] = useState(""); // Store the selected target number
    const markerSize = 10; // Marker size in pixels
    const offset = markerSize / 2; // Half of the marker size for centering

    // Handle dartboard click
    const handleClick = async (event) => {
        if (!target) {
            alert("Please select a target number before throwing.");
            return;
        }

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
            const response = await fetch(
                `http://localhost:8000/calculate-score?radius=${radius}&angle=${angle}`
            );

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

    // Handle form submission
    const handleSubmit = async () => {
        if (clicks.length !== 3) {
            alert("Please make exactly 3 throws before submitting.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/submit-throws", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    target,
                    throws: clicks.map((click) => ({
                        radius: click.radius,
                        angle: click.angle,
                    })),
                }),
            });

            if (!response.ok) {
                console.error("Error submitting data:", response.statusText);
                return;
            }

            const data = await response.json();
            console.log("Submission successful:", data);
            alert("Submission successful!");

            // Reset state after successful submission
            setClicks([]);
            setTarget("");
        } catch (error) {
            console.error("Error submitting data:", error);
        }
    };

    const handleClear = () => {
        setClicks([]); // Reset the clicks state
        setTarget(""); // Clear the selected target
    };

    // Handle target selection
    const handleTargetChange = (event) => {
        setTarget(event.target.value);
    };

    return (
        <div style={styles.container}>
            {/* Target Selection Dropdown */}
            <div style={styles.dropdownContainer}>
                <label htmlFor="target">Select Target:</label>
                <select
                    id="target"
                    value={target}
                    onChange={handleTargetChange}
                    style={styles.dropdown}
                >
                    <option value="" disabled>
                        Select a number
                    </option>
                    {[...Array(20).keys()].map((i) => (
                        <option key={i + 1} value={i + 1}>
                            {i + 1}
                        </option>
                    ))}
                    <option value="bullseye">Bullseye</option>
                </select>
            </div>

            <div style={styles.dartboardContainer}>
                {/* Dartboard Image */}
                <img
                    src="/dartboard.png"
                    alt="Dartboard"
                    onClick={handleClick}
                    style={styles.dartboard}
                />

                {/* Render Click Markers */}
                {clicks.map((click, index) => (
                    <React.Fragment key={index}>
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
                    </React.Fragment>
                ))}
            </div>

            {/* Buttons */}
            <div style={styles.buttonContainer}>
                <button onClick={handleSubmit} style={styles.submitButton}>
                    Submit
                </button>
                <button onClick={handleClear} style={styles.resetButton}>
                    Reset
                </button>
            </div>
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
    dropdownContainer: {
        marginBottom: "10px",
    },
    dropdown: {
        marginLeft: "10px",
        padding: "5px",
    },
    dartboardContainer: {
        position: "relative",
        maxWidth: "60%",
        marginBottom: "20px",
    },
    dartboard: {
        width: "100%",
        cursor: "pointer",
    },
    buttonContainer: {
        display: "flex",
        gap: "10px",
    },
    submitButton: {
        padding: "10px 20px",
        backgroundColor: "#28a745",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
    resetButton: {
        padding: "10px 20px",
        backgroundColor: "#dc3545",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
};

export default Dartboard;
