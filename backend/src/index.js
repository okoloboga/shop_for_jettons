const express = require('express');
const router = require('./routes/route');
const apicache = require('apicache');

const {
    swaggerDocs: SwaggerDocs,
} = require('./swagger.js');

const app = express();
const cache = apicache.middleware;
const PORT = process.env.PORT || 3000;

app.use(cache('2 minutes'))
app.use('/api', router);
app.listen(PORT, () => {
	console.log(`API is listening on port ${PORT}`);
    SwaggerDocs(app, PORT);
})

