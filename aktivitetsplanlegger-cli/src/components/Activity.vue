
<template>

<div id="activity">
    <div id="row">
        <input type="submit" @click="get_activities_user_paticipation()" value="Påmeldte aktiviteter">
        <input type="submit" @click="get_activities_by_username()" value="Mine aktiviteter">
    </div>
    <br/>
    <div id="search">
        <input type="text" v-model="search" placeholder="Søk .."/>
    </div>
    <div id="row">
        <p style="color: white; display: inline">Sorter etter:</p><input type="submit" @click="orderByDate()" value="Førstkommende dato">
        <input type="submit" @click="get_activities" value="Nylig lagt til">
    </div>
    <br/>


    <div id="activities">
        <div id="activity_list" v-for="activity in filteredList" v-bind:key="activity">

            <div v-if="!edit || activity.activity_id != activityid">
                <div id="img_container">
                    <img :src="require('@/assets/uploads/' + activity.image)" />
                </div>

                <div id="activity_top">
                    <div id="edit_buttons" v-if="loggedInUsername == activity.username">
                        <div id="delete_button" @click="removeItem(activity)">
                            <i class="fa fa-times fa-2x"></i>
                        </div>
                        <div id="edit_button" @click="editItem(activity)">
                            <i class="fa fa-edit fa-2x"></i>
                        </div>
                    </div>

                    <div id="activity_title">
                        <h3> {{ activity.title }} </h3>
                        <h4> <i class="fa fa-calendar"></i> Dato: {{ activity.date.split('-')[2] }}. {{ this.getMonth(activity.date.split('-')[1]) }} {{ activity.date.split('-')[0]}} </h4>
                        <h4> <i class="fa fa-map-marker"></i> Sted: {{ activity.location }} </h4>
                        <h4> <i class="fa fa-user"></i> Lagt ut av: {{ activity.username }}</h4>
                        <h4> <i class="fa fa-users"></i>
                        <span v-if="activity.participants == 0">Ingen deltakere enda</span>
                        <span v-if="activity.participants == 1">{{ activity.participants }} deltaker</span>
                        <span v-if="activity.participants > 1">{{ activity.participants }} deltakere</span></h4>
                        <h4>{{ activity.participants }}</h4>
                    </div>

                    <div id="activity_buttons">
                        <div class="flex">
                            <input type="submit" v-if="loggedInUsername != activity.username" @click.once="signMeUp(activity)" value="Meld meg på">
                        </div>
                    </div>
                </div>

                <div id="activity_description" class="show-white-space">
                    <p>{{ activity.description }}</p>
                </div> 
            </div>

            
            <div id="edit_activity" v-if="edit && activity.activity_id == activityid">
                <form method="PUT" v-on:submit="submitEdit(activity)">

                    <div id="img_container">
                        <img :src="require('@/assets/uploads/' + activity.image)" />
                    </div>

                    <div id="activity_top">
                        <div id="edit_buttons" v-if="loggedInUsername == activity.username">
                            <div id="delete_button" @click="removeItem(activity)">
                                <i class="fa fa-times fa-2x"></i>
                            </div>
                            <div id="edit_button" @click="editItem(activity)">
                                <i class="fa fa-edit fa-2x"></i>
                            </div>
                        </div>

                        <div id="activity_title">
                            <input type="text" id="title" name="title" placeholder="Tittel på aktivitet" required v-model="title">
                            <input type="date" id="date" name="date" style="max-height: 50px; min-height: 50px;"  :min="dateToday" max="2030-01-01" required v-model="date">
                            <input type="text" id="location" name="location" placeholder="Sted" required v-model="location">

                            <h4> <i class="fa fa-user"></i> Lagt ut av: <strong>{{ activity.username }}</strong></h4>
                        </div>

                        <div id="activity_buttons">
                            <div class="flex">
                                <input type="submit" @click.once="signMeUp()" value="Meld meg på">
                            </div>
                        </div>
                    </div>

                    <div id="activity_description" class="show-white-space">
                        <textarea v-model="description"></textarea>
                        <input type="submit" value="Save">
                        <button v-on:click="cancelEdit">Cancel</button>
                    </div>

                </form>
            </div>


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
            images: [],
            image: null,
            activity_image: null,
            userid: null,
            activity: null,
            search: "",       
            edit: false,
            activityid: null,
            activity_description: null,
            description: null,
            loggedInUsername: null,
            dateToday: null,
            acitivty_participation: null,
        }
    },
    methods: {
        async get_activities() {
            // get activites
            let response = await fetch(baseURL + "activities_get");
            if (response.status != 200){
                console.log("Failed to get activities")
                return ""
            }
            let result = await response.json();
            this.activities = result;
        },
        async orderByDate() {
            // get activites
            let response = await fetch(baseURL + "activities_get_date");
            if (response.status != 200){
                console.log("Failed to get activities")
                return ""
            }
            let result = await response.json();
            this.activities = result;
        },
        async get_activities_by_username() {
            // get activites created by username
            let username = this.loggedInUsername
            console.log(username)

            let response = await fetch(baseURL + "activities_get_by_username/" + username);
            if (response.status != 200){
                console.log("Failed to get activities by username")
                return ""
            }
            let result = await response.json();
            console.log(result)
            if (result == null) {
                alert("Du har ikke lagt til noen aktiviteter enda.")
            } else {
                this.activities = result;
            }
            //this.activities = result;
        },
        async get_activities_user_paticipation() {
            // get activites created by username
            let username = this.loggedInUsername

            let response = await fetch(baseURL + "activities_get_user_participation/" + username);
            if (response.status != 200){
                console.log("Failed to get activities by participation")
                return ""
            }
            let result = await response.json();
            console.log(result)
            if (result == null) {
                alert("Du er ikke påmeldt noen aktiviteter enda.")
            } else {
                this.activities_participation = result;
                console.log(result)
            }
        },
        // remove activity
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
        getMonth(month) {
            const months = ["januar","februar","mars","april","mai","juni","juli","august","september","oktober","november","desember"];
            let monthName = months[month-1]
            return monthName
        },
        // edit activity
        editItem(activity) {
            this.activityid = activity.activity_id
            this.edit = true
            this.title = activity.title
            this.date = activity.date
            this.location = activity.location
            this.description = activity.description
        },
        // hides the edit-field
        cancelEdit() {
            this.edit = false;
        },
        // submits the edited post and fetches the updated values for the post
        async submitEdit(activity) {
            event.preventDefault();

            let activity_id = activity.activity_id
            let formData = new FormData();

            formData.append("title", this.title)
            formData.append("date", this.date)
            formData.append("location", this.location)
            formData.append("description", this.description)                

            await fetch(baseURL + "set_activity/" + activity_id, {
                credentials: 'include',
                contentType: "text/plain; charset=utf-8",
                method: "PUT",
                body: formData,
            });
            this.edit = false;
            this.get_activities()
        },
        async signMeUp(activity) {
            let activity_id = activity.activity_id
            let username = sessionStorage.getItem("username")
            console.log(username)
            console.log(activity_id)
            
            await fetch(baseURL + 'participate/' + activity_id, {
                credentials: 'include',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"activity_id": activity_id, "username": username})
            });
            this.$router.go()
        }
    },
    async created() {
        // get activites (without reloading the page)
        this.get_activities()

        // Check if the user is logged in
        if (sessionStorage["username"]) {
            this.loggedInUsername = sessionStorage.getItem("username")
        }

        const today = new Date()
        const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()
        this.dateToday = date

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