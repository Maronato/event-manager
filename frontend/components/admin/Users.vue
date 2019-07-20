<template>
    <div>
        <br />
        <div class="small big-title">Lista de usuários</div>
        <component
            :is="tableComponent"
            v-model="list"
            :initial-list-size="initialListSize"
            @toggle-hacker="toggleHacker"
            @toggle-staff="toggleStaff"
            @toggle-mentor="toggleMentor"
            @toggle-admin="toggleAdmin"
            @delete-user="deleteObject"
        />
    </div>
</template>
<script>
    import ClientTable from "./UserTables/ClientTable"
    import ServerTable from "./UserTables/ServerTable"
    export default {
        components: { ClientTable, ServerTable },
        data() {
            return {
                list: [],
                initialListSize: 0,
                listSizeThreshold: 250
            }
        },
        computed: {
            tableComponent() {
                if (this.belowThreshold) {
                    return ClientTable
                }
                return ServerTable
            },
            belowThreshold() {
                return this.initialListSize <= this.listSizeThreshold
            }
        },
        mounted() {
            this.fetchList()
            this.listSub()
        },
        methods: {
            fetchList() {
                this.$auth
                    .request("/api/profiles/all/count/")
                    .then(response => {
                        this.initialListSize = response.count
                        let url = "/api/profiles/all/"
                        if (!this.belowThreshold) {
                            url += "?limit=" + 50
                        }
                        return this.$auth.request(url).then(response => {
                            if (this.belowThreshold) {
                                this.list = response
                            } else {
                                this.list = response.results
                            }
                        })
                    })
                    .catch(() => {
                        this.$toast(
                            "Opa!",
                            "Não conseguimos carregar a lista de usuários",
                            "error"
                        )
                    })
            },
            pushToList(object) {
                this.$eventBus.$emit('add-user')
                if (this.belowThreshold) {
                    this.list.push(object)
                }
            },
            updateOnList(object) {
                this.$eventBus.$emit('update-user')
                const idx = this.list.findIndex(
                    obj => obj.unique_id === object.unique_id
                )
                if (idx >= 0) {
                    this.list.splice(idx, 1, object)
                }
            },
            removeFromList(object) {
                this.$eventBus.$emit('remove-user')
                const idx = this.list.findIndex(
                    obj => obj.unique_id === object.unique_id
                )
                if (idx >= 0) {
                    this.list.splice(idx, 1)
                }
            },
            listSub() {
                this.$modelWS({
                    app: "user_profile",
                    model: "Profile",
                    signal: "create",
                    callback: this.pushToList
                })
                this.$modelWS({
                    app: "user_profile",
                    model: "Profile",
                    signal: "update",
                    callback: this.updateOnList
                })
                this.$modelWS({
                    app: "user_profile",
                    model: "Profile",
                    signal: "delete",
                    callback: this.removeFromList
                })
            },

            // Admin-Specific actions
            deleteObject(object) {
                this.$swal({
                    title: "Tem certeza?",
                    text: "Essa ação é irreversível!",
                    icon: "warning",
                    buttons: ["Cancelar", "Apagar"],
                    dangerMode: true
                }).then(response => {
                    if (response) {
                        this.$auth
                            .request({
                                method: "delete",
                                url: "/api/users/delete/" + object.unique_id + "/"
                            })
                            .then(() => {
                                this.$toast("Aviso", "Usuário removido", "info")
                                this.removeFromList(object)
                            })
                            .catch(() => {
                                this.$toast(
                                    "Opa!",
                                    "Algo de errado aconteceu 😞",
                                    "error"
                                )
                            })
                    }
                })
            },
            toggleHacker(object) {
                if (object.is_hacker && object.state !== "incomplete") {
                    this.$swal({
                        title: "Tem certeza?",
                        text:
                            "Esse usuário perderá seu formulário de aplicação e qualquer outra propriedade associada ao seu status de hacker!",
                        icon: "warning",
                        buttons: ["Cancelar", "Alterar"],
                        dangerMode: true
                    }).then(response => {
                        if (response) {
                            this.$auth
                                .request({
                                    method: "post",
                                    url: "/api/hackers/toggle/",
                                    data: {
                                        unique_id: object.unique_id
                                    }
                                })
                                .then(() => {
                                    this.$toast("Aviso", "Usuário alterado", "info")
                                })
                                .catch(() => {
                                    this.$toast(
                                        "Opa!",
                                        "Algo de errado aconteceu 😞",
                                        "error"
                                    )
                                })
                        }
                    })
                } else {
                    this.$auth
                        .request({
                            method: "post",
                            url: "/api/hackers/toggle/",
                            data: {
                                unique_id: object.unique_id
                            }
                        })
                        .then(() => {
                            this.$toast("Aviso", "Usuário alterado", "info")
                        })
                        .catch(() => {
                            this.$toast(
                                "Opa!",
                                "Algo de errado aconteceu 😞",
                                "error"
                            )
                        })
                }
            },
            toggleStaff(object) {
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/staff/toggle/",
                        data: {
                            unique_id: object.unique_id
                        }
                    })
                    .then(() => {
                        this.$toast("Aviso", "Usuário alterado", "info")
                    })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu 😞", "error")
                    })
            },
            toggleMentor(object) {
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/mentors/toggle/",
                        data: {
                            unique_id: object.unique_id
                        }
                    })
                    .then(() => {
                        this.$toast("Aviso", "Usuário alterado", "info")
                    })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu 😞", "error")
                    })
            },
            toggleAdmin(object) {
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/admin/toggle/",
                        data: {
                            unique_id: object.unique_id
                        }
                    })
                    .then(() => {
                        this.$toast("Aviso", "Usuário alterado", "info")
                    })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu 😞", "error")
                    })
            }
        }
    }
</script>
