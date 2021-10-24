<template>

<div id="login">
    <img src="../assets/logo.png"/>
    <h2 v-if="!loggedIn">Logg inn</h2>
    <h2 v-if="loggedIn">Du er logget inn</h2>

    <form @submit.prevent="handleSubmit">
        <div id="login_form">
                <label for="username">Brukernavn:</label>
                <input type="text" id="username" name="username" placeholder="Brukernavn" required v-model="username">
                <label for="password">Passord:</label>
                <input type="password" id="password" name="password" placeholder="Passord" required v-model="password">
                <div v-if="passwordError">{{ passwordError }}</div>
        </div>

    <div id="login_buttons">
        <input type="submit" value="Logg inn">
        <router-link to="/register"><input type="submit" value="Registrer ny bruker"></router-link>
    </div>
    </form>
</div>

</template>



<script>
let baseURL = "http://127.0.0.1:5000/";

export default {
  name: 'Login',
  data() {
    return {
        username: '',
        password: '',
        passwordError: '',
        loggedIn: false
    }
  },
  methods: {
      // Login user
      async handleSubmit() {
        let response = await fetch(baseURL + "login", {
            credentials: 'include',
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username: this.username, password: this.password })
        });
        if (response.status != 200) {
            console.log("error")
        }
        let user = await response.json();

        // Store user's username, firstname, lastname in sessionStorage
        sessionStorage.setItem("username", user["username"]);
        sessionStorage.setItem("firstname", user["firstname"]);
        sessionStorage.setItem("lastname", user["lastname"]);

        // reload page (login-button changes to logout-button)
        window.location.reload(true)
      }
    },
    created() {
        // Check if the user is logged in
        if (sessionStorage["username"]) {
            this.loggedIn = true;
        }
    }
}
</script>
