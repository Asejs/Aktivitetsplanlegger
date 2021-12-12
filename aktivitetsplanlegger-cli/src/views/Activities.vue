<template>

<main>
    <h1 v-if="loggedIn">Velkommen {{ firstname }} {{ lastname }}!</h1>
    <h1 v-if="!loggedIn">Velkommen!</h1>
    <h1>Utforsk aktiviteter</h1>
        
    <div v-if="loggedIn">
      <AddActivity/>
    </div>
    <div v-if="!loggedIn">
      <div id="container">
        <div id="buttons">
            <button style="opacity: 60%" @click="isVisible = true">+ Legg til ny aktivitet</button>
            <p style="color: white"><router-link to="/login" style="color: white"><u><b>Logg inn</b></u></router-link> for å legge til en ny aktivitet</p>

        </div>
      </div>
    </div>
      
    <div id="content">
        <Activity />
    </div>
</main>

</template>



<script>
import AddActivity from '../components/AddActivity';
import Activity from '../components/Activity';


export default {
  name: 'Aktiviteter',
  components: {
      AddActivity,
      Activity
  },
  data() {
    return {
      user: "",
      firstname: "",
      lastname: "",
      loggedIn: false
      }
  },
  created() {
    if (sessionStorage["username"]) {
      this.firstname = sessionStorage.getItem("firstname");
      this.lastname = sessionStorage.getItem("lastname");
      this.loggedIn = true
    }
  }
}

</script>

