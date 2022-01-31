class Event {
	constructor(app) {
	this.route = '/alarm/:id'
       	this.methods = [ 'all' ]
	}

	async process(db, req, res, next) {
		console.log(req.params.id)
		res.end(JSON.stringify({ success: true, message: 'Well Done!'}))

	}
}

module.exports = {
	Event,
};
