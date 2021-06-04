<template>

<main>
    <!-- <h1 v-if="user">Hi, {{user.firstname}} {{user.last_name}}</h1> -->
    <!-- v-if="!user" -->
    <h1 v-if="loggedIn" style="color: white">Velkommen {{ firstname }} {{ lastname }}!</h1>
    <h1 v-if="!loggedIn" style="color: white">Velkommen!</h1>
    <h1 style="color: white">Utforsk aktiviteter</h1>
        
      <!--
      <div id="buttons">
        <select type="number" name="size" id="size" style="width: 150px">
          <option value="1" selected>Filtrer</option>
          <option value="2">Utendørs</option>
          <option value="3">Innendørs</option>
      </select>
      </div>
      -->

    
    <div v-if="loggedIn">
      <AddActivity/>
    </div>

    <div v-if="!loggedIn">
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

//let baseURL = "http://127.0.0.1:5000/";


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

