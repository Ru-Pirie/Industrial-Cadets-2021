const path = require('path');

class Event {
	constructor(app) {
        this.route = '/door/:door/:image'
        this.methods = [ 'post' ]
	}

	async process(db, req, res, next) {
        res.sendFile(path.join(__dirname, `../images/${req.params.door}/${req.params.image}`))
	}
}

module.exports = {
	Event,
};
