export interface UserCreate {
  display_name: string
  email: string
  password: string
}

export interface Token {
  display_name: string
  access_token: string
}

export interface AuthState {
  user: string | null
  token: string | null
}
