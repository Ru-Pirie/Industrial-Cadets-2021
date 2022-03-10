const fs = require('fs');

class Event {
	constructor(app) {
        this.route = '/door/:id'
        this.methods = [ 'get' ]
	}

	async process(db, req, res, next) {
        const files = fs.readdirSync(`./images/${req.params.id}`);

        const images = [];
        files.forEach(img => {
            images.push(`
            <p>    - <a href="/door/${req.params.id}/${img}">${img}</a></p>
            <div class="hover-img">
                <img src="/door/${req.params.id}/${img}">
            </div>
            `)
        })

		const html = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Ubuntu&display=swap');

        body {
            font-family: 'Ubuntu', sans-serif;
            background-color: gray;
            display: flex;
            justify-content: center;
        }

        .alarmTrue {
            color: red;
        }

        .alarmFalse {
            color: green;
        }

        h1 {
            text-align: center;
            width: 100%;
            margin-top: 25x;
        }

        h2 {
            margin-left: 15px;
        }

        .box {
            background-color: white;
            width: 50%;
            height: 100%;
            border-radius: 20px;       
        }

        .box p {
            margin-left: 15px;
        }text-align: center;
            }
        </style>
        <body>
            <div class="box">
                <h1>ID: <b>${req.params.id}</b></h1>
                <h2>Images:</h2>
                ${images.join('')}
            </div>
        </body>
        </html>
        `
        res.send(html)
	}
}

module.exports = {
	Event,
};
