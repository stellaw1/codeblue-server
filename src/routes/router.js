import { Router } from 'express';
import { handle_dummy, handle_req, handle_healthy, handle_ca } from './default.js';

const router = Router();

router.get('/', handle_dummy);
router.post('/', handle_req);

router.post('/healthy', handle_healthy);

router.post('/ca', handle_ca);

export default router;