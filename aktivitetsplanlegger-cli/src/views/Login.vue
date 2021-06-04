<template>


    <div id="login">
        <img src="../assets/logo.png"/>
        <h2>Logg inn</h2>

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
        passwordError: ''
    }
  },
  
  methods: {
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
            //let result = await request.json();
            // returned data
        }
        
        let user = await response.json();
        console.log(user)
        sessionStorage.setItem("username", user["username"]);
        sessionStorage.setItem("firstname", user["firstname"]);
        sessionStorage.setItem("lastname", user["lastname"]);

        this.$router.push('/activities')
      }
    },
    created() {
      if (sessionStorage["username"]) {
          //
      }
    }
}
</script>
