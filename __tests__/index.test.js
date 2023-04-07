import request from 'supertest';
import app from '../src/index.js';
import * as data from './data/data.js';

describe('Server Tests', function () {
    test('responds to /', async () => {
        const res = await request(app)
            .post('/')
            .send(JSON.stringify(data.valid_body));
        expect(res.header['content-type']).toBe('text/html; charset=utf-8');
        expect(res.statusCode).toBe(200);
    });

    // test('responds to /healthy', async () => {
    //     const res = await request(app).post('/healthy');
    //     expect(res.header['content-type']).toBe('text/html; charset=utf-8');
    //     expect(res.statusCode).toBe(200);
    //     expect(res.text).toEqual('hello jaxnode!');
    // });

    // test('responds to /ca', async () => {
    //     const res = await request(app).post('/ca');
    //     expect(res.header['content-type']).toBe('text/html; charset=utf-8');
    //     expect(res.statusCode).toBe(200);
    //     expect(res.text).toEqual('hello Annie!');
    // });
});
