export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    hasMore?: boolean;
  };
}

export interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>;
}
