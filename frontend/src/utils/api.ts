// helper functions
function normalizeHeaders(headers?: HeadersInit): Record<string, string> {
  if (!headers) return {}
  if (headers instanceof Headers) {
    return Object.fromEntries(headers.entries())
  }
  if (Array.isArray(headers)) {
    return Object.fromEntries(headers)
  }
  return headers
}

async function refreshAccessToken(): Promise<string | null> {
  const response = await fetch('http://127.0.0.1:8000/api/v1/auth/refresh', {
    method: 'POST',
    credentials: 'include',
  })

  if (!response.ok) return null

  const data = await response.json()
  localStorage.setItem('access_token', data.access_token)
  return data.access_token
}

// api error class
export class ApiError extends Error {
  status: number
  code?: string
  body?: unknown
  error?: string
  failureCases?: unknown

  constructor(status: number, code?: string, message: string = '', body?: unknown) {
    // If FastAPI sends a detail object, extract its fields
    let finalMessage = message
    let error: string | undefined
    let failureCases: unknown

    if (body && typeof body === 'object' && 'detail' in body) {
      const detail = body['detail'] as {
        message?: string
        error?: string
        failure_cases?: unknown
      }

      finalMessage = detail.message ?? message
      error = detail.error
      failureCases = detail.failure_cases
    }

    super(finalMessage)
    Object.setPrototypeOf(this, ApiError.prototype)

    this.status = status
    this.code = code
    this.body = body
    this.error = error
    this.failureCases = failureCases
  }
}

// unified fetch
export async function apiFetch<T = unknown>(
  url: string,
  options: RequestInit = {},
  retries: number = 3,
  retryDelay: number = 500,
  responseType: 'json' | 'text' | 'blob' | 'formData' = 'json',
): Promise<T> {
  const apiPath = 'http://127.0.0.1:8000/api/v1' + url
  let token = localStorage.getItem('access_token')

  const headers: Record<string, string> = {
    ...normalizeHeaders(options.headers),
  }

  // Only set Content-Type if body is plain object or string
  if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] ?? 'application/json'
    // auto-stringify plain objects
    if (!(options.body instanceof Blob) && !(options.body instanceof URLSearchParams)) {
      options.body = JSON.stringify(options.body)
    }
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  let attempt = 0
  while (attempt <= retries) {
    try {
      let response = await fetch(apiPath, {
        ...options,
        headers,
        credentials: 'include',
      })

      if (response.status === 401) {
        const newToken = await refreshAccessToken()
        if (newToken) {
          token = newToken
          headers['Authorization'] = `Bearer ${newToken}`
          response = await fetch(apiPath, {
            ...options,
            headers,
            credentials: 'include',
          })
        }
      }

      if (!response.ok) {
        let body: unknown
        try {
          body = await response.json()
        } catch {
          body = await response.text()
        }
        throw new ApiError(response.status, response.statusText, 'Request failed', body)
      }

      switch (responseType) {
        case 'json':
          return (await response.json()) as T
        case 'text':
          return (await response.text()) as unknown as T
        case 'blob':
          return (await response.blob()) as unknown as T
        case 'formData':
          return (await response.formData()) as unknown as T
      }
    } catch (err) {
      if (err instanceof ApiError) throw err
      if (attempt < retries) {
        await new Promise((res) => setTimeout(res, retryDelay * (attempt + 1)))
        attempt++
      } else {
        throw new ApiError(0, 'NetworkError', 'Failed to fetch after retries')
      }
    }
  }

  throw new ApiError(0, 'UnknownError', 'Unexpected failure in apiFetch')
}
