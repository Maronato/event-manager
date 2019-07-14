import { SubscriptionManager } from 'model_sockets/js/subscription';

export default class MentorSubscription extends SubscriptionManager {
    constructor(debug) {
        const url =
            "/ws/subscriptions/online_mentor/";
        super(url, debug, true);
    }
}
