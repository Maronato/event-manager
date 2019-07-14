<template>
    <div id="login">
        <v-container>
            <div class="content">
                <v-segment>
                    <div class="logo">
                        <img :src="context.event_logo" />
                    </div>
                    <v-divider horizontal></v-divider>
                    <div v-if="loginState === 'login'">
                        <v-form :loading="formLoading">
                            <v-form-field>
                                <v-btn
                                    type="btn"
                                    fluid
                                    social="facebook"
                                    content="Entrar com Facebook"
                                    icon="facebook"
                                    @click="socialLogin('facebook')"
                                />
                            </v-form-field>
                            <v-form-field>
                                <v-btn
                                    type="btn"
                                    fluid
                                    color="black"
                                    content="Entrar com GitHub"
                                    icon="github"
                                    @click="socialLogin('github')"
                                />
                            </v-form-field>
                            <v-form-field>
                                <v-btn
                                    type="btn"
                                    fluid
                                    social="youtube"
                                    content="Entrar com Google"
                                    icon="google"
                                    @click="socialLogin('google')"
                                />
                            </v-form-field>
                        </v-form>
                        <v-divider horizontal>Ou</v-divider>
                        <v-btn
                            v-show="!showTokenField"
                            type="btn"
                            class="login"
                            fluid
                            content="Usar token para acesso"
                            @click="showTokenField = true"
                        />
                        <v-form
                            v-show="showTokenField"
                            :error="error"
                            @submit.prevent="tokenLogin()"
                        >
                            <v-form-field>
                                <v-message error>{{ errorMessage }}</v-message>
                                <label>Token</label>
                                <v-input
                                    v-model="token"
                                    :loading="tokenLoading"
                                    :disabled="tokenLoading"
                                    type="text"
                                    required
                                    placeholder="AbC123"
                                />
                            </v-form-field>
                            <v-btn
                                :loading="tokenLoading"
                                :disabled="tokenLoading"
                                class="login"
                                fluid
                                content="Entrar com token"
                                type="submit"
                            />
                        </v-form>
                    </div>
                    <div v-if="loginState === 'forgot'">
                        <div class="ui forgot-password form">
                            <v-form :success="success" @submit.prevent="sendResetEmail()">
                                <v-message success>{{ successMessage }}</v-message>
                                <v-form-field>
                                    <label>Email</label>
                                    <v-input
                                        v-model="resetEmail"
                                        type="email"
                                        :loading="emailLoading"
                                        :disabled="emailLoading"
                                        required
                                        placeholder="foo@bar.com"
                                    />
                                </v-form-field>
                                <v-form-field>
                                    <v-btn
                                        :loading="emailLoading"
                                        :disabled="emailLoading"
                                        class="login"
                                        fluid
                                        content="Recuperar token"
                                        type="submit"
                                    />
                                </v-form-field>
                            </v-form>
                        </div>
                    </div>

                    <div class="ui divider"></div>

                    <div v-if="loginState === 'login'" class="forgot">
                        <a href="#" @click="setLoginState('forgot')">Esqueceu seu token?</a>
                    </div>
                    <div v-if="loginState === 'forgot'" class="forgot">
                        <a href="#" @click="setLoginState('login')">Fazer login</a>
                    </div>
                </v-segment>
            </div>
        </v-container>
    </div>
</template>
<script>
    import axios from "axios"

    export default {
        props: ["loginContext"],
        data() {
            return {
                errorMessage: login_context.error != "" ? login_context.error : "",
                successMessage: "",
                loginState: "login",
                tokenLoading: false,
                emailLoading: false,
                formLoading: false,
                showTokenField: false,
                resetEmail: "",
                token: "",
                context: login_context
            }
        },
        computed: {
            error: function() {
                return this.errorMessage != ""
            },
            success: function() {
                return this.successMessage != ""
            }
        },
        methods: {
            setLoginState(state) {
                this.loginState = state
            },
            tokenLogin() {
                self.errorMessage = ""
                if (this.token === "") return
                self = this
                this.tokenLoading = true
                axios
                    .post(this.context.check_token_url, {
                        token: this.token
                    })
                    .then(function(response) {
                        window.location.href = response.data.redirect_url
                    })
                    .catch(function(error) {
                        self.errorMessage = error.response.data.error
                        self.tokenLoading = false
                    })
            },
            sendResetEmail() {
                if (this.resetEmail === "") return
                self = this
                this.emailLoading = true
                axios
                    .post(this.context.reset_email_url, {
                        email: self.resetEmail
                    })
                    .then(function(response) {
                        self.successMessage = response.data.message
                    })
                    .catch(function(error) {
                        console.error(error)
                    })
                    .then(function() {
                        self.emailLoading = false
                    })
            },
            socialLogin(login) {
                this.formLoading = true
                if (login === "facebook") {
                    window.location.pathname = this.context.social_urls.facebook
                }
                if (login === "github") {
                    window.location.pathname = this.context.social_urls.github
                }
                if (login === "google") {
                    window.location.pathname = this.context.social_urls.google
                }
            }
        }
    }
</script>

<script>
    export default {
        data() {
            return {
                token: ""
            }
        },
        mounted() {
            const query = new URLSearchParams(window.location.search)
            if (query.get("token")) {
                this.token = query.get("token")
                this.login()
            }
        },
        methods: {
            login() {
                this.loading = true
                this.$auth
                    .loginWith("local", {
                        data: {
                            token: this.token
                        }
                    })
                    .then(() => {
                        this.$router.push("/")
                    })
                    .catch(err => {
                        this.loading = false
                        if (err.response.status === 400) {
                            this.loginFail = true
                        } else {
                            this.error = true
                            this.errorMessage = "Oops! Algo de errado aconteceu!"
                        }
                    })
            }
        },
        options: {
            auth: false
        }
    }
</script>
