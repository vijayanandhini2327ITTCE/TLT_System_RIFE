import React, { useEffect, useRef } from "react";
import type { PlaybackSpeed } from "./PlaybackControls";

interface TimeLapsePlayerProps {
  videoUrl: string | null;
  speed: PlaybackSpeed;
}

const TimeLapsePlayer: React.FC<TimeLapsePlayerProps> = ({ videoUrl, speed }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    if (videoRef.current) {
      const rateMap: Record<PlaybackSpeed, number> = {
        slow: 0.5,
        normal: 1.0,
        fast: 2.0
      };
      videoRef.current.playbackRate = rateMap[speed];
    }
  }, [speed]);

  if (!videoUrl) {
    return <div className="player-placeholder">Select a line to view time-lapse.</div>;
  }

  return (
    <div className="time-lapse-player">
      <video
        ref={videoRef}
        src={videoUrl}
        controls
        width={640}
        height={360}
      />
    </div>
  );
};

export default TimeLapsePlayer;
