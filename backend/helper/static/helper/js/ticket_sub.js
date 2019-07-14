import { SubscriptionManager } from 'model_sockets/js/subscription';

export default class TicketSubscription extends SubscriptionManager {
    constructor(unique_id, signal, debug) {
        const url =
            "/ws/subscriptions/tickets/" +
            unique_id +
            "/universal/";
        super(url, debug, true, signal);
        this.unique_id = unique_id;
    }
}
