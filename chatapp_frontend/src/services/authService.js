import api from '../api/api';


export const AuthService = {
    login: async (userData) => {
        try{
            const response = await api.post("/login/", userData);
            return response.data
        }
        // eslint-disable-next-line no-unused-vars
        catch(error) {       
            // No need to add message.error here → interceptor already handles it
            return null;
        } 
    }
}