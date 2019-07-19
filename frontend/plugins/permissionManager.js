const perms = {
    application: ({ user }) => {
        return user.state === 'incomplete' || user.state === "submitted"
    },
    admin: ({ user }) => {
        return user.is_admin
    },
    staff: ({ user }) => {
        return user.is_staff
    },
    company: ({ user }) => {
        return user.is_employee && user.employee_company_access >= 0
    },
    team: ({ user }) => {
        return user.is_hacker && user.state === 'checkedin'
    },
    schedule: ({ user }) => {
        return (user.is_hacker ? user.state === "confirmed" || user.state === "checkedin" : false) || user.is_staff || user.is_admin || user.employee_company_access >= 0
    },
    helper: ({ user }) => {
        return user.is_mentor || user.employee_company_access >= 0 || user.is_staff || (user.is_hacker && user.state === "checkedin")
    },
    stats: ({user}) => {
        return user.is_admin || user.is_staff || user.employee_company_access >= 0
    }
}

export default ({ app }, inject) => {
    inject('perms', perms)
}
