<template>
    <div id="team" class="page">
        <div class="divided title">
            Equipe
        </div>

        <div class="ui stackable centered page grid">
            <LatestAnnouncement />
            <div class="row">
                <div class="column">
                    <template v-if="current_team == null">
                        <Create
                        @teamCreated="teamCreated($event)"
                        :team_context="team"/>
                    </template>
                    <template v-else>
                        <TeamView
                        @receiveUpdates='$event ? subscribe() : unsubscribe()'
                        @leaveTeam="current_team = null"
                        :team_context="team"
                        :team="current_team" />
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "project/js/axios_csrf";
import toast from "project/js/notifications";
import LatestAnnouncement from "announcement/components/latest_announcement.vue";
import Create from "team/components/create/create.vue";
import TeamView from "team/components/view/view.vue";

import TeamSubscription from "team/js/team_sub.js";

export default {
    props: ["team_context", "user_context", "settings_context"],
    components: { LatestAnnouncement, Create, TeamView },
    data() {
        return {
            team: this.team_context,
            user: this.user_context,
            settings: this.settings_context,
            current_team: null,

            updateconnection: null,
            deleteconnection: null,
            receiveUpdates: true
        }
    },
    methods: {
        fetchTeamData() {
            axios.get(
                this.team.api.current_team
                ).then(data => {
                    this.current_team = data.data
                    this.updateSubscription()
                }).catch(error => {
                    if (error.response.status != 403) {
                        console.error(error);
                        toast("Opa!", "Algo de errado aconteceu :(", "error")
                    }
                })
        },
        teamCreated(team) {
            this.current_team = team
            this.updateSubscription()
        },
        unsubscribe() {
            if (this.updateconnection) {
                this.updateconnection.unsubscribe()
                this.updateconnection.disconnect()
            }
            if (this.deleteconnection) {
                this.deleteconnection.unsubscribe()
                this.deleteconnection.disconnect()
            }
        },
        subscribe() {
            this.updateconnection = new TeamSubscription(this.current_team.id, "update")
            this.deleteconnection = new TeamSubscription(this.current_team.id, "delete")

            this.updateconnection.connect();
            this.deleteconnection.connect();
            this.updateconnection.subscribe(team => {
                this.current_team = team
            });
            this.deleteconnection.subscribe(() => {
                this.current_team = null
            });
        },
        updateSubscription() {
            this.unsubscribe()
            this.subscribe()
        }
    },
    mounted() {
        this.fetchTeamData()
    }
};
</script>

