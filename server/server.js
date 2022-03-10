const express = require('express');
const parser = require('body-parser');
const multer = require('multer');
const fs = require('fs')

fs.unlinkSync('./data.db');

const db = require('better-sqlite3')('data.db');
const path = require('path');

const upload = multer({ dest: './images/temp'})

const app = express()

async function setupDB() {
	await db.prepare('CREATE TABLE IF NOT EXISTS doors(    `id` VARCHAR(36) NOT NULL PRIMARY KEY,    `trigger` TINYINT NOT NULL DEFAULT 0,    `alive` TINYINT NOT NULL DEFAULT 1,    `ping` TINYINT NOT NULL DEFAULT 0,    `name` VARCHAR(2048))').run()
	await db.prepare('CREATE TABlE IF NOT EXISTS pings (`id` VARCHAR(2048) NOT NULL, `receuved` TIMESTAMP NOT NULL)').run()
}

setupDB();

require('dotenv').config()

// Image Err Handeler
const handleError = (err, res) => {
    res
      .status(500)
      .contentType("text/plain")
      .end("Oops! Something went wrong!");
};

// parse application/x-www-form-urlencoded
app.use(parser.urlencoded({ extended: false }))

// parse application/json
app.use(parser.json())

const routes = fs.readdirSync('./routes');

routes.forEach(async route => {
	console.log(route)
    if (route.includes('.html')) return;
    const file = require(`./routes/${route}`)
    const event = new file.Event(app);
    console.log(`Processing route file:\n    Route - ${event.route}\n    Methods - [ ${event.methods.join(', ')} ]`)    
    console.log(event)
    app[event.methods[0]](event.route, async function (...args) {
        event.process(db, ...args)
    })
});

app.post("/door/:id", upload.array('file', 12), async (req, res) => {
    if (req.files && req.files.length === 0) return res.status(400).end(JSON.stringify({ success: false, error: "No File Supplied" }))
    if (!fs.existsSync(`./images/${req.params.id}`)) fs.mkdirSync(`./images/${req.params.id}`);

    const imageName = `${Date.now()}.png`;

    const imageTempPath = req.files[0].path;
    const imageTargetPath = path.join(__dirname, `./images/${req.params.id}/${imageName}`);

    if (path.extname(req.files[0].originalname).toLowerCase() === ".png") {
        fs.rename(imageTempPath, imageTargetPath, err => {
            if (err) return handleError(err, res);

            res
                .status(200)
                .end(JSON.stringify({ success: true, name: imageName, path: imageTargetPath }));
        });
    }
    else {
        fs.unlink(imageTempPath, err => {
            if (err) return handleError(err, res);

            res
                .status(403)
                .end(JSON.stringify({ success: false, error: "Invalid File Format" }));
        });
    }
});

app.listen(process.env.PORT, () => {
    console.log(`\nRunning: http://localhost:${process.env.PORT}`)
})


