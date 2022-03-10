const f = require('fs')

class Event {
	constructor(app) {
	this.route = '/'
       	this.methods = [ 'ALL' ]
	}

	async process(req, res, next) {
		res.end('TESTING')
	}
}

module.exports = {
	Event,
};
