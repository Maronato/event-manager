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
                    <v-list-item-avatar width="100%" height="100%">
                        <img src="~/static/img/logo.svg" />
                    </v-list-item-avatar>
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
                    <v-flex xs12 lg8>
                        <LatestAnnouncement />
                    </v-flex>
                    <v-spacer />
                </v-layout>
                <v-layout row wrap>
                    <v-spacer />
                    <v-flex xs12 lg8>
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
                if (this.$auth.user.is_admin) {
                    items.push({
                        icon: "fas fa-users-cog",
                        title: "Admin",
                        to: "/admin/"
                    })
                }
                return items
            }
        },
        beforeMount() {
            // API Fetch
            this.fetchSettings()
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

            // API Fetch
            fetchSettings() {
                this.$auth.request("/api/settings/").then(settings => {
                    this.$store.commit("settings/set", settings)
                })
            },
            fetchAnnouncements() {
                this.$auth.request("/api/announcements/").then(announcements => {
                    this.$store.commit("announcements/update", announcements)
                })
            },

            // Subs
            selfSub() {
                this.$selfWS({
                    signal: "update",
                    debug: false,
                    callback: user => {
                        this.$auth.setUset(user)
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
                        this.$store.commit("announcements/push", announcement)
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
