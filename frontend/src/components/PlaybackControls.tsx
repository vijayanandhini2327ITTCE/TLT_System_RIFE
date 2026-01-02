import React from "react";

export type PlaybackSpeed = "slow" | "normal" | "fast";

interface PlaybackControlsProps {
  speed: PlaybackSpeed;
  onSpeedChange: (speed: PlaybackSpeed) => void;
}

const PlaybackControls: React.FC<PlaybackControlsProps> = ({
  speed,
  onSpeedChange
}) => {
  return (
    <div className="playback-controls">
      <span>Playback speed:</span>
      <button
        className={speed === "slow" ? "selected" : ""}
        onClick={() => onSpeedChange("slow")}
      >
        Slow
      </button>
      <button
        className={speed === "normal" ? "selected" : ""}
        onClick={() => onSpeedChange("normal")}
      >
        Normal
      </button>
      <button
        className={speed === "fast" ? "selected" : ""}
        onClick={() => onSpeedChange("fast")}
      >
        Fast
      </button>
    </div>
  );
};

export default PlaybackControls;
