import Vue from "vue";
import Team from "team/components/team.vue";
import SuiVue from "semantic-ui-vue";

Vue.use(SuiVue);

var base = new Vue({
    data() {
        return {
            team_context: team_context,
            user_context: user_context,
            settings_context: settings_context,
        };
    },
    el: "#team-app",
    template: '<Team v-bind:team_context="team_context" v-bind:user_context="user_context" :settings_context="settings_context" />',
    components: { Team }
});
