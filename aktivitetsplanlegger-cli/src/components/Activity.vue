
<template>

<div id="activity">
    <div id="search">
        <input type="text" v-model="search" placeholder="Søk .."/>
    </div>

    <div id="activity_list" v-for="activity in filteredList" v-bind:key="activity">
        <div id="img_container">
            <img src="@/assets/default.png"/>
        </div>


        <div id="activity_top">
        <!--
        <div id="favorite_icon">
            <img src="@/assets/bookmark.png" style="width:50px"/>
        </div>
        -->
            <div id="edit_buttons" v-if="loggedInUsername == activity.username">
                <div id="delete_button" @click="removeItem(activity)">
                    <i class="fa fa-times fa-2x"></i>
                </div>
                <div id="edit_button" @click="edit">
                    <i class="fa fa-edit fa-2x"></i>
                </div>
            </div>

            <div id="activity_title">
                <h3> {{ activity.title }} </h3>
                <h4> <i class="fa fa-calendar"></i> Dato: {{ activity.date }} </h4>
                <h4> <i class="fa fa-map-marker"></i> Sted: {{ activity.location }} </h4>
                <h4> <i class="fa fa-user"></i> Lagt ut av: <strong>{{ activity.username }}</strong></h4>
            </div>

            <div id="activity_buttons">
                <div class="flex">
                    <input type="submit" @click.once="signMeUp" value="Meld meg på">
                </div>
                
                <div id="participants">
                    <h4> <i class="fa fa-users"></i>Deltakere: 0/20</h4>
                </div>
            </div>
        </div>

        <div id="activity_description">
            <p>{{ activity.description }}</p>
        </div>    
    </div>
</div>

</template>


<script>
    let baseURL = "http://127.0.0.1:5000/";

    export default {
        name: 'Activity',
        data() {
            return {
                activities: [],
                userid: "",
                activity: "",
                search: "",       
                loggedInUsername: ""   
                /*sortBy: "name",
                sortDirection: "asc"*/
            }
        },
        methods: {
            // sign up button
            signMeUp() {
                console.log("signup")

            },
            async get_activities() {
                // Get activites
                let response = await fetch(baseURL + "activities_get");
                if (response.status != 200){
                    console.log("Failed to get activities");
                    return ""
                }
                let result = await response.json();
                this.activities = result;
            },
            // remove selected activity
            async removeItem(activity) {
                var c = confirm("Are you sure you want to delete this entry?");
                if (c) {
                    let activity_id = activity.activity_id
                    let response = await fetch(baseURL + "del_activities/" + activity_id, {
                        credentials: 'include',
                        method: 'DELETE',
                        headers: {
                            "Content-Type": "application/json",
                        },
                    });
                    if (response.status != 200){
                        console.log("error")
                        return 'error'
                    }
                }
                this.get_activities()
            },

            // edit selected activity
            edit() {
                console.log("edit")
            }
            // sort the activities
            /*sort(activity) {
                if(activity === this.sortBy) {
                    this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
                }
                this.sortBy = s;
            },*/
        },
        async created() {
            this.get_activities()
            // Check if the user is logged in
            if (sessionStorage["username"]) {
                this.loggedInUsername = sessionStorage.getItem("username")
            }
        },
        computed: {
            // The search filter searches through activity title, location, username and description
            filteredList() {
            return this.activities.filter((activity) => {
                return activity.title.toLowerCase().includes(this.search.toLowerCase()) ||
                activity.location.toLowerCase().includes(this.search.toLowerCase()) ||
                activity.username.toLowerCase().includes(this.search.toLowerCase()) ||
                activity.description.toLowerCase().includes(this.search.toLowerCase())
            })
        },
    }
}
</script>