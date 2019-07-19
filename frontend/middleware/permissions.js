const getMatchedComponents = (route, matches = false) => {
    return [].concat.apply([], route.matched.map(function (m, index) {
        return Object.keys(m.components).map(function (key) {
            matches && matches.push(index)
            return m.components[key]
        })
    }))
}

function runMiddleware(ctx, permissions) {
    // If the user does not have permission, return
    if (!permissions({
            ctx: ctx,
            app: ctx.app,
            user: ctx.$auth.user,
            settings: ctx.store.state.settings.settings
        })) {
        ctx.app.$cookies.set('messages', [['', '', 'error', 'Você não tem permissão para isso']])
        ctx.$auth.redirect('home')
    }
}

export default function (ctx) {
    // Ignore unauthenticated requests
    if (!ctx.$auth.loggedIn) {
        return
    }

    const matches = []
    const Components = getMatchedComponents(ctx.route, matches)
    // Disable middleware if no route was matched to allow 404/error page
    if (!Components.length) {
        return
    } else if (Components.length > 1) {
        console.error("More than one Component matched? What?", Components)
        return
    }

    const permissions = Components[0].options.permissions

    // Ignore if page did not set permissions
    if (!permissions) {
        return
    }
    // If settings is not set, fetch it
    if (Object.keys(ctx.store.state.settings.settings).length === 0) {
        return ctx.$auth.request("/api/settings/").then(settings => {
            ctx.store.commit("settings/set", settings)
            // Execute async middleware
            return runMiddleware(ctx, permissions)
        })
    }
    // Execute middleware as normal
    return runMiddleware(ctx, permissions)
}
