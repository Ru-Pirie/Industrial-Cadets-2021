class Event {
	constructor(app) {
	this.route = '/alarm/:id'
       	this.methods = [ 'ALL' ]
	}

	async process(req, res, next) {
		console.log(req.params.id)
		res.end(JSON.stringify({ success: true, message: 'Well Done!'}))

	}
}

module.exports = {
	Event,
};
