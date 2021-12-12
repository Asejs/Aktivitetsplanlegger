
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
            <p class="error" v-if="error">{{ error }}</p>

            <form id="newactivity" method="POST" enctype="multipart/form-data" v-on:submit="publishPost">
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
                    <input type="date" id="date" name="date" style="max-height: 50px; min-height: 50px;" :min="dateToday" max="2030-01-01" required v-model="date">
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

                <div class="row">
                    <div class="col-25">
                        <label for="fileToUpload">Last opp et bilde:</label>
                    </div>
                    <div class="col-75">
                        <input name="file" type="file" @change="onFileSelected" ref="uploadedFile" accept=".jpg, .JPG, .jpeg, .JPEG, .png, .PNG, .webp">
                    </div>
                </div>

                <div class="row">
                    <div class="col-25">
                        <label for="fileToUpload">Velg bilde:</label>
                    </div>
                    <div class="col-75">
                        <div class="radio">
                            <input type="radio" name="choose_image" id="myRadio1" value="bilde1.jpeg" v-model="radio"  @click="radio = null">
                            <label for="myRadio1"><img src="@/assets/bilde1.jpeg"/></label>
            
                            <input type="radio" name="choose_image" id="myRadio2" value="bilde2.jpeg" v-model="radio"  @click="radio = null">
                            <label for="myRadio2"><img src="@/assets/bilde2.jpeg"/></label>
                
                            <input type="radio" name="choose_image" id="myRadio3" value="bilde3.jpeg" v-model="radio" @click="radio = null">
                            <label for="myRadio3"><img src="@/assets/bilde3.jpeg"/></label>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <br/><input type="submit" value="Legg til aktivitet">
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
      data () {
          return {
              title: null,
              date: null,
              location: null,
              description: null,
              isVisible: false,
              imgFile: null,
              radio: null,
              error: null,
              dateToday: null,
          }
      },
      methods: {
        // imgFile blir satt til valgt bilde
        onFileSelected(event) {
            this.imgFile = event.target.files[0]
            return
        },
        async publishPost() {
            event.preventDefault();

            if  (this.imgFile == null && this.radio == null) {
                this.error = "Du må velge et bilde";
                return                
            }

            let username = sessionStorage.getItem("username")

            // post request
            // uses formdata since you can't convert images to json...
            let formData = new FormData();

            formData.append("username", username)
            formData.append("title", this.title)
            formData.append("date", this.date)
            formData.append("location", this.location)
            formData.append("description", this.description)

            if (this.radio != null) {
                formData.append("radio", this.radio)
            }
            else {
                formData.append("file", this.imgFile, this.imgFile.name)
            }

            await fetch(baseURL + "upload_image", {
                credentials: 'include',
                contentType: "text/plain; charset=utf-8",
                method: 'POST',
                body: formData,
            });

            this.$router.go()
        },
    },
    created() {
        const today = new Date()
        const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()
        this.dateToday = date
    }
}

</script>
