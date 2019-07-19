<template>
    <base-layout>
        <v-navigation-drawer
            id="sidebar"
            v-model="showNav"
            class="elevation-8"
            :class="{open: showNav}"
            fixed
            dark
            app
        >
            <v-list>
                <v-list-item href="/" :ripple="false">
                    <v-container>
                        <v-list-item-avatar width="100%" height="100%" tile>
                            <img src="~/static/img/logo.svg" />
                        </v-list-item-avatar>
                    </v-container>
                </v-list-item>
                <v-list-item
                    v-for="(item, i) in items"
                    :key="i"
                    :to="item.to"
                    router
                    exact>
                    <v-list-item-action>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title v-text="item.title" />
                    </v-list-item-content>
                </v-list-item>
                <v-list-item @click="logout()">
                    <v-list-item-action>
                        <v-icon>fas fa-sign-out-alt</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Logout</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <div v-show="isMobile" class="tab" @click="drawer = !drawer">
            <img src="~/static/img/logo.svg" />
        </div>
        <v-content>
            <v-container>
                <v-layout row wrap>
                    <v-spacer />
                    <v-flex xs12 lg8 xl6>
                        <LatestAnnouncement />
                    </v-flex>
                    <v-spacer />
                </v-layout>
                <v-layout row wrap>
                    <v-spacer />
                    <v-flex xs12 md10 xl8>
                        <nuxt />
                    </v-flex>
                    <v-spacer />
                </v-layout>
            </v-container>
        </v-content>
    </base-layout>
</template>

<script>
    import baseLayout from "./base"
    import LatestAnnouncement from "~/components/announcements/LatestAnnouncement"
    export default {
        components: { baseLayout, LatestAnnouncement },
        data() {
            return {
                drawer: false
            }
        },
        computed: {
            isMobile() {
                return this.$vuetify.breakpoint.width <= 1264
            },
            showNav: {
                get() {
                    return this.drawer || !this.isMobile
                },
                set(value) {
                    this.drawer = value
                }
            },
            items() {
                const items = [
                    {
                        icon: "fas fa-tachometer-alt",
                        title: "Dashboard",
                        to: "/"
                    }
                ]
                if (
                    this.$perms.application({
                        app: this,
                        user: this.$auth.user,
                        settings: this.$store.state.settings.settings
                    })
                ) {
                    items.push({
                        icon: "fas fa-scroll",
                        title: "Aplicação",
                        to: "/application/"
                    })
                }
                if (this.$perms.admin({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-users-cog",
                        title: "Admin",
                        to: "/admin/"
                    })
                }
                if (this.$perms.staff({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-hands-helping",
                        title: "Staff",
                        to: "/staff/"
                    })
                }
                if (this.$perms.company({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-building",
                        title: "Empresa",
                        to: "/company/"
                    })
                }
                if (this.$perms.team({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-users",
                        title: "Equipe",
                        to: "/team/"
                    })
                }
                if (this.$perms.schedule({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-calendar-day",
                        title: "Eventos",
                        to: "/schedule/"
                    })
                }
                if (this.$perms.helper({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-life-ring",
                        title: "Helper",
                        to: "/helper/"
                    })
                }
                if (this.$perms.stats({ user: this.$auth.user })) {
                    items.push({
                        icon: "fas fa-chart-bar",
                        title: "Stats",
                        to: "/stats/"
                    })
                }
                return items
            }
        },
        beforeMount() {
            // API Fetch
            this.fetchAnnouncements()
            // WS Subscribe
            this.selfSub()
            this.settingsSub()
            this.announcementsSub()
        },
        methods: {
            logout() {
                this.$auth.logout()
            },
            fetchAnnouncements() {
                this.$auth.request("/api/announcements/").then(announcements => {
                    this.$store.dispatch("announcements/update", announcements)
                })
            },

            // Subs
            selfSub() {
                this.$selfWS({
                    signal: "update",
                    debug: false,
                    callback: user => {
                        this.$auth.setUser(user)
                    }
                })
            },
            settingsSub() {
                this.$modelWS({
                    app: "settings",
                    model: "Settings",
                    signal: "update",
                    debug: false,
                    callback: settings => {
                        this.$store.commit("settings/set", settings)
                    }
                })
            },
            announcementsSub() {
                this.$modelWS({
                    app: "announcement",
                    model: "Announcement",
                    signal: "create",
                    debug: false,
                    callback: announcement => {
                        this.$store.dispatch("announcements/push", announcement)
                    }
                })
                this.$modelWS({
                    app: "announcement",
                    model: "Announcement",
                    signal: "delete",
                    debug: false,
                    callback: () => {
                        this.fetchAnnouncements()
                    }
                })
            }
        }
    }
</script>
<style lang="scss">
    #sidebar.open + .tab {
        margin-left: -10px;
    }
    .v-navigation-drawer__content a {
        color: white;
    }
</stylelang>
