class InvalidDeviceReadingException(ValueError):
    def __init__(self, device_id, invalid_value):
        self.device_id = device_id
        self.invalid_value = invalid_value
        super().__init__(
            f"Gia tri {invalid_value} khong hop le tren thiet bi {device_id}"
        )
