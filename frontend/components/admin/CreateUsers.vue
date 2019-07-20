<template>
    <div>
        <div class="small big-title">Criar usuários</div>
        <v-divider class="my-3" />
        <br />
        <v-layout row wrap>
            <v-flex xs12 md6>
                <h3 class="font-weight-light headline">Criar</h3>
                <br />
                <label>
                    CSV, formato:
                    <code>Primeiro nome, Sobrenome, Email</code>
                </label>
                <v-textarea
                    v-model="csv"
                    outlined
                    class="mt-2"
                    :placeholder="`Fulano, Da Silva, fulano@gmail.com
Maria, Souza, maria@outlook.com
João, Pedro, joao@pedro.com`"
                ></v-textarea>
                <v-btn
                    color="blue"
                    class="white--text ma-2"
                    tile
                    @click="checkFormat()"
                >Checar formato</v-btn>
                <v-btn
                    :loading="createLoading"
                    :disabled="!formatIsValid"
                    color="green"
                    class="white--text ma-2"
                    tile
                    @click="createUsers()"
                >Criar usuários</v-btn>
                <v-checkbox
                    v-model="sendEmails"
                    class="mt-2"
                    :disabled="!formatIsValid"
                    label="Enviar emails de verificação"
                />
            </v-flex>

            <v-flex xs12 md5 offset-md1>
                <v-flex xs12>
                    <v-alert v-if="error" type="error">{{ error }}</v-alert>
                </v-flex>
                <h3 class="font-weight-light headline">Checar saída</h3>
                <v-list-item
                    v-for="user in users"
                    :key="user.email"
                    class="selectable-list-item"
                    :two-line="user.token.length === 0"
                    :three-line="user.token.length > 0"
                >
                    <v-list-item-icon>
                        <v-icon :color="getColor(user)" v-text="getIcon(user)"></v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ user.first_name }} {{ user.last_name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
                        <v-list-item-subtitle v-if="user.token.length > 0">
                            Token:
                            <kbd>{{ user.token }}</kbd>
                        </v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action v-if="user.token">
                        <v-btn icon>
                            <v-icon color="grey lighten-1" @click="$copyText(user.token)">far fa-copy</v-icon>
                        </v-btn>
                    </v-list-item-action>
                </v-list-item>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                csv: "",
                validCsv: [],
                error: "",
                users: [],
                createLoading: false,
                sendEmails: false
            }
        },
        computed: {
            formatIsValid() {
                return this.csv.length > 0 && this.csv === this.validCsv
            }
        },
        methods: {
            checkFormat() {
                this.error = ""
                try {
                    this.users = formatCSV(this.csv)
                    this.validCsv = this.csv
                } catch (error) {
                    this.error = error
                }
            },
            createUsers() {
                this.createLoading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/api/users/batch_create/",
                        data: {
                            users: this.users,
                            send_emails: this.sendEmails
                        }
                    })
                    .then(data => {
                        this.validCsv = ""
                        this.users = data.users.reduce((users, user) => {
                            user.token = user.token || ''
                            users.push(user)
                            return users
                        }, [])
                    })
                    .catch(() => {
                        this.validCsv = ""
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                    })
                    .then(() => {
                        this.createLoading = false
                    })
            },
            getIcon(user) {
                const map = {
                    pending: "far fa-circle",
                    success: "fas fa-check-circle",
                    error: "fas fa-times-circle"
                }
                return map[user.result]
            },
            getColor(user) {
                const map = {
                    pending: "black",
                    success: "green",
                    error: "red"
                }
                return map[user.result]
            }
        }
    }

    function formatCSV(csv) {
        const rows = csv.split("\n")
        if (csv.length === 0) {
            throw new Error("Não tem nada aqui")
        }
        const users = {}
        return rows.map(function(row, i) {
            i = i + 1
            const columns = row.split(",")
            if (columns.length !== 3) {
                throw new Error(
                    "Linha " +
                        i +
                        " tem " +
                        columns.length +
                        " valores. Eram esperados 3"
                )
            }
            const FirstName = columns[0].trim()
            const LastName = columns[1].trim()
            const email = columns[2].trim().toLowerCase()
            if (FirstName.length === 0 || LastName.length === 0) {
                throw new Error("Linha " + i + ", nome ou sobrenome vazios")
            }
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            if (!re.test(String(email).toLowerCase())) {
                throw new Error("Linha " + i + ", email inválido")
            }
            if (users[email]) {
                throw new Error("Linha " + i + ", email já digitado")
            }
            users[email] = true

            return {
                first_name: FirstName,
                last_name: LastName,
                email: email,
                result: "pending",
                token: ""
            }
        })
    }
</script>
<style>
    .selectable-list-item {
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
        user-select: text;
    }
</style>
