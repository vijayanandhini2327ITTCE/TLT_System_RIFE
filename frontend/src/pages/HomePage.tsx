import React, { useEffect, useState } from "react";
import FileUpload from "../components/FileUpload";
import ScanLineSelector from "../components/ScanLineSelector";
import TimeLapsePlayer from "../components/TimeLapsePlayer";
import PlaybackControls, { PlaybackSpeed } from "../components/PlaybackControls";
import { uploadVolumes, fetchLineVideos, buildVideoUrl } from "../api/tltApi";
import { LineVideoInfo } from "../types/tlt";

const HomePage: React.FC = () => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [numLines, setNumLines] = useState<number>(0);
  const [lines, setLines] = useState<LineVideoInfo[]>([]);
  const [selectedLine, setSelectedLine] = useState<number | null>(null);
  const [speed, setSpeed] = useState<PlaybackSpeed>("normal");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) return;
    (async () => {
      try {
        const data = await fetchLineVideos(sessionId);
        setLines(data);
        setError(null);
        if (data.length > 0) {
          setSelectedLine(data[0].line_index);
        }
      } catch {
        setError("Failed to load line videos for this session.");
      }
    })();
  }, [sessionId]);

  const handleUploaded = (sid: string, nl: number) => {
    setSessionId(sid);
    setNumLines(nl);
    setLines([]);
    setSelectedLine(null);
    setError(null);
  };

  const currentVideoUrl =
    selectedLine != null && sessionId
      ? buildVideoUrl(
          `/tlt/video?session_id=${encodeURIComponent(
            sessionId
          )}&line_index=${selectedLine}`
        )
      : null;

  return (
    <div className="container">
      <h1>Automated Time Lapse Tomography (TLT)</h1>
      <p className="subtitle">
        Upload Day-1 and Day-30 OCT volumes to visualize 30-day retinal changes per B-scan line.
      </p>

      <FileUpload
        onUploaded={handleUploaded}
        onLoadingChange={setLoading}
        uploadHandler={uploadVolumes}
      />

      {loading && <p className="status">Processing OCT volumes, please wait...</p>}
      {error && <p className="error">{error}</p>}

      {sessionId && (
        <div className="session-info">
          <p>Session ID: {sessionId}</p>
          <p>Total B-scan lines: {numLines}</p>
        </div>
      )}

      {sessionId && lines.length > 0 && (
        <>
          <ScanLineSelector
            lines={lines}
            selectedLine={selectedLine}
            onSelect={setSelectedLine}
          />
          <PlaybackControls speed={speed} onSpeedChange={setSpeed} />
          <TimeLapsePlayer videoUrl={currentVideoUrl} speed={speed} />
        </>
      )}
    </div>
  );
};

export default HomePage;
