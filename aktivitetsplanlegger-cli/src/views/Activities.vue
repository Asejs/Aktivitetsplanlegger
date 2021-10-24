<template>

<main>
    <h1 v-if="loggedIn" style="color: white">Velkommen {{ firstname }} {{ lastname }}!</h1>
    <h1 v-if="!loggedIn" style="color: white">Velkommen!</h1>
    <h1 style="color: white">Utforsk aktiviteter</h1>
        
    <div v-if="loggedIn">
      <AddActivity/>
    </div>

    <div style="color: white" v-if="!loggedIn">
      Logg inn for å legge til en ny aktivitet
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

