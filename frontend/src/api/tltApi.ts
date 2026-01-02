import axios from "axios";
import { TLTProcessResponse, LineVideoInfo } from "../types/tlt";

// Configure this to match your backend base URL
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function uploadVolumes(
  day1File: File,
  day30File: File
): Promise<TLTProcessResponse> {
  const formData = new FormData();
  formData.append("day1_zip", day1File);
  formData.append("day30_zip", day30File);

  const res = await axios.post<TLTProcessResponse>(
    `${API_BASE}/tlt/process`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  );
  return res.data;
}

export async function fetchLineVideos(
  sessionId: string
): Promise<LineVideoInfo[]> {
  const res = await axios.get<LineVideoInfo[]>(`${API_BASE}/tlt/lines`, {
    params: { session_id: sessionId }
  });
  return res.data;
}

export function buildVideoUrl(relativeUrl: string): string {
  // Backend returns '/tlt/video?...' relative to API base
  return `${API_BASE}${relativeUrl}`;
}
