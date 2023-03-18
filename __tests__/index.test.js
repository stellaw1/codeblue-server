import request from 'supertest';
import express from 'express';
import router from '../index.js';

const app = new express();
app.use('/', router);

describe('Server Tests', function () {
    test('responds to /', async () => {
        const res = await request(app).get('/');
        expect(res.header['content-type']).toBe('text/html; charset=utf-8');
        expect(res.statusCode).toBe(200);
        expect(res.text).toEqual('hello world!');
    });

    test('responds to /healthy', async () => {
        const res = await request(app).post('/healthy');
        expect(res.header['content-type']).toBe('text/html; charset=utf-8');
        expect(res.statusCode).toBe(200);
        expect(res.text).toEqual('hello jaxnode!');
    });

    test('responds to /ca', async () => {
        const res = await request(app).post('/ca');
        expect(res.header['content-type']).toBe('text/html; charset=utf-8');
        expect(res.statusCode).toBe(200);
        expect(res.text).toEqual('hello Annie!');
    });
});
