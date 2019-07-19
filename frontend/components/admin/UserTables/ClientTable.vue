<template>
    <div>
        <v-container grid-list-lg>
            <v-layout row wrap>
                <v-flex xs12 md9 class="no-message-input">
                    <v-text-field
                        v-model="search"
                        outlined
                        label="Pesquisar"
                        prepend-inner-icon="search"
                    ></v-text-field>
                </v-flex>
                <v-flex xs12 md3 class="no-message-input">
                    <v-select
                        v-model="filter"
                        :items="filters"
                        filled
                        rounded
                        return-object
                        label="Filtrar"
                    ></v-select>
                </v-flex>
            </v-layout>
        </v-container>
        <v-layout row wrap>
            <v-flex xs12>
                <v-data-table
                    :show-expand="isMobile"
                    :headers="headers"
                    :items="filteredList"
                    no-data-text="Sem resultados na pesquisa 😞"
                    no-results-text="Sem resultados na pesquisa 😞"
                    :page.sync="page"
                    :items-per-page="itemsPerPage"
                    hide-default-footer
                    class="elevation-1"
                    @page-count="pageCount = $event"
                >
                    <template v-slot:expanded-item="{ headers, item }">
                        <td :colspan="headers.length">
                            <v-container>
                                <v-layout
                                    row
                                    wrap
                                    justify-center
                                    text-xs-center
                                    align-center>
                                    <v-flex xs6 md3>
                                        <v-btn
                                            class="my-1 white--text"
                                            :outlined="!item.is_hacker"
                                            color="blue"
                                            @click="$emit('toggle-hacker', item)"
                                            v-text="`Hacker`"
                                        />
                                    </v-flex>
                                    <v-flex xs6 md3>
                                        <v-btn
                                            class="my-1 white--text"
                                            :outlined="!item.is_staff"
                                            color="blue"
                                            @click="$emit('toggle-staff', item)"
                                            v-text="`Staff`"
                                        />
                                    </v-flex>
                                    <v-flex xs6 md3>
                                        <v-btn
                                            class="my-1 white--text"
                                            :outlined="!item.is_admin"
                                            color="blue"
                                            @click="$emit('toggle-admin', item)"
                                            v-text="`Admin`"
                                        />
                                    </v-flex>
                                    <v-flex xs6 md3>
                                        <v-btn
                                            class="my-1 white--text"
                                            :outlined="!item.is_mentor"
                                            color="blue"
                                            @click="$emit('toggle-mentor', item)"
                                            v-text="`Mentor`"
                                        />
                                    </v-flex>
                                    <v-flex xs6 md3>
                                        <v-btn
                                            class="my-1 white--text"
                                            color="red"
                                            @click="$emit('delete-user', item)"
                                            v-text="`Apagar`"
                                        />
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </td>
                    </template>
                    <template v-slot:item.attributes="{ item }">
                        <v-icon v-if="item.is_verified" size="large" color="green">fas fa-check</v-icon>
                        <v-icon v-if="item.has_facebook" size="large" color="blue">fab fa-facebook</v-icon>
                        <v-icon v-if="item.has_github" size="large" color="black">fab fa-github</v-icon>
                        <v-icon v-if="item.has_google" size="large" color="red">fab fa-google</v-icon>
                    </template>
                    <template v-slot:item.unique_id="{ item }">
                        <kbd>{{ item.unique_id }}</kbd>
                    </template>
                    <template v-slot:item.full_name="{ item }">
                        <b>{{ item.full_name }}</b>
                    </template>
                    <template v-slot:item.state="{ item }">
                        <b>{{ item.state | mapState }}</b>
                    </template>
                    <template v-slot:item.action="{ item }">
                        <v-btn
                            class="my-1 px-2 white--text"
                            :outlined="!item.is_hacker"
                            color="blue"
                            @click="$emit('toggle-hacker', item)"
                            v-text="`Hacker`"
                        />
                        <v-btn
                            class="my-1 ml-1 px-2 white--text"
                            :outlined="!item.is_staff"
                            color="blue"
                            @click="$emit('toggle-staff', item)"
                            v-text="`Staff`"
                        />
                        <v-btn
                            class="my-1 ml-1 px-2 white--text"
                            :outlined="!item.is_admin"
                            color="blue"
                            @click="$emit('toggle-admin', item)"
                            v-text="`Admin`"
                        />
                        <br />
                        <v-btn
                            class="my-1 px-2 white--text"
                            :outlined="!item.is_mentor"
                            color="blue"
                            @click="$emit('toggle-mentor', item)"
                            v-text="`Mentor`"
                        />
                        <v-btn
                            class="my-1 ml-1 px-2 white--text"
                            color="red"
                            @click="$emit('delete-user', item)"
                            v-text="`Apagar`"
                        />
                    </template>
                    <template v-slot:footer>
                        <v-divider></v-divider>
                        <v-container grid-list-md pb-0>
                            <v-layout row wrap>
                                <v-flex xs12 md2>
                                    <v-select
                                        v-model="itemsPerPage"
                                        solo
                                        :items="itemsPerPageOptions"
                                        label="Por página"
                                    ></v-select>
                                </v-flex>
                                <v-flex xs12 md8 text-xs-center>
                                    <v-pagination
                                        v-model="page"
                                        prev-icon="mdi-menu-left"
                                        next-icon="mdi-menu-right"
                                        class="pagination"
                                        :total-visible="isMobile ? 5 : 7"
                                        :length="pageCount"
                                    ></v-pagination>
                                </v-flex>
                                <v-spacer></v-spacer>
                            </v-layout>
                        </v-container>
                    </template>
                </v-data-table>
            </v-flex>
        </v-layout>
    </div>
</template>
<script>
    export default {
        filters: {
            mapState: function(state) {
                const map = {
                    unverified: "Não verificado",
                    verified: "Verificado",
                    incomplete: "Incompleto",
                    submitted: "Submetido",
                    late: "Atrasado",
                    declined: "Recusado",
                    admitted: "Admitido",
                    waitlist: "Fila de espera",
                    withdraw: "Desistente",
                    confirmed: "Confirmado",
                    checkedin: "Checkin"
                }
                return map[state]
            }
        },
        props: {
            value: {
                type: Array,
                default: []
            }
        },
        data() {
            return {
                page: 1,
                pageCount: 0,
                itemsPerPage: 10,
                search: "",
                filter: null,
                itemsPerPageOptions: [
                    {
                        text: 10,
                        value: 10
                    },
                    {
                        text: 20,
                        value: 20
                    },
                    {
                        text: 50,
                        value: 50
                    }
                ],
                filters: [
                    {
                        text: "Todos",
                        value: "Todos",
                        filter: object => true
                    },
                    {
                        text: "Hacker",
                        value: "Hacker",
                        filter: object => object.is_hacker
                    },
                    {
                        text: "Admins",
                        value: "Admins",
                        filter: object => object.is_admin
                    },
                    {
                        text: "Staff",
                        value: "Staff",
                        filter: object => object.is_staff
                    },
                    {
                        text: "Mentor",
                        value: "Mentor",
                        filter: object => object.is_mentor
                    }
                ],
                mobileBreakpoint: 1264
            }
        },
        computed: {
            list: {
                get() {
                    return this.value
                },
                set(value) {
                    this.$emit("input", value)
                }
            },
            filteredList() {
                let list = [...this.list]
                if (this.search) {
                    list = list.filter(object => {
                        const byName =
                            object.full_name
                                .toLowerCase()
                                .indexOf(this.search.toLowerCase()) > -1
                        const byEmail =
                            object.email
                                .toLowerCase()
                                .indexOf(this.search.toLowerCase()) > -1
                        const byUID =
                            object.unique_id
                                .toLowerCase()
                                .indexOf(this.search.toLowerCase()) > -1
                        return byName || byEmail || byUID
                    })
                }
                if (this.filter) {
                    list = list.filter(object => this.filter.filter(object))
                }
                return list
            },
            isMobile() {
                return this.$vuetify.breakpoint.width < this.mobileBreakpoint
            },
            headers() {
                const headers = [
                    { text: "ID", value: "unique_id" },
                    { text: "Nome", value: "full_name" },
                    { text: "Email", value: "email" },
                    { text: "Estado", value: "state" },
                    { text: "Atributos", value: "attributes" }
                ]
                if (!this.isMobile) {
                    headers.push({
                        value: "action",
                        width: "256px",
                        class: "action-column"
                    })
                }
                return headers
            }
        }
    }
</script>
<style>
    .action-column {
        min-width: 256px;
    }
    @media only screen and (min-width: 600px) {
        .v-data-table td,
        .v-data-table th {
            padding-right: 5px;
        }
        .v-data-table td {
            height: 8em;
        }
    }
    @media only screen and (max-width: 400px) {
        .pagination {
            margin-left: -3em;
        }
    }
    .no-message-input {
        margin-bottom: -30px;
    }
</style>
