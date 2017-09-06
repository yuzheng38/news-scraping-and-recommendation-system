class Auth {
    /**
     * Helper class to handle user authentication. 
     */
    static authenticateUser(token, email) {
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
    }

    /**
     * Check if a user is authenticated
     */
    static isUserAuthenticated() {
        return localStorage.getItem('token') !== null;
    }

    /**
     * De-authenticate a user
     */
    static deauthenticate() {
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    }

    /**
     * Getter for token
     */
    static getToken() {
        return localStorage.getItem('token');
    }

    /**
     * Getter for email
     */
    static getEmail() {
        return localStorage.getItem('email');
    }
}

export default Auth;