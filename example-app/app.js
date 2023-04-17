const express = require('express')
const app = express()
const port = 80

app.get('/', (req, res) => {
    res.send('Hello World!\n')
})

app.listen(port, () => {
    console.log(`This app is listening at http://localhost:${port}`)
})
