
<template>
<div id="container">
    <div id="buttons">
        <button @click="isVisible = true">+ Legg til ny aktivitet</button>
    </div>

    <div id="add_activity" v-show="isVisible">
        <div id="add_activity_title">
            <h2>Legg til ny aktivitet</h2>
            <div id="close_button" @click="isVisible = false">
                <i class="fa fa-times fa-2x"></i>
            </div>
        </div>

        <div id="add_activity_form">
            <form @submit.prevent="handleSubmit">
                <div class="row">
                    <div class="col-25">
                    <label for="title">Tittel:</label>
                    </div>
                    <div class="col-75">
                    <input type="text" id="title" name="title" placeholder="Tittel på aktivitet" required v-model="title">
                    </div>
                </div>
                <div class="row">
                    <div class="col-25">
                    <label for="date">Dato:</label>
                    </div>
                    <div class="col-75">
                    <input type="date" id="date" name="date" style="max-height: 40px" min="2021-06-04" max="2030-01-01" required v-model="date">
                    </div>
                </div>
                <div class="row">
                    <div class="col-25">
                    <label for="location">Sted:</label>
                    </div>
                    <div class="col-75">
                    <input type="text" id="location" name="location" placeholder="Sted" required v-model="location">
                    </div>
                </div>
                <div class="row">
                    <div class="col-25">
                    <label for="description">Beskrivelse:</label>
                    </div>
                    <div class="col-75">
                    <textarea id="description" name="description" placeholder="Beskrivelse av aktivitet" style="height:300px" required v-model="description"></textarea>
                    </div>
                </div>


                <!--<form action="upload.php" method="post" enctype="multipart/form-data">
                <div class="row">
                    <div class="col-25">
                        <label for="fileToUpload">Velg et bilde:</label>
                    </div>
                    <div class="col-75">
                        <input type="file" @change="onFileSelected" name="fileToUpload" id="fileToUpload">
                        <button @click="onUpload">Upload</button>
                    </div>
                    </div>
                    </form>-->


                <div class="row">
                    <br/><input type="submit" value="Legg til aktivitet">
                    <!-- <input type="submit" value="Upload Image" name="submit"> -->
                </div>
            </form>
        </div>
        </div>
</div>

</template>


<script>
let baseURL = "http://127.0.0.1:5000/";

  export default {
      name: 'AddActivity',
      props: [''],
      data () {
          return {
              //selectedFile: null
              title: '',
              date: '',
              location: '',
              description: '',
              isVisible: false,
          }
      },
      
      methods: {
          async handleSubmit() {
            let username = sessionStorage.getItem("username")
            console.log(username)

            let response = await fetch(baseURL + "add_activity_post", {
                credentials: 'include',
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: username, title: this.title, date: this.date, location: this.location, description: this.description })
            });
            if (response.status == 404){
                console.log("No user logged in!")
                return
            }
            else {
                console.log("Lagt til aktivitiet: ", this.title)
                alert("Lagt til aktivitet.");
            }
            window.location.reload(true)
        },
      }
      /*
      methods: {
          onFileSelected(event) {
              console.log(event)
              this.selectedFile = event.target.files[0]
          },
          onUpload() {
              post request
              const fd = new FormData()
              fd.append('image', this.selectedFile, this.selectedFile)

              }
            */
}

</script>
