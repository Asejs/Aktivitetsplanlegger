<template>

<div id="container">
  <header>
    <div id="logo">
        <router-link to="/"><img src="@/assets/logo.png"/></router-link>
    </div>
    
    <nav>
        <ul>
            <router-link to="/activities"><li>Utforsk aktiviteter</li></router-link>
            <router-link :key="$route.fullPath" to="/login"><li v-if="!loggedIn"><strong>Logg inn</strong></li></router-link>
            <li v-if="loggedIn" @click="logout" style="color: white"><strong>Logg ut</strong></li>
        </ul>
    </nav>
  </header>

  <router-view/>

</div>

</template>


<script>
import '@/assets/css/style.css';

let baseURL = "http://127.0.0.1:5000/";

export default {
    data() {
        return {
            loggedIn: this.checkIfIsLoggedIn()
        }
    },
    methods: {
        // logout
        async logout() {
            let response = await fetch(baseURL + "logout");
            if (response.status != 200){
                alert("Failed to log out!");
                return
            }
            sessionStorage.clear()
            window.location.reload(true)
            this.loggedIn = false
        },
        checkIfIsLoggedIn() {
            if (sessionStorage["username"]) {
                this.loggedIn = true
                return true
            } else {
                return false
            } 
        }
    },
    mounted() {
        this. checkIfIsLoggedIn()
        if (sessionStorage["username"]) {
            this.loggedIn = true
        }
    }
}
</script>