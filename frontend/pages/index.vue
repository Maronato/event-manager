<template>
    <div id="dashboard" class="page">
        <div class="divided big-title">Dashboard</div>
        <div class="page">
            <div class="status">
                <!-- Visível a hackers o tempo todo ou para outros não verificados -->
                <State v-if="$auth.user.is_hacker || $auth.user.state === 'unverified'" />

                <CompleteApp v-if="completeAppPerms" />

                <!-- Visível para todos não verificados -->
                <ResendEmail v-if="$auth.user.state === 'unverified'" />

                <!-- Visível a hackers que foram admitidos -->
                <Confirm v-if="$auth.user.state === 'admitted'" />

                <!-- Visível a hackers que se abstiveram -->
                <UndoWithdraw v-if="$auth.user.state=='withdraw'" />

                <!-- Visível a hackers que não pagaram -->
                <Payment v-if="$auth.user.state=='unpaid'" />

                <!-- Visível a hackers que confirmaram -->
                <Info v-if="$auth.user.state=='confirmed'" />

                <!-- Visível sempre para quem não é hacker ou para hackers confirmados e que fizeram checkin -->
                <Reminders
                    v-if="!$auth.user.is_hacker || ($auth.user.is_hacker && ($auth.user.state === 'confirmed' || $auth.user.state === 'checkedin'))"
                />

                <!-- Visível sempre para quem não é hacker ou para hackers confirmados e que fizeram checkin -->
                <QRid
                    v-if="!$auth.user.is_hacker || ($auth.user.is_hacker && ($auth.user.state === 'confirmed' || $auth.user.state === 'checkedin'))"
                />

                <!-- Visível a hackers que confirmaram -->
                <Withdraw v-if="$auth.user.state=='confirmed'" />

                <!-- Visível sempre pra todos -->
                <no-ssr>
                    <Access />
                </no-ssr>
            </div>
        </div>
    </div>
</template>

<script>
    import Access from "~/components/dashboard/sections/Access"
    import QRid from "~/components/dashboard/sections/QRid"
    import State from "~/components/dashboard/sections/State"
    import ResendEmail from "~/components/dashboard/sections/ResendEmail"
    import Confirm from "~/components/dashboard/sections/Confirm"
    import UndoWithdraw from "~/components/dashboard/sections/UndoWithdraw"
    import Withdraw from "~/components/dashboard/sections/Withdraw"
    import Info from "~/components/dashboard/sections/Info"
    import CompleteApp from "~/components/dashboard/sections/CompleteApp"
    import Reminders from "~/components/dashboard/sections/Reminders"
    import Payment from "~/components/dashboard/sections/Payment"

    export default {
        components: {
            Access,
            QRid,
            State,
            ResendEmail,
            Confirm,
            UndoWithdraw,
            Withdraw,
            Info,
            CompleteApp,
            Reminders,
            Payment
        },
        head() {
            return { title: "Dashboard" }
        },
        computed: {
            completeAppPerms() {
                return this.$perms.application({
                    app: this,
                    user: this.$auth.user,
                    settings: this.$store.state.settings.settings
                })
            }
        }
    }
</script>
