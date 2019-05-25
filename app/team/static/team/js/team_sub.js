import { BaseSubscription } from 'model_sockets/js/subscription';

export default class TeamSubscription extends BaseSubscription {
    constructor(team_id, signal, debug) {
        super(debug);
        this.team_id = team_id;
        this.signal = signal;
        this.url =
            "/ws/subscriptions/team/" +
            team_id +
            "/" +
            signal +
            "/";
    }
}
