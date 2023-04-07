const valid_body = {
    sensors: [
        {
            data: [1, 2, 3],
            location: 'forehead'
        },
        {
            data: [1, 2, 3, 4, 5],
            location: 'wrist'
        }
    ],
    device_id:
        'dxDHYEeDQTqAr60WoA5qvi:APA91bF6XbB9eglqPbpk14UQOuJqQdHqgW7XWVa5GT_2uFjIHO3nYwKvnGG_tBW61h-pTETQf--1w8NDG1KW5bgfCbcdMoGop3Hvj8HLeSNYIuSoABhIYgIVQAEJ4JbffHGNHRv_vLZF'
};

const missing_sensors_body = {
    sensors: [],
    device_id:
        'dxDHYEeDQTqAr60WoA5qvi:APA91bF6XbB9eglqPbpk14UQOuJqQdHqgW7XWVa5GT_2uFjIHO3nYwKvnGG_tBW61h-pTETQf--1w8NDG1KW5bgfCbcdMoGop3Hvj8HLeSNYIuSoABhIYgIVQAEJ4JbffHGNHRv_vLZF'
};

const missing_device_id_body = {
    sensors: [
        {
            data: [1, 2, 3],
            location: 'forehead'
        },
        {
            data: [1, 2, 3, 4, 5],
            location: 'wrist'
        }
    ]
};

const missing_sensor_data_body = {
    sensors: [
        {
            data: [1, 2, 3],
            location: 'forehead'
        },
        {
            data: [],
            location: 'wrist'
        }
    ],
    device_id:
        'dxDHYEeDQTqAr60WoA5qvi:APA91bF6XbB9eglqPbpk14UQOuJqQdHqgW7XWVa5GT_2uFjIHO3nYwKvnGG_tBW61h-pTETQf--1w8NDG1KW5bgfCbcdMoGop3Hvj8HLeSNYIuSoABhIYgIVQAEJ4JbffHGNHRv_vLZF'
};

const missing_sensor_location_body = {
    sensors: [
        {
            data: [1, 2, 3]
        },
        {
            data: [1, 2, 3, 4, 5],
            location: 'wrist'
        }
    ],
    device_id:
        'dxDHYEeDQTqAr60WoA5qvi:APA91bF6XbB9eglqPbpk14UQOuJqQdHqgW7XWVa5GT_2uFjIHO3nYwKvnGG_tBW61h-pTETQf--1w8NDG1KW5bgfCbcdMoGop3Hvj8HLeSNYIuSoABhIYgIVQAEJ4JbffHGNHRv_vLZF'
};

const invalid_device_id_type_body = {
    sensors: [
        {
            data: [1, 2, 3],
            location: 'forehead'
        },
        {
            data: [1, 2, 3, 4, 5],
            location: 'wrist'
        }
    ],
    device_id: 12345
};

const invalid_sensor_data_type_body = {
    sensors: [
        {
            data: [1, 2, 'abc'],
            location: 'forehead'
        },
        {
            data: [1, 2, 3, 4, 5],
            location: 'wrist'
        }
    ],
    device_id:
        'dxDHYEeDQTqAr60WoA5qvi:APA91bF6XbB9eglqPbpk14UQOuJqQdHqgW7XWVa5GT_2uFjIHO3nYwKvnGG_tBW61h-pTETQf--1w8NDG1KW5bgfCbcdMoGop3Hvj8HLeSNYIuSoABhIYgIVQAEJ4JbffHGNHRv_vLZF'
};

export {
    valid_body,
    missing_sensors_body,
    missing_device_id_body,
    missing_sensor_data_body,
    missing_sensor_location_body,
    invalid_device_id_type_body,
    invalid_sensor_data_type_body
};
