const fs = require('fs')
const path = require('path');

class Event {
	constructor(app) {
	this.route = '/'
       	this.methods = [ 'get' ]
	}

	async process(db, req, res, next) {
		let file = fs.readFileSync(path.join(__dirname, '../html/index.html'), 'utf8')
        file = file.replace('{{doors}}', `
            <li class="null">Alpha - Offline</li>
            <li class="alarmed">Gamma - Alarmed</li>
            <li class="trigger">Delta - Triggered</li>
            <li class="reset">Theta - Awaiting Reset</li>
        `)
        res.end(file)
	}
}

module.exports = {
	Event,
};
