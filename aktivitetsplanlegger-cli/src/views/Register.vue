<template>

    <div id="register">

        
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
                    <div v-if="passwordError">{{ passwordError }}</div>
            </div>
        
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
          username: '',
          firstname: '',
          lastname: '',
          email: '',
          password: '',
          passwordError: ''
    }
  },  
  methods: {
        async handleSubmit() {
            console.log("Form submitted.")
            // validate passwords
            let response = await fetch(baseURL + "signup", {
                credentials: 'include',
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: this.username, firstname: this.firstname, lastname: this.lastname, email: this.email, password: this.password })
            });
            if (response.status != 200){
                console.log("error")
                return 'error'
                }

            if (this.password.length < 5 ) {
                this.passwordError = "Passordet må inneholde minst 6 tegn."
                return 'error'
            }

            else {
                console.log("Registrert med brukernavn:", this.username)
                await alert("Du er registrert.");
                this.$router.push('/login')
            }
            
            
            //let user = await response.json();
            console.log(response);
            //let logoutform = document.getElementById("logoutform");
            //logoutform.style.display = "block";
            //document.getElementById("loggedinname").innerText = user.username;
            
            // an alternative to this call would be 
            // returning the addresses as a field of the user
            //getAddresses();
            //this.clearForm();
        },
        clearForm() {
            this.username = '',
            this.firstname = '',
            this.lastname = '',
            this.email = '',
            this.password = ''
        }
  }
}
/*
TO DO:
1. checkform i methods:
this.errors =[];
https://vuejs.org/v2/cookbook/form-validation.html


*/
</script>