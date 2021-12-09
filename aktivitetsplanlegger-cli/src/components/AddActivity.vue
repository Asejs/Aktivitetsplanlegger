
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

                <div class="row">
                    <div class="col-25">
                        <label for="fileToUpload">Velg et bilde:</label>
                    </div>
                    <div class="col-75">
                        <input name="file" type="file" @change="onFileSelected" ref="uploadedFile" accept=".jpg, .JPG, .jpeg, .JPEG, .png, .PNG, .webp">
                        <!--<button @click="onUpload">Upload</button>-->
                    </div>
                </div>


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
              imgFile: null,
          }
      },
      /*watch: {
          '$route': function() {
              this.reLoadPosts();
            }
        },*/
      
      methods: {
        /*reLoadPosts: async function() {
            await getPostsReload(this, this.$route.path, this.$route.params.id);
        },*/

        // imgFile blir satt til valgt bilde
        onFileSelected(event) {
            console.log(event)
            this.imgFile = event.target.files[0]
            console.log(this.imgFile)
        },

        async publishPost() {
            event.preventDefault();
            //this.imgFile = this.$refs.uploadedFile.file;


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
            console.log(response)

            console.log("MY FILE:", this.imgFile)
            console.log("NAME:", this.imgFile.name)

            //post request
            //uses formdata since you can't convert images to json...
            let formData = new FormData();

            formData.append("file", this.imgFile, this.imgFile.name);
            console.log("FORMDATA:", formData)

            let imgresponse = await fetch(baseURL + "upload_image", {
                credentials: 'include',
                method: 'POST',
                body: formData,
            });
            console.log("IMGRESPONSE", imgresponse)
            await this.$router.push('/activities');
        },
    }
}

</script>
