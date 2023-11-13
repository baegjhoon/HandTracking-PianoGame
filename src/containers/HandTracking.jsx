import React, { useCallback, useEffect, useRef } from "react";
import Webcam from "react-webcam";
import { css } from "@emotion/css";
import { Camera } from "@mediapipe/camera_utils";
import { Hands } from "@mediapipe/hands";
import { drawCanvas } from "../utils/drawCanvas";

const HandTracking = () => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  const resultsRef = useRef();

  /**
   * 검출결과 (프레임마다 호출됨)
   * @param results
   */
  const onResults = useCallback((results) => {
    resultsRef.current = results;

    const canvasCtx = canvasRef.current?.getContext("2d");
    if (canvasCtx) {
      drawCanvas(canvasCtx, results);
    }
  }, []);

  // 초기 설정
  useEffect(() => {
    const hands = new Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      },
    });

    hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    hands.onResults(onResults);

    if (webcamRef.current) {
      const camera = new Camera(webcamRef.current.video, {
        onFrame: async () => {
          await hands.send({ image: webcamRef.current.video });
        },
        width: 1280,
        height: 720,
      });
      camera.start();
    }
  }, [onResults]);

  /* 랜드마크들의 좌표를 콘솔에 출력 */
  const OutputData = () => {
    const results = resultsRef.current;

    if (results && results.multiHandLandmarks) {
      console.log(results.multiHandLandmarks);
    } else {
      console.error("Results or multiHandLandmarks are undefined.");
    }
  };

  return (
    <div className={styles.container}>
      {/* 비디오 캡쳐 */}
      <Webcam
        audio={false}
        style={{ visibility: "hidden" }}
        width={1280}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={{ width: 1280, height: 720, facingMode: "user" }}
      />

      {/* 랜드마크를 손에 표시 */}
      <canvas
        ref={canvasRef}
        className={styles.canvas}
        width={1280}
        height={720}
      />
      {/* 좌표 출력 */}
      <div className={styles.buttonContainer}>
        <button className={styles.button} onClick={OutputData}>
          Output Data
        </button>
      </div>
    </div>
  );
};

// ==============================================
// styles

const styles = {
  container: css`
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  `,
  canvas: css`
    position: absolute;
    width: 1280px;
    height: 720px;
    background-color: #fff;
  `,
  buttonContainer: css`
    position: absolute;
    top: 20px;
    left: 20px;
  `,
  button: css`
    color: #fff;
    background-color: #0082cf;
    font-size: 1rem;
    border: none;
    border-radius: 5px;
    padding: 10px 10px;
    cursor: pointer;
  `,
};

export default HandTracking;
