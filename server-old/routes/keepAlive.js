const path = require('path');

class Event {
	constructor(app) {
        this.route = '/alive/:door/:status'
        this.methods = [ 'post' ]
	}

	async process(db, req, res, next) {
        console.log(req.params)
        res.end(JSON.stringify({ ack: true }))
	}
}

module.exports = {
	Event,
};
