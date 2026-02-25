import axios from "axios";
import type {
  AnalysisReport,
  AnalysisStatusResponse,
  AnalyzeResponse,
} from "@/types/report";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL?.trim() ||
  "http://127.0.0.1:8000";

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 60_000,
});

export const analyzeSample = async (
  file: File,
): Promise<AnalyzeResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post<AnalyzeResponse>(
    "/analyze",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
};

export const fetchAnalysisStatus = async (
  id: string,
): Promise<AnalysisStatusResponse> => {
  const response = await apiClient.get<AnalysisStatusResponse>(
    `/status/${id}`,
  );

  return response.data;
};

export const fetchReport = async (id: string): Promise<AnalysisReport> => {
  const response = await apiClient.get<AnalysisReport>(`/reports/${id}`);

  return response.data;
};
