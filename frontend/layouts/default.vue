<template>
    <base-layout>
        <v-navigation-drawer
            id="sidebar"
            v-model="showNav"
            class="elevation-8"
            :class="{open: showNav}"
            fixed
            dark
            app>
            <v-list>
                <v-list-item href="/" :ripple="false">
                    <v-list-item-avatar width="100%" height="100%">
                        <img src="~/static/img/logo.svg">
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
            <img v-show="!showNav" src="~/static/img/logo.svg" />
            <span v-show="showNav" class="close">&#x2715;</span>
        </div>
        <v-content>
            <v-container>
                <nuxt />
            </v-container>
        </v-content>
    </base-layout>
</template>

<script>
    import baseLayout from "./base"
    export default {
        components: { baseLayout },
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
        mounted() {
            this.$selfWS({signal: 'update', debug: true, callback: () => {
                console.log("deu bom")
            }})
        },
        methods: {
            logout() {
                this.$auth.logout()
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
