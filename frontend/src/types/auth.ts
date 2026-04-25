export interface UserCreate {
  display_name: string
  email: string
  password: string
}

export interface Token {
  display_name: string
  access_token: string
}

export interface UserRead {
  id: string
  display_name: string
  email: string
}

export interface AuthState {
  user: UserRead | null
  token: string | null
  isInitialized: boolean
  isVerified: boolean
}
