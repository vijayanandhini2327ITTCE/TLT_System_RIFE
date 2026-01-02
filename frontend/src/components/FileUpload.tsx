import React, { useState } from "react";

interface FileUploadProps {
  onUploaded: (sessionId: string, numLines: number) => void;
  onLoadingChange: (loading: boolean) => void;
  uploadHandler: (
    day1: File,
    day30: File
  ) => Promise<{ session_id: string; num_lines: number }>;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onUploaded,
  onLoadingChange,
  uploadHandler
}) => {
  const [day1File, setDay1File] = useState<File | null>(null);
  const [day30File, setDay30File] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!day1File || !day30File) {
      setError("Please select both Day-1 and Day-30 volumes.");
      return;
    }
    setError(null);
    onLoadingChange(true);
    try {
      const res = await uploadHandler(day1File, day30File);
      onUploaded(res.session_id, res.num_lines);
    } catch {
      setError("Upload or processing failed. Please try again.");
    } finally {
      onLoadingChange(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="file-upload">
      <div className="field">
        <label>Day-1 OCT volume:</label>
        <input
          type="file"
          accept=".zip,.png,.jpg,.jpeg"
          onChange={(e) => setDay1File(e.target.files?.[0] || null)}
        />
      </div>
      <div className="field">
        <label>Day-30 OCT volume:</label>
        <input
          type="file"
          accept=".zip,.png,.jpg,.jpeg"
          onChange={(e) => setDay30File(e.target.files?.[0] || null)}
        />
      </div>
      <button type="submit">Generate Time-Lapse</button>
      {error && <p className="error">{error}</p>}
    </form>
  );
};

export default FileUpload;
