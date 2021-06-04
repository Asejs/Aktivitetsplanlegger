<template>
  <header>
    <div id="logo">
        <router-link to="/"><img src="@/assets/logo.png"/></router-link>
    </div>
    
    <nav>
        <ul>
            <router-link to="/activities"><li>Utforsk aktiviteter</li></router-link>
            <router-link to="/login"><li v-if="!loggedIn"><strong>Logg inn</strong></li></router-link>
            <li v-if="loggedIn" @click="logout" style="color: white"><strong>Logg ut</strong></li>
        </ul>
    </nav>

  </header>

  <!-- i router view kommer viewet; feks: home/login osv. -->
  <router-view/>


</template>


<script>
let baseURL = "http://127.0.0.1:5000/";

export default {
    data() {
        return {
            loggedIn: false
        }
    },
    methods: {
        async logout() {
            let response = await fetch(baseURL + "logout");
            if (response.status != 200){
                alert("Failed to log out!");
                return
            }
            sessionStorage.clear()
            window.location.reload(true)
        }
    },
    created() {
        if (sessionStorage["username"]) {
            this.loggedIn = true
    }

    }
}
</script>


<!-- --------------------------------------------------- -->




<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Raleway&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@100&display=swap');

@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&display=swap');

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@100&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Old+Standard+TT:wght@700&display=swap');

/* ----------------------------------------------- */

#links {
    position: relative;
    top: 100px;
}

html {
    height: 100%;
}

* {
    margin: 0px;
}

body {
    background-color: #aab39e;
    min-height: 100%;
    height: 100%;
    font-family: 'Roboto', sans-serif;
}


h1 {
    padding-bottom: 20px;
    color: white;
    font-size: 1.3em;
    text-align: center;
}

h2 {
    padding: 30px;
    color: #5e5e5e;
    font-size: 1.0em;
    
}

h3 {
    color: #2d2d2d;

    font-size: 1.2em;
    margin-bottom: 15px;
}

h4 {
    color: #727272;
    font-family: 'Roboto', sans-serif;
    font-size: 0.9em;
    font-weight: 700;
    line-height: 160%;
}


p {
    color: #212121;
    font-family: 'Open Sans', sans-serif;
    font-size: 0.8em;
    margin-top: 10px;
    margin-bottom: 10px;
}

a {
    color: #FFFFFF;
    text-decoration: none;
}

router-link {
    color: #FFFFFF;
    text-decoration: none;

}

a:hover {
    text-decoration: none;
}

i {
    margin-right: 5px;
}

/* ----------------------------------------------- */


#homepage {
    top: 60px;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-right: 0px;
    margin-left: 0px;
}

#homepage img {
    width: 100%;
    max-width: 1800px;
}

#home_description {
    position: relative;
    color: white;

    background-color: rgb(113, 125, 108);
    flex: 1;
    width: 100%;
    padding-left: 60px;
    padding-top: 30px;
    padding-bottom: 40px;
    padding-right: 200px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 2px 0px;
    max-width: 1800px;
    margin-top: -20px;
}

#home_description img {
    max-width: 500px;
    min-width: 100px;
    margin: 0px;
}

/* ----------------------------------------------- */

#login {
    border-radius: 10px;
    padding: 20px;
    position: relative;
    margin-left: auto;
    margin-right: auto;
    top: 120px;
    background-color: #909b83;
    width: 450px;
    height: 680px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 2px 0px;
}

#login label {
    color: white;
    padding: 0px;
    text-align: left;
    font-weight: 900;
    margin-top: 1px;
}

#login img {
    display: flex;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: -90px;
}

#login_form {
    display: flex;
    flex-direction: column;
    height: 100px;
    justify-content: flex-end;
}

#login_buttons {
    display: flex;
    flex-direction: column;
    height: 150px;
    margin-top: 25px;
}

#login input {
    margin-bottom: 5px;
    width: 290px;
}


#login h2 {
    color: white;
}

/* ----------------------------------------------- */

#back_button {
    display: flex;
    align-items: left;
    position: relative;
    top: 20px;
    width: 100%;
}

#register {
    border-radius: 10px;
    padding: 10px;
    position: relative;
    margin-left: auto;
    margin-right: auto;
    top: 120px;
    background-color: #909b83;
    width: 450px;
    height: 680px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 2px 0px;
}

#register label {
    color: white;
    padding: 0px;
    text-align: left;
    font-weight: 900;
    margin-top: 1px;
}

#register button {
    background-color: transparent;
    position: relative;
    justify-content: left;
    width: 40px;
}

#register input[type=submit] {
    margin-top: 30px;
}

#register h2 {
    color: white;
    margin-top: 20px;
}

#register_form {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 350px;
}

#register input {
    margin-bottom: 5px;
    width: 290px;
}

/* ----------------------------------------------- */


header {
    height: 60px;
    width: 100%;
    min-width: 600px;

    background-color: #909b83;
    position: fixed;
    top: 0px;
    z-index: 1;
    font-size: 0.8em;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 2px 0px;
}

#logo {
    width: 260px;
    position: fixed;
    left: 10%;
    color: #F2EEE7;
}

#logo img {
    width: 100%;
}

/* ----------------------------------------------- */

nav {
    position: absolute;
    right: 5%;
    height: 100%;
    
}

nav ul {
    list-style-type: none;
    height: 100%;
    display: flex;    
}

nav li {
    display: flex;
    height: 100%;
    align-items: center;
    padding-left: 20px;
    padding-right: 20px;
}

nav li:hover {
    background-color: #97a28a;
}


/* ----------------------------------------------- */

main {
    position: relative;
    width: 80%;
    margin-top: 100px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 100px;
    max-width: 700px;
    min-width: 600px;
    display: flex;
    flex-direction: column;
}


#banner {
    position: relative;
    top: 60px;
    display: flex;
    width: 100%;
    height: 400px;
    justify-content: center;
    background-color: rgb(113, 125, 108);
}
    

/* ----------------------------------------------- */

#buttons {
    display: flex;
    justify-content: space-between;
}

/* ----------------------------------------------- */

#content {
    position: relative;
    margin-top: 17px;
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

/* ----------------------------------------------- */


#add_activity {
    background-color: white;
    width: 100%;
    position: relative;
    top: 20px;
    min-width: 600px;
    box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 0px 1px;
    margin-bottom: 30px;
}

#close_button {
    color: #c1c1c1;
    margin-top: auto;
    margin-bottom: auto;
    margin-right: 20px;
}

#close_button:hover {
    color: #727272;
    cursor: pointer;

}


#add_activity_title {
    width: 100%;
    position: relative;
    display: flex;
    justify-content: space-between;
    box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 0px 1px;
}

#add_activity_form {
    background-color: white;
    padding-right: 30px;
    padding-top: 30px;
    padding-bottom: 20px;
}


/* ----------------------------------------------- */
#activity_list {
    margin-bottom: 40px;
    background-color: white;
    box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 0px 1px;
}

#search {
    margin-bottom: 20px;
}

#activity{
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}

#edit_buttons {
    position: absolute;
    right: 0px;
    width: 42px;
    height: 80px;
    margin-top: -300px;
    margin-right: 10px;
    background-color: white;
    border-radius: 10px;
    text-align: center;
}

#delete_button {
    position: relative;
    color: #555555;

}

#edit_button {
    position: relative;
    top: 10px;
    left: 2px;
    color: #575757;
    flex-flow: flex-end;
}

#delete_button:hover {
    color: #0e0e0e;
    cursor: pointer;
}

#edit_button:hover {
    color: #0e0e0e;
    cursor: pointer;
}



#favorite_icon {
    position: absolute;
    top: -11px;
    right: 20px;
    opacity: 90%;
}

#activity_top {
    width: 100%;
    display: flex;
    justify-content: space-between;
    position: relative;
    align-self: flex-end;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 2px 0px;
    margin-top: 10px;
}

#activity_title {
    margin-left: 30px;
    margin-right: 30px;
    margin-bottom: 15px;
    margin-top: 10px;
}

#activity_buttons {
    width: 150px;
    margin-right: 10px;
}

.flex {
    display: flex;
}

#participants {
    text-align: right;
    margin-right: 5px;
    margin-top: 5px;
}

#img_container {
    position: relative;
    height: 300px;
    width: 100%;
    background-color: #dadada;
}

#img_container img {
    width: 100%;
    height: 300px;
    object-fit: cover;
    opacity: 90%;
}

#img_container img:hover {
    width: 100%;
    height: 300px;
    object-fit: cover;
}

#activity_description {
    width: 100%;
    height: 100%;
    position: relative;
    padding-left: 30px;
    padding-right: 30px;
    padding-top: 10px;
    padding-bottom: 20px;
}


/* ----------------------------------------------- */

* {
    box-sizing: border-box;
}

input {
    width: 200px;
}  

input[type=text], select, textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
    font-family: 'Raleway', sans-serif;
    font-size: 0.7em;
}


input[type=date], input[type=password], input[type=email] {
    width: 100%;
    padding: 12px;
    border: 1px solid #d2d2d2;
    border-radius: 4px;
    resize: vertical;
    font-family: 'Raleway', sans-serif;
    font-size: 0.7em;
}

input[type=submit] {
    height: 40px;
    width: 160px;
    background-color: #adb6a9;
    border: none;
    border-radius: 6px;
    padding: 6px;
    color: white;
    text-align: center;
    font-weight: 500;
    cursor: pointer;
    font-family: 'Raleway', sans-serif;
    font-size: 0.7em;
    float: right;
}

#buttons input[type=submit]{
    background-color: #7d7d7d;

}

input[type=submit]:hover {
    background-color: #767676;
}

button {
    height: 40px;
    width: 150px;
    font-size: 0.7em;
    background-color: #c28c62;
    border: none;
    border-radius: 6px;
    color: white;
    text-align: center;
    margin-left: 5px;
}

button:hover {
    background-color: #545454;
    cursor: pointer;
}


textarea {
    max-height: 300px;
    min-height: 300px;
}


select {
    background-color: #939393;
    height: 40px;
    border: none;
    border-radius: 6px;
    padding: 6px;
    color: white;
    text-align: center;
    font-weight: 500;
}


/* ----------------------------------------------- */

label {
    padding: 12px 12px 12px 0;
    display: inline-block;
    width: 10em;
    margin-right: 1em;
    text-align: right;
    padding-left: 20px;
    margin-bottom: 5px;
    font-size: 0.9em;
}

.col-25 {
    float: left;
    width: 25%;
    margin-top: 6px;
}
  
.col-75 {
    float: left;
    width: 75%;
    margin-top: 6px;
}
  
/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
}



/* ----------------------------------------------- */

/* If you use plain CSS your layout should at least adjust to window sizes between 1800px and 800px.
If you use bootstrap, your layout should be responsive adjusting also to phone sized displays, e.g. 375px.
Your layout should contain some kind of background or banner images.


 */
/* når width blir mindre enn 600px */
@media screen and (max-width: 600px) {
}


</style>