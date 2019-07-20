<template>
    <div id="admin" class="page">
        <div class="divided big-title">Admin</div>
        <v-container>
            <v-layout row wrap>
                <v-spacer />
                <v-flex xs12>
                    <v-layout row wrap>
                        <v-tabs
                            v-model="tab"
                            background-color="transparent"
                            grow
                            show-arrows
                            center-active
                            centered>
                            <v-tabs-slider></v-tabs-slider>
                            <v-tab v-for="t in tabs" :key="t.name" :href="`#` + t.name">
                                {{ t.name }}
                            </v-tab>
                        </v-tabs>
                    </v-layout>
                    <v-layout
                        row
                        wrap
                        mt-5
                        justify-center>
                        <v-flex xs12>
                            <v-tabs-items v-model="tab" continuous>
                                <v-tab-item v-for="t in tabs" :key="t.name" :value="t.name">
                                    <component :is="t.component" v-if="t.component" />
                                </v-tab-item>
                            </v-tabs-items>
                        </v-flex>
                    </v-layout>
                </v-flex>
                <v-spacer />
            </v-layout>
        </v-container>
    </div>
</template>

<script>
    import Users from "~/components/admin/Users.vue"
    import CreateUsers from "~/components/admin/CreateUsers.vue"
    // import Company from "./sections/company.vue"
    // import Settings from "./sections/settings.vue"
    import Announcements from "~/components/admin/Announcements.vue"

    export default {
        head() {
            return { title: "Godmode" }
        },
        components: {
            Users,
            CreateUsers,
            // Company,
            // Settings,
            Announcements,
            // LatestAnnouncement
        },
        data() {
            return {
                tab: null,
                tabs: [
                    {
                        name: "Listar",
                        icon: "fas fa-robot",
                        component: Users
                    },
                    {
                        name: "Criar",
                        icon: "fas fa-users",
                        component: CreateUsers
                    },
                    {
                        name: "Empresas",
                        icon: "fas fa-tags",
                        component: null
                    },
                    {
                        name: "Anúncios",
                        icon: "fas fa-folder",
                        component: Announcements
                    },
                    {
                        name: "Configurações",
                        icon: "fas fa-folder",
                        component: null
                    }
                ]
            }
        },
        permissions: args => {
            return args.app.$perms.admin(args)
        }
    }
</script>
<style scoped>
    .v-tabs-items {
        background-color: transparent
    }
</style>
