<template>
    <div>
        <br />
        <div class="small big-title">Lista de usuários</div>
        <UserTable
            v-model="list"
            :list-size-threshold="50"
            @toggle-hacker="toggleHacker"
            @toggle-staff="toggleStaff"
            @toggle-mentor="toggleMentor"
            @toggle-admin="toggleAdmin"
            @delete-user="deleteObject"
        />
    </div>
</template>
<script>
    import UserTable from "./UserTables/UserTable"
    export default {
        components: { UserTable },
        data() {
            return {
                list: []
            }
        },
        methods: {

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
