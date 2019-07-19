<template>
    <div id="login">
        <v-container>
            <div class="content">
                <v-card>
                    <v-container>
                        <div class="logo">
                            <img src="~/static/img/logo.png" />
                        </div>
                        <v-expand-transition leave-absolute>
                            <div v-if="loginState === 'login'">
                                <v-form :loading="formLoading">
                                    <v-btn
                                        class="my-3"
                                        block
                                        tile
                                        color="blue"
                                        :href="baseURL + `/social/login/facebook/`"
                                    >
                                        <v-icon left>fab fa-facebook-f</v-icon>Entrar com Facebook
                                    </v-btn>
                                    <v-btn
                                        class="my-3"
                                        block
                                        tile
                                        color="black"
                                        :href="baseURL + `/social/login/github/`"
                                    >
                                        <v-icon left>fab fa-github</v-icon>Entrar com GitHub
                                    </v-btn>
                                    <v-btn
                                        class="my-3"
                                        block
                                        tile
                                        color="red"
                                        :href="baseURL + `/social/login/google/`"
                                    >
                                        <v-icon left>fab fa-google</v-icon>Entrar com Google
                                    </v-btn>
                                </v-form>
                                <v-divider></v-divider>
                                <v-btn
                                    v-show="!showTokenField"
                                    class="my-3 login"
                                    block
                                    tile
                                    @click="showTokenField = true"
                                >Usar token para acesso</v-btn>
                                <v-form
                                    v-show="showTokenField"
                                    :error="error"
                                    class="my-3"
                                    @submit.prevent="tokenLogin()"
                                >
                                    <v-alert v-show="errorMessage" type="error">{{ errorMessage }}</v-alert>
                                    <v-text-field
                                        v-model="token"
                                        :loading="tokenLoading"
                                        :disabled="tokenLoading"
                                        type="text"
                                        label="Token"
                                        required
                                        placeholder="AbC123"
                                    />
                                    <v-btn
                                        :loading="tokenLoading"
                                        :disabled="tokenLoading"
                                        class="mb-3 login"
                                        block
                                        tile
                                        @click="tokenLogin"
                                    >Entrar com token</v-btn>
                                </v-form>
                            </div>
                        </v-expand-transition>
                        <v-expand-transition leave-absolute>
                            <div v-if="loginState === 'forgot'">
                                <div class="forgot-password form">
                                    <v-form :success="success" @submit.prevent="sendResetEmail()">
                                        <v-message success>{{ successMessage }}</v-message>
                                        <v-text-field
                                            v-model="resetEmail"
                                            type="email"
                                            label="Email"
                                            :loading="emailLoading"
                                            :disabled="emailLoading"
                                            required
                                            placeholder="foo@bar.com"
                                        />
                                        <v-btn
                                            :loading="emailLoading"
                                            :disabled="emailLoading"
                                            class="my-3 login"
                                            block
                                            tile
                                        >Recuperar token</v-btn>
                                    </v-form>
                                </div>
                            </div>
                        </v-expand-transition>

                        <v-divider />

                        <div v-if="loginState === 'login'" class="forgot mt-3">
                            <a href="#" @click="setLoginState('forgot')">Esqueceu seu token?</a>
                        </div>
                        <div v-if="loginState === 'forgot'" class="forgot mt-3">
                            <a href="#" @click="setLoginState('login')">Fazer login</a>
                        </div>
                    </v-container>
                </v-card>
            </div>
        </v-container>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                errorMessage: "",
                successMessage: "",
                loginState: "login",
                tokenLoading: false,
                emailLoading: false,
                formLoading: false,
                showTokenField: false,
                resetEmail: "",
                token: ""
            }
        },
        computed: {
            error: function() {
                return this.errorMessage !== ""
            },
            success: function() {
                return this.successMessage !== ""
            },
            baseURL() {
                return process.env.API_URL_BROWSER
            }
        },
        created() {
            if (this.$auth.loggedIn) {
                this.$router.push("/")
            }
        },
        beforeMount() {
            if (this.$route.query.token) {
                this.login(this.$route.query.token)
            }
        },
        methods: {
            setLoginState(state) {
                this.loginState = state
            },
            tokenLogin() {
                this.errorMessage = ""
                if (this.token === "") return
                this.tokenLoading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/auth/token/check/",
                        data: {
                            token: this.token
                        }
                    })
                    .then(response => {
                        this.$auth
                            .request({
                                method: "post",
                                url: "/auth/token/login/",
                                data: {
                                    token: this.token
                                }
                            })
                            .then(response => {
                                this.login(response.token)
                            })
                    })
                    .catch(error => {
                        this.errorMessage = error.response.data.error
                        this.tokenLoading = false
                        return Promise.reject(error)
                    })
            },
            sendResetEmail() {
                if (this.resetEmail === "") return
                this.emailLoading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "/profile/api/reset_token_email/",
                        data: {
                            email: this.resetEmail
                        }
                    })
                    .then(response => {
                        this.successMessage = response.data.message
                    })
                    .catch(error => {
                        console.error(error)
                    })
                    .then(() => {
                        this.emailLoading = false
                    })
            },
            login(token) {
                this.formLoading = true
                this.$auth
                    .loginWith("local", {
                        data: {
                            token: token
                        }
                    })
                    .then(() => {
                        this.$router.push("/")
                    })
                    .catch(err => {
                        this.formLoading = false
                        if (err.response.status === 400) {
                            this.$toast(
                                "Opa!",
                                "Parece que você não tem acesso para entrar",
                                "error"
                            )
                        } else {
                            this.$toast(
                                "Opa!",
                                "Algo de errado aconteceu!",
                                "error"
                            )
                        }
                    })
            }
        },
        auth: false,
        layout: "login"
    }
</script>
