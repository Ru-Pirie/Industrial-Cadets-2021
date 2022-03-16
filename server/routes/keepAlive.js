const path = require('path');

class Event {
	constructor(app) {
        this.route = '/alive/:door/:status'
        this.methods = [ 'post' ]
	}

    uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }
      

	async process(db, req, res, next) {
        const dbRes = await db.prepare('SELECT * FROM doors WHERE name = ?').all(req.params.door);
        
        let alarm;
        switch (req.params.status) {
            case 'ok':
                alarm = 0;
                break;
            case 'trig':
                alarm = 1;
                break;
            case 'rst':
                alarm = 2;
                break;
            default:
                alarm = 3;
                break;
        }

        if (dbRes.length === 0) {
            const id = this.uuidv4()
            await db.prepare('INSERT INTO doors (id, trigger, alive, ping, name) VALUES (?, ?, ?, ?, ?)').run(id, alarm, 1, 1, req.params.door);
            await db.prepare('INSERT INTO pings (id) VALUES (?)').run(id);
        } else {
            const id = db.prepare('SELECT * FROM doors WHERE name = ?').get(req.params.door);
            await db.prepare('INSERT INTO pings (id) VALUES (?)').run(id.id);
            await db.prepare('UPDATE doors SET trigger = ? WHERE id = ?').run(alarm, id.id);
        }

        res.end(JSON.stringify({ ack: true }))
	}
}

module.exports = {
	Event,
};
