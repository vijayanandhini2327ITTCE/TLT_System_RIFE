import React from "react";
import { LineVideoInfo } from "../types/tlt";

interface ScanLineSelectorProps {
  lines: LineVideoInfo[];
  selectedLine: number | null;
  onSelect: (lineIndex: number) => void;
}

const ScanLineSelector: React.FC<ScanLineSelectorProps> = ({
  lines,
  selectedLine,
  onSelect
}) => {
  if (lines.length === 0) {
    return null;
  }

  return (
    <div className="scanline-selector">
      <h3>Select B-scan line</h3>
      <div className="line-buttons">
        {lines.map((line) => (
          <button
            key={line.line_index}
            className={
              selectedLine === line.line_index ? "line-btn selected" : "line-btn"
            }
            onClick={() => onSelect(line.line_index)}
          >
            Line {line.line_index}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ScanLineSelector;
