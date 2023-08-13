import { AuthResponse, LoginForm, RegisterForm, User } from './interface';
import { api } from '../boot/axios';

export const loginUser = async (
  loginForm: LoginForm
): Promise<AuthResponse> => {
  const { data } = await api.post('/auth/', loginForm);
  return data;
};

export const getCurrentUser = async (): Promise<User> => {
  const { data } = await api.get('/me/');
  return data;
};

export const registerUser = async (
  registerForm: RegisterForm
): Promise<User> => {
  const { data } = await api.post('/register/', registerForm);
  return data;
};
