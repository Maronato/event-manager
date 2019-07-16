const colors = require('vuetify/es5/util/colors').default

module.exports = {
    mode: 'universal',

    server: {
        port: 3000,
        host: "0.0.0.0"
    },

    /*
     ** Headers of the page
     */
    head: {
        titleTemplate: '%s - ' + process.env.EVENT_NAME ,
        title:'',
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || ''
            }
        ],
        link: [
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
            {
                rel: 'stylesheet',
                href:
                    'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
            },
            {
                rel: "stylesheet",
                href: "//use.fontawesome.com/releases/v5.9.0/css/all.css"
            },
            {
                rel: "stylesheet",
                href: "//cdnjs.cloudflare.com/ajax/libs/izitoast/1.4.0/css/iziToast.min.css"
            }
        ]
    },
    /*
     ** Customize the progress-bar color
     */
    loading: { color: '#fff' },
    /*
     ** Global CSS
     */
    css: [
        '~/assets/scss/normalize.css',
        '~/assets/scss/site.scss'
    ],
    /*
     ** Plugins to load before mounting the App
     */
    plugins: [
        { src: '~/plugins/localStorage.js', mode: 'client' },
        { src: '~/plugins/toast.js', mode: 'client' },
        { src: '~/plugins/websockets.js', mode: 'client' },
        '~/plugins/moment.plugin.js',
        '~/plugins/eventBus.js',
    ],
    /*
     ** Nuxt.js modules
     */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios',
        '@nuxtjs/pwa',
        "@nuxtjs/auth",
    ],
    devModules: [
        '@nuxtjs/vuetify',
        '@nuxtjs/eslint-module',
    ],
    router: {
        middleware: ['auth']
    },
    env: {
        API_URL: process.env.API_URL,
        API_URL_BROWSER: process.env.API_URL_BROWSER,
        EVENT_NAME: process.env.EVENT_NAME,
        EVENT_DESCRIPTION: process.env.EVENT_DESCRIPTION,
    },
    axios: {
        credentials: true
    },
    /*
     ** Axios module configuration
     ** See https://axios.nuxtjs.org/options
     */
    auth: {
        strategies: {
            local: {
                tokenType: "JWT",
                endpoints: {
                    login: {
                        url: "/auth/jwt/login_with/",
                        method: "post",
                        propertyName: "token"
                    },
                    logout: {
                        url: "/auth/jwt/logout/",
                        method: "get",
                        propertyName: false
                    },
                    user: {
                        url: "/api/me/",
                        method: "get",
                        propertyName: false
                    }
                }
            }
        },
        redirect: {
            login: '/login',
            logout: '/login',
            home: '/'
        }
    },
    /*
     ** vuetify module configuration
     ** https://github.com/nuxt-community/vuetify-module
     */
    vuetify: {
        theme: {
            primary: colors.blue.darken2,
            accent: colors.grey.darken3,
            secondary: colors.amber.darken3,
            info: colors.teal.lighten1,
            warning: colors.amber.base,
            error: colors.deepOrange.accent4,
            success: colors.green.accent3
        },
        icons: {
            iconfont: 'fa'
        }
    },
    /*
     ** Build configuration
     */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {
            if (ctx.isDev) {
                config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
            }
        }
    }
}
