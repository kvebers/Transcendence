import React, { useEffect, useRef, useState } from "react";

const Pong = () => {
  const sender = useRef(null);
  const player0 = useRef(null);
  const player1 = useRef(null);
  const gameSocket = useRef(null);
  const [receivedData, setReceivedData] = useState(null);

  useEffect(() => {
    async function getData() {
      gameSocket.current = new WebSocket("wss://localhost/game/asdfasdf/");

      let canvas = document.getElementById("gameCanvas");
      let context = canvas.getContext("2d");
      gameSocket.current.onmessage = function (event) {
        setReceivedData(JSON.parse(event.data));
        console.log("received data: " + event.data)

        let room_name = receivedData.current["room_name"];
        let gameState = receivedData.current["game_state"];
        let users = receivedData.current["users"];

        console.log("data" + users, room_name, gameState);
        sender.current = receivedData.current["users"][0];
        player0.current = receivedData.current["users"][0];
        player1.current = receivedData.current["users"][1];
        if (receivedData.current["type"] === "game_message") {
          console.log("rendering game frame" + event.data);
          renderGameFrame(receivedData.current);
        }
        else if (receivedData.current["type"] === "ending_message") {
          window.location.href =
            "https://localhost/game/ending/?gameinfo=" +
            receivedData.current["score"] +
            "&gametag=" +
            receivedData.current["game_tag"] +
            "&roomname=" +
            room_name;
        }
      };

      const renderGameFrame = (gameData) => {
        if (context && canvas) {
          clearCanvas();
          drawField();
          var score = player0.current + "  " + gameData.score + " " + player1.current;
          displayScore(score);
          drawPaddle(0, gameData.player0, 10, 110);
          drawPaddle(1, gameData.player1, 10, 110);
          drawBall(
            gameData.ball_x,
            gameData.ball_y,
            gameData.ball_speed_x,
            gameData.ball_speed_y,
            gameData.ball_speed
          );
        }
        console.log("gameData::::::: " + gameData, gameData.player0);
      };

      const clearCanvas = () => {
        if (context && canvas) {
          context.clearRect(0, 0, canvas.width, canvas.height);
        }
      };

      function hexToRgb(hex) {
        // Remove the hash if it exists
        hex = hex.replace(/^#/, "");

        // Parse the hex values to separate R, G, B components
        const bigint = parseInt(hex, 16);
        const r = (bigint >> 16) & 255;
        const g = (bigint >> 8) & 255;
        const b = bigint & 255;

        // Return the RGB values as an object
        return { r, g, b };
      }

      const drawBall = (x, y, speedX, speedY, ballSpeed) => {
        if (context) {
          // Define a color gradient based on speed
          const colorGradient = [
            { speed: 7, color: "#ffff00" },
            { speed: 10, color: "#ff4d00" },
            { speed: 13, color: "#ff0000" },
            { speed: 18, color: "#0000ff" },
            { speed: 50, color: "#bf00ff" },
          ];

          // Find the color corresponding to the ball's speed in the gradient
          let ballColor = "white"; // Default color
          for (const { speed, color } of colorGradient) {
            if (ballSpeed <= speed) {
              ballColor = color;
              break;
            }
          }

          // Display the magnitude of the speed
          context.fillStyle = ballColor;
          context.font = "14px Arial";
          let show_speed = `Speed: ${ballSpeed.toFixed(3)}`;
          context.fillText(show_speed, x - 30, y - 30);

          // Draw the main ball
          context.fillStyle = ballColor;
          context.beginPath();
          context.arc(x, y, 10, 0, Math.PI * 2);
          context.fill();
          context.closePath();

          // Draw the trailing circles
          const trailCount = 5; // Adjust the number of circles in the trail
          const trailSpacing = 1.5; // Adjust the spacing between circles in the trail

          for (let i = 1; i <= trailCount; i++) {
            const trailOpacity = 1 - i / trailCount;
            const trailRadius = i * trailSpacing;

            const rgb = hexToRgb(ballColor);
            context.fillStyle = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${trailOpacity})`; // Yellow color with variable opacity
            context.beginPath();
            context.arc(
              x - speedX * trailRadius,
              y - speedY * trailRadius,
              10,
              0,
              Math.PI * 2
            );
            context.fill();
            context.closePath();
          }
        }
      };

      const drawPaddle = (player, y, width, height) => {
        if (context) {
          if (player === 0) {
            context.fillStyle = "red"; // Player 0 Paddle color
            context.fillRect(0, y, width, height);
          } else {
            context.fillStyle = "blue"; // Player 1 Paddle color
            context.fillRect(790, y, width, height);
          }
        }
      };

      const drawField = () => {
        if (context) {
          context.fillStyle = "#ffffff";
          context.fillRect(398, 0, 4, 400);
        }
      };

      const displayScore = (score) => {
        if (context) {
          context.fillStyle = "white";
          context.fillRect(285, 5, 240, 70);
          context.fillStyle = "black";
          context.fillText("Score!", 295, 40);
          context.fillText(score, 300, 65);
        }
      };

      const handleKeyDown = (event) => {
        console.log(event.key)
        const user = sender.current;
        if (event.key === "w") {
          gameSocket.current.send("pw" + user);
        } else if (event.key === "s") {
          gameSocket.current.send("ps" + user);
        } else if (event.key === "i") {
          gameSocket.current.send("pi" + user);
        } else if (event.key === "k") {
          gameSocket.current.send("pk" + user);
        }
      };

      const handleKeyUp = (event) => {
        const user = sender.current;
        if (event.key === "w") {
          gameSocket.current.send("rw" + user);
        } else if (event.key === "s") {
          gameSocket.current.send("rs" + user);
        } else if (event.key === "i") {
          gameSocket.current.send("ri" + user);
        } else if (event.key === "k") {
          gameSocket.current.send("rk" + user);
        }
      };

      const startGame = () => {
        gameSocket.current.send("startgame");
      };

      document.addEventListener("keyup", handleKeyUp);
      document.addEventListener("keydown", handleKeyDown);
      const startButton = document.getElementById("startGame");
      startButton.addEventListener("click", startGame);

      // Cleanup function
      return () => {
        console.log("closing socket and removing listener");
        gameSocket.current.close();
        document.removeEventListener("keyup", handleKeyUp);
        document.removeEventListener("keydown", handleKeyDown);
        startButton.removeEventListener("click", startGame);
      };
    }
    getData();
  }, [receivedData]);

  return (
    <div
      id="game-container"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
      }}
    >
      <canvas
        id="gameCanvas"
        width="1000"
        height="700"
        style={{ backgroundColor: "black" }}
      ></canvas>
      <button id="startGame">Start Game</button>
    </div>
  );
};

export default Pong;
