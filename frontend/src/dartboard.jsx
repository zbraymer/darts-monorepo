import React, { useEffect } from "react";

const Dartboard = () => {
    useEffect(() => {
        const canvas = document.getElementById("dartboard");
        const ctx = canvas.getContext("2d");

        const dartboardRadius = canvas.width / 2; // Radius of the dartboard
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        const segments = [
            6, 13, 4, 18, 1, 20, 5, 12, 9, 14,
            11, 8, 16, 7, 19, 3, 17, 2, 15, 10,
        ];
        const colors = ["black", "white"];

        // Draw the dartboard
        const drawDartboard = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw the dartboard rings
            drawRing(dartboardRadius, 0.95, "#000");
            drawRing(dartboardRadius * 0.8, 0.8, "#000");
            drawRing(dartboardRadius * 0.15, 0.15, "#000");

            // Draw numbered segments
            const segmentAngle = (2 * Math.PI) / segments.length;
            for (let i = 0; i < segments.length; i++) {
                const startAngle = i * segmentAngle - Math.PI / 2;
                const endAngle = startAngle + segmentAngle;

                // Alternate colors
                ctx.fillStyle = colors[i % 2];
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, dartboardRadius * 0.95, startAngle, endAngle);
                ctx.closePath();
                ctx.fill();

                // Draw segment labels
                drawLabel(segments[i], startAngle + segmentAngle / 2, dartboardRadius * 0.85);
            }
        };

        const drawRing = (radius, widthRatio, color) => {
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius * widthRatio, 0, 2 * Math.PI);
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.stroke();
        };

        const drawLabel = (text, angle, distance) => {
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(angle);
            ctx.textAlign = "center";
            ctx.fillStyle = "black";
            ctx.font = "14px Arial";
            ctx.fillText(text, 0, -distance);
            ctx.restore();
        };

        const handleClick = (event) => {
            const rect = canvas.getBoundingClientRect();

            const x = event.clientX - rect.left - centerX;
            const y = centerY - (event.clientY - rect.top);

            const radius = Math.sqrt(x ** 2 + y ** 2);
            const normalizedRadius = radius / dartboardRadius;
            const angle = Math.atan2(y, x) * (180 / Math.PI);
            const adjustedAngle = (angle + 360) % 360;

            displayClickInfo(adjustedAngle.toFixed(2), normalizedRadius.toFixed(2));
        };

        const displayClickInfo = (angle, radius) => {
            drawDartboard();
            ctx.fillStyle = "black";
            ctx.font = "16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(`Angle: ${angle}°`, centerX, canvas.height - 50);
            ctx.fillText(`Radius: ${radius}`, centerX, canvas.height - 30);
        };

        canvas.addEventListener("click", handleClick);

        // Initial draw
        drawDartboard();

        // Cleanup event listener
        return () => {
            canvas.removeEventListener("click", handleClick);
        };
    }, []);

    return <canvas id="dartboard" width="500" height="500" style={{ border: "1px solid #000" }} />;
};

export default Dartboard;
