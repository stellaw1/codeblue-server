import * as def from '../src/routes/default.js';
import * as data from './data/data.js';

describe('default tests', function () {
    test('valid request format', () => {
        expect(def.validate_request_format(data.valid_body)).toBe(true);
    });
    test('missing sensors request format', () => {
        expect(def.validate_request_format(data.missing_sensors_body)).toBe(
            false
        );
    });
    test('missing device_id request format', () => {
        expect(def.validate_request_format(data.missing_device_id_body)).toBe(
            false
        );
    });
    test('missing sensor data request format', () => {
        expect(def.validate_request_format(data.missing_sensor_data_body)).toBe(
            false
        );
    });
    test('missing sensor location request format', () => {
        expect(
            def.validate_request_format(data.missing_sensor_location_body)
        ).toBe(false);
    });
    test('invalid device_id type request format', () => {
        expect(
            def.validate_request_format(data.invalid_device_id_type_body)
        ).toBe(false);
    });
    test('invalid sensor data type request format', () => {
        expect(
            def.validate_request_format(data.invalid_sensor_data_type_body)
        ).toBe(false);
    });
});
