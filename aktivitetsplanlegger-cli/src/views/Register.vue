<template>

<div id="register" class="bg-color">

    <div id="back_button">
        <router-link to="/login">
        <button type="button"><i class="fa fa-chevron-left fa-2x"></i></button>
        </router-link>
    </div>

    <div id="register_text">
    <h2>Registrer ny bruker</h2>
    </div>

    <form @submit.prevent="handleSubmit">
        <div id="register_form">
                <label>Brukernavn:</label>
                <input type="text" id="username" name="username" placeholder="Brukernavn" required v-model="username">
                <label>Fornavn:</label>
                <input type="text" id="firstname" name="firstname" placeholder="Fornavn" required v-model="firstname">
                <label>Etternavn:</label>
                <input type="text" id="lastname" name="lastname" placeholder="Etternavn" required v-model="lastname">
                <label>Email:</label>
                <input type="email" id="email" name="email" placeholder="Email" required v-model="email">
                <label>Passord:</label>
                <input type="password" id="password" name="password" placeholder="Passord" required v-model="password">
                <label>Gjenta passord:</label>
                <input type="password" id="repeatPassword" name="repeatPassword" placeholder="Gjenta passord" required v-model="repeatPassword">
        </div>    
        <div id="error" v-if="error">{{ error }}</div>
        <input type="submit" value="Registrer ny bruker"><br>
    </form>

</div>

</template>

<script>
let baseURL = "http://127.0.0.1:5000/";

export default {
  name: 'Register',
  data() {
      return {
          username: null,
          firstname: null,
          lastname: null,
          email: null,
          password: null,
          repeatPassword: null,
          error: null,
    }
  },  
  methods: {
    // signup user
    async handleSubmit() {
        event.preventDefault();

        // Password error handling:
        if (this.password != this.repeatPassword) {
            this.error = "Passordene må være like.";
            return 'error'
        }
        
        if (this.password.length < 5 ) {
            this.error = "Passordet må inneholde minst 6 tegn."
            return 'error'
        }

        let user = {
            "username": this.username,
            "firstname": this.firstname,
            "lastname": this.lastname,
            "email": this.email,
            "password": this.password,
        };

        let response = await fetch(baseURL + "register", {
            credentials: 'include',
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user)
        });
        console.log(result)
        let result = await response.json();

        if (result['register'] == "success") {
            this.username = this.firstname = this.lastname = this.password = this.repeatPassword = null;
            await alert("Du er registrert.");
            this.$router.push('/login')
        }
        else {
            this.error = result['error'];
        }
    },
  }
}
</script>