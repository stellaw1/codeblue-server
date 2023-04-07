import { Router } from 'express';
import { handle_req, handle_heartrate, handle_detect } from './default.js';

const router = Router();

router.post('/', handle_req);

router.post('/heartrate', handle_heartrate);

router.post('/detect', handle_detect);

export default router;
