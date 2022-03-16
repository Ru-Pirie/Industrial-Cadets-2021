const fs = require('fs')
const path = require('path');

class Event {
	constructor(app) {
	this.route = '/'
       	this.methods = [ 'get' ]
	}

	async process(db, req, res, next) {
        const dbRes = await db.prepare('SELECT * FROM doors').all();
        const doors = [];

        for (const item of dbRes) {
            let a, b;

            if (item.alive === 0) {
                a = 'null';
                b = 'Offline'
            } else if (item.trigger === 3) {
                a = 'null';
                b = 'Unknown'
            } else if (item.trigger === 2) {
                a = 'reset';
                b = 'Awaiting Reset'
            } else if (item.trigger === 1) {
                a = 'trigger';
                b = 'Triggered'
            } else if (item.trigger === 0) {
                a = 'alarmed';
                b = 'Alarmed'
            } else {
                a = 'null';
                b = 'Unknown'
            }

            doors.push(`<li class="${a}">${item.name} - ${b}</li>`);
        }


		let file = fs.readFileSync(path.join(__dirname, '../html/index.html'), 'utf8')
        file = file.replace('{{doors}}', doors.join(''))
        res.end(file)
	}
}

module.exports = {
	Event,
};
