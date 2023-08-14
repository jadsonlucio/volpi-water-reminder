export interface LoginForm {
  username: string;
  password: string;
}

export interface AuthResponse {
  auth_token: string;
  refresh_token: string;
  expiration_datetime: string;
}

export interface RegisterForm {
  username: string;
  password: string;
  confirm_password: string;
  first_name?: string;
  last_name?: string;
  email: string;
  weight: number;
}

export interface User {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  weight: string;
  daily_goal_ml: number;
}

// water consumption interfaces

export interface WaterConsumptionFilter {
  date_before?: Date;
  date_after?: Date;
}

export interface WaterConsumptionForm {
  id?: string;
  date: Date;
  consumption_ml: number;
}

export interface WaterConsumptionRecord {
  id: number;
  date: string;
  consumption_ml: number;
}
