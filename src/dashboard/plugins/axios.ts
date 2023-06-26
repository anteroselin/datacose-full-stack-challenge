import { Plugin } from '@nuxt/types';
import { NuxtAxiosInstance } from '@nuxtjs/axios';

const axiosPlugin: Plugin = (context, inject) => {
  const { $axios } = context;

  // Create a separate Axios instance for API requests
  const api: NuxtAxiosInstance = $axios.create();

  // Interceptor to set Authorization header before each request
  api.interceptors.request.use((config) => {
    const accessToken = localStorage.getItem('access-token');
    if (accessToken) {
      config.headers.common['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  });

  inject('axios', api);
};

export default axiosPlugin;
