export default function ({app, $auth, params, redirect}) {
    const code = params.code
    console.log('verifying email', code)
    return $auth.request({
            method: "post",
            url: "/api/profiles/verify_email/",
            data: {
                code: code
            }
        }).then(response => {
            return $auth
                .loginWith("local", {
                    data: {
                        token: response.token
                    }
                })
                .then(() => {
                    return $auth.fetchUser().then(() => {
                        return redirect('/')
                    })
                })
        })
        .catch(() => {
            return redirect('/login/')
        })
}
